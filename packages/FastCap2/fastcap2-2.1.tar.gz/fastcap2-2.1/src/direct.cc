
#include "mulGlobal.h"
#include "mulDisplay.h"
#include "direct.h"
#include "calcp.h"
#include "counters.h"

double **Q2PDiag(ssystem *sys, charge **chgs, int numchgs, int *is_dummy, int calc)
{
  double **mat;
  int i, j;

  /* Allocate storage for the potential coefficients. */
  mat = sys->heap.mat(numchgs, numchgs, AQ2PD);

  if(calc) {
    /* Compute the potential coeffs. */
    /* - exclude dummy panels when they would need to carry charge
       - exclude dielec i/f panels when they would lead to evals at their
         centers (only if using two-point flux-den-diff evaluations) */
    for(i=0; i < numchgs; i++) { 
      if (NUMDPT == 2) {
        if(chgs[i]->dummy);     /* don't check surface of a dummy */
        else if(chgs[i]->surf->type == DIELEC || chgs[i]->surf->type == BOTH)
            continue;
      }
      for(j=0; j < numchgs; j++) { /* need to have charge on them */
        if (SKIPQD == ON) {
          if(chgs[j]->pos_dummy == chgs[i] || chgs[j]->neg_dummy == chgs[i])
              continue;
        }
        if(!is_dummy[j]) mat[i][j] = calcp(sys,
                                           chgs[j], chgs[i]->x, chgs[i]->y,
                                           chgs[i]->z, NULL);
      }
    }
  }

  if (sys->dsq2pd) {
    dispQ2PDiag(sys, mat, chgs, numchgs, is_dummy);
  }

  return(mat);
}

double **Q2P(ssystem *sys, charge **qchgs, int numqchgs, int *is_dummy, charge **pchgs, int numpchgs, int calc)
{
  double **mat;
  int i, j;

  /* Allocate storage for the potential coefficients. P rows by Q cols. */
  mat = sys->heap.mat(numpchgs, numqchgs, AQ2P);
  for(i=0; i < numpchgs; i++) {
    if(calc) {
      /* exclude:
         - dummy panels in the charge list
         - dielectric i/f panels in the eval list (if doing 2-point E's)*/
      if (NUMDPT == 2) {
        if(pchgs[i]->dummy);    /* don't check the surface of a dummy */
        else if(pchgs[i]->surf->type == DIELEC || pchgs[i]->surf->type == BOTH)
            continue;
      }
      for(j=0; j < numqchgs; j++) { /* only dummy panels in the charge list */
        if(!is_dummy[j])          /* (not the eval list) are excluded */
            mat[i][j] = calcp(sys,
                              qchgs[j], pchgs[i]->x, pchgs[i]->y,
                              pchgs[i]->z, NULL); /* old: pchgs[i],qchgs[j] */
      }
    }
  }

  if (sys->disq2p) {
    dispQ2P(sys, mat, qchgs, numqchgs, is_dummy, pchgs, numpchgs);
  }

  return(mat);
}

/*
  used only in conjunction with DMPMAT == ON  and DIRSOL == ON
  to make 1st directlist mat = full P mat
*/
double **Q2Pfull(ssystem *sys, cube *directlist, int numchgs)
{
  int i, j, fromp, fromq, top, toq;
  double **mat;
  cube *pq, *pp;
  charge **pchgs, **qchgs, *eval;

  /* allocate room for full P matrix */
  mat = sys->heap.mat(numchgs, numchgs, AQ2P);

  /* load the matrix in the style of Q2P() - no attempt to exploit symmetry */
  /* calculate interaction between every direct list entry and entire dlist */
  for(pp = directlist; pp != NULL; pp = pp->dnext) {
    pchgs = pp->chgs;
    fromp = pchgs[0]->index - 1; /* row index range */
    top = fromp + pp->upnumeles[0];
    for(pq = directlist; pq != NULL; pq = pq->dnext) {
      qchgs = pq->chgs;
      fromq = qchgs[0]->index - 1; /* column index range */
      toq = fromq + pq->upnumeles[0];

      for(i = fromp; i < top; i++) {
        for(j = fromq; j < toq; j++) { 
          eval = qchgs[j-fromq];
          mat[i][j] = calcp(sys, pchgs[i-fromp],eval->x, eval->y, eval->z, NULL);
        }
      }

    }
  }
  return(mat);
}

/*
  - returned matrix has L below the diagonal, U above (GVL1 pg 58)
  - if allocate == TRUE ends up storing P and LU (could be a lot)
*/
double **ludecomp(ssystem *sys, double **matin, int size, int allocate)
{
  double factor, **mat;
  int i, j, k;

  if(allocate == TRUE) {
    /* allocate for LU matrix and copy A */
    mat = sys->heap.mat(size, size);
    for(i = 0; i < size; i++) {
      for(j = 0; j < size; j++) mat[i][j] = matin[i][j];
    }
  }
  else mat = matin;

  for(k = 0; k < size-1; k++) { /* loop on rows */
    if(mat[k][k] == 0.0) {
      sys->error("ludecomp: zero piovt");
    }
    for(i = k+1; i < size; i++) { /* loop on remaining rows */
      factor = (mat[i][k] /= mat[k][k]);
      counters.fulldirops++;
      for(j = k+1; j < size; j++) { /* loop on remaining columns */
        mat[i][j] -= (factor*mat[k][j]);
        counters.fulldirops++;
      }
    }
  }
  return(mat);
}

/*
  For direct solution of Pq = psi, used if DIRSOL == ON or if preconditioning.
*/
void solve(double **mat, double *x, double *b, int size)
{
  int i, j;

  /* copy rhs */
  if(x != b) for(i = 0; i < size; i++) x[i] = b[i];

  /* forward elimination */
  for(i = 0; i < size; i++) {   /* loop on pivot row */
    for(j = i+1; j < size; j++) { /* loop on elimnation row */
      x[j] -= mat[j][i]*x[i];
      counters.fulldirops++;
    }
  }

  /* back substitution */
  for(i--; i > -1; i--) {               /* loop on rows */
    for(j = i+1; j < size; j++) { /* loop on columns */
      x[i] -= mat[i][j]*x[j];
      counters.fulldirops++;
    }
    x[i] /= mat[i][i];
    counters.fulldirops++;
  }
}

/* 
  In-place inverts a matrix using guass-jordan.
  - is_dummy[i] = 0 => ignore row/col i
*/
void invert(double **mat, int size, int *reorder)
{
  int i, j, k, best;
  double normal, multiplier, bestval, nextbest;
/*
  matlabDump(mat,size,"p");
*/
  for(i=0; i < size; i++) {
    best = i;
    bestval = ABS(mat[i][i]);
    for(j = i+1; j < size; j++) {
      nextbest = ABS(mat[i][j]);
      if(nextbest > bestval) {
        best = j;
        bestval = nextbest;
      }
    }

    /* If reordering, find the best pivot. */
    if(reorder != NULL) {
      reorder[i] = best;
      if(best != i) {
        for(k=0; k < size; k++) {
          bestval = mat[k][best];
          mat[k][best] = mat[k][i];
          mat[k][i] = bestval;
        }
      }
    }

    /* First i^{th} column of A. */
    normal = 1.0 / mat[i][i];
    for(j=0; j < size; j++) {
      mat[j][i] *= normal;
    }
    mat[i][i] = normal;

    /* Fix the backward columns. */
    for(j=0; j < size; j++) {
      if(j != i) {
        multiplier = -mat[i][j];
        for(k=0; k < size; k++) {
          if(k != i) mat[k][j] += mat[k][i] * multiplier;
          else mat[k][j] = mat[k][i] * multiplier;
        }
      }
    }
  }

  /* Unravel the reordering, starting with the last column. */
  if(reorder != NULL) {
    for(i=size-2; i >= 0; i--) {
      if(reorder[i] != i) {
        for(k=0; k < size; k++) {
          bestval = mat[k][i];
          mat[k][reorder[i]] = mat[k][i];
          mat[k][i] = bestval;
        }
      }
    }
  }
/*
  matlabDump(mat,size,"c");
*/

}

/*
  Used in conjuction with invert() to remove dummy row/columns
   comp_rows = TRUE => remove rows corresponding to ones in is_dummy[]
   comp_rows = FALSE => remove cols corresponding to ones in is_dummy[]
   comp_rows = BOTH => remove both rows and columns
   returns number of rows/cols in compressed matrix
*/
int compressMat(ssystem *sys, double **mat, int size, int *is_dummy, int comp_rows)
{
  static Heap local_heap;
  static int *cur_order;
  static int cur_order_array_size = 0;
  int cur_order_size, i, j, k;
  
  if(cur_order_array_size < size) {
    cur_order = local_heap.alloc<int>(size, AMSC);
  }
  
  /* figure the new order vector (cur_order[i] = index of ith row/col) */
  for(i = cur_order_size = 0; i < size; i++) {
    if(!is_dummy[i]) cur_order[cur_order_size++] = i;
  }

  if(comp_rows == TRUE || comp_rows == BOTH) {
    /* compress by removing rows from the matrix */
    for(i = 0; i < cur_order_size; i++) {
      if((k = cur_order[i]) == i) continue; /* if not reordered */
      for(j = 0; j < size; j++) { /* copy the row to its new location */
        mat[i][j] = mat[k][j];
      }
    }
  }
  if(comp_rows == FALSE || comp_rows == BOTH) {
    /* compress by removing columns from the matrix */
    for(j = 0; j < cur_order_size; j++) {
      if((k = cur_order[j]) == j) continue; /* if not reordered */
      for(i = 0; i < size; i++) { /* copy the col to its new location */
        mat[i][j] = mat[i][k];
      }
    }
  }
  return(cur_order_size);
}

/*
  Used in conjuction with invert() to add dummy row/columns
   exp_rows = TRUE => add rows corresponding to ones in is_dummy[]
   exp_rows = FALSE => add cols corresponding to ones in is_dummy[]
   exp_rows = BOTH => add rows and columns
*/
void expandMat(double **mat, int size, int comp_size, int *is_dummy, int exp_rows)
{
  int i, j, next_rc;

  if(exp_rows == TRUE || exp_rows == BOTH) {
    next_rc = comp_size - 1;
    /* add rows to the matrix starting from the bottom */
    for(i = size - 1; i >= 0; i--) {
      if(is_dummy[i]) {         /* zero out dummy row */
        for(j = 0; j < size; j++) mat[i][j] = 0.0;
      }
      else {                    /* copy the row from its compressed location */
        for(j = 0; j < size; j++) mat[i][j] = mat[next_rc][j];
        next_rc--;
      }
    }
  }
  if(exp_rows == FALSE || exp_rows == BOTH) {
    next_rc = comp_size - 1;
    /* add columns to the matrix starting from the right */
    for(j = size - 1; j >= 0; j--) {
      if(is_dummy[j]) {         /* zero out dummy column */
        for(i = 0; i < size; i++) mat[i][j] = 0.0;
      }
      else {                    /* copy the col from its compressed location */
        for(i = 0; i < size; i++) mat[i][j] = mat[i][next_rc];
        next_rc--;
      }
    }
  }
}

#if defined(UNUSED)
/*
Checks to see if the matrix has the M-matrix sign pattern and if
it is diagonally dominant. 
*/
static void matcheck(double **mat, int rows, int size)
{
  double rowsum;
  int i, j;

  for(i = rows - 1; i >= 0; i--) {
    for(rowsum = 0.0, j = size - 1; j >= 0; j--) {
      if((i != j)  && (mat[i][j] > 0.0)) {
        printf("violation mat[%d][%d] =%g\n", i, j, mat[i][j]);
      }
      if(i != j) rowsum += ABS(mat[i][j]);
    }
    printf("row %d diag=%g rowsum=%g\n", i, mat[i][i], rowsum);
    if(rowsum > mat[i][i]) {
      for(j = size - 1; j >= 0; j--) {
        printf("col%d = %g ", j, mat[i][j]);
      }
      printf("\n");
    }
  }
}
#endif

#if defined(UNUSED)
static void matlabDump(double **mat, int size, char *name)
{
FILE *foo;
int i,j;
char fname[100];

  sprintf(fname, "%s.m", name);
  foo = fopen(fname, "w");
  fprintf(foo, "%s = [\n", name);
  for(i=0; i < size; i++) {
    for(j=0; j < size; j++) {
      fprintf(foo, "%.10e  ", mat[i][j]);
    }
    fprintf(foo, "\n");
  }
  fprintf(foo, "]\n");
}
#endif

