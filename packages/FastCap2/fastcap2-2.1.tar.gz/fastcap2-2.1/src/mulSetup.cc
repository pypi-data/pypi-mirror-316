
#include "mulGlobal.h"
#include "mulSetup.h"
#include "mulMulti.h"
#include "mulStruct.h"
#include "input.h"
#include "calcp.h"

#include <cstdio>
#include <cstdlib>
#include <cassert>

cube *cstack[1024];             /* Stack used in several routines. */

static void getAllInter(ssystem *sys);
static void set_vector_masks(ssystem *sys);
static int placeq(int flag, ssystem *sys, charge *charges);
static void setMaxq(ssystem *sys);
static void indexkid(ssystem *sys, cube *dad, int *pqindex, int *pcindex);
static void linkcubes(ssystem *sys);
static void getnbrs(ssystem *sys);
static void getrelations(ssystem *sys);
static void setPosition(ssystem *sys);
static void setExact(ssystem *sys, int numterms);

/*
  sets up the partitioning of space and room for charges and expansions
*/
void mulInit(ssystem *sys, charge *charges)
{
  int qindex=1, cindex=1;

  if (sys->dirsol || sys->expgcr) {
    sys->depth = 0;                //  put all the charges in first cube
  }

  sys->depth = placeq(sys->depth < 0, sys, charges); /* create cubes, put in charges */

  getrelations(sys);            /* Get all the prnts and kids for each cube. */

  setPosition(sys);             /* Figures out position of cube center. */
  indexkid(sys, sys->cubes[0][0][0][0], &qindex, &cindex); 
                                /* Index chgs and cubes. */

#if ADAPT == ON
  setExact(sys, multerms(sys->order)); /* Note cubes to be done exactly and
                                           determine the number of nonempty
                                           kids for each cube. */
#else
  setExact(sys, 0);             /* Note cubes to be done exactly and
                                           determine the number of nonempty
                                           kids for each cube. */
#endif

  getnbrs(sys);                 /* Get all the nearest neighbors. At bot level
                                   add as nearest nbrs cubes in exact block. */
  linkcubes(sys);               /* Make linked-lists of direct, multis, and
                                   locals to do at each level. */
  set_vector_masks(sys);        /* set up sys->is_dummy and sys->is_dielec */
  setMaxq(sys);                 /* Calculates the max # chgs in cubes treated
                                   exactly, and over lowest level cubes. */
  getAllInter(sys);             /* Get the interaction lists at all levels. */
}

/*
  places the charges using best number of levels for adaptive algorithm
  - returns number of levels used
  - can be called with flag == OFF to set depth = sys->depth
  - uses entire panel list, dieletric and dummy panels are included
     (excluding BOTH or DIELELC type panels if NUMDPT == 2, ie 
     two-point flux-density-differences are being use ),
     so the constraining type of exactness is usually
     local expansion exactness---using this method the switch to multipole
     exactness is done automatically if there are no dielectric panels
  - when the method without dielectric panels is set up, these loops will
     need to ignore all dielectric panels
  - this routine is still called to set automatic levels if ADAPT is OFF,
     ie even when the calculation is not adaptive, so results can be compared
*/
static int placeq(int flag, ssystem *sys, charge *charges)
{
  int i, j, k, l, side, totalq, isexact, depth;
  int xindex, yindex, zindex, limit = multerms(sys->order), compflag;
  int exact_cubes_this_level, cubes_this_level;
  double length0, length, exact_ratio;
  double minx, maxx, miny, maxy, minz, maxz, maxTileLength;
  charge *nextq, *compq;
  cube *****cubes, *nextc;

  /* Figure out the length of lev 0 cube and total number of charges. */
  nextq = charges;
  minx = maxx = nextq->x;
  miny = maxy = nextq->y;
  minz = maxz = nextq->z;

  for(totalq = 1, nextq = nextq->next; nextq != NULL;
      totalq++, nextq = nextq->next) {
    maxx = MAX(nextq->x, maxx);
    minx = MIN(nextq->x, minx);
    maxy = MAX(nextq->y, maxy);
    miny = MIN(nextq->y, miny);
    maxz = MAX(nextq->z, maxz);
    minz = MIN(nextq->z, minz);
  }

  sys->minx = minx;
  sys->miny = miny;
  sys->minz = minz;

  /* Make sure cube isn't smaller than a tile. */
  for(maxTileLength = 0.0, nextq = charges;
      nextq != NULL; nextq = nextq->next) {
    length = tilelength(nextq);
    maxTileLength = MAX(maxTileLength, length);
  }
  if((maxx - minx) < maxTileLength) {
    maxx += 0.5 * maxTileLength;
    minx -= 0.5 * maxTileLength;
  }
  if((maxy - miny) < maxTileLength) {
    maxy += 0.5 * maxTileLength;
    miny -= 0.5 * maxTileLength;
  }
  if((maxz - minz) < maxTileLength) {
    maxz += 0.5 * maxTileLength;
    minz -= 0.5 * maxTileLength;
  }

  /* (see below for test for panel size vs cube size) */

  length0 = MAX((maxx - minx), (maxy - miny));
  length0 = MAX((maxz - minz), length0);

  /* Create the vectors for storing the charges and coefficients. */
  sys->q = sys->heap.alloc<double>(totalq + 1, AMSC);
  sys->p = sys->heap.alloc<double>(totalq + 1, AMSC);

  /* set up mask vector: is_dummy[i] = TRUE => panel i is a dummy */
  sys->is_dummy = sys->heap.alloc<int>(totalq + 1, AMSC);

  /* set up mask vector: is_dielec[i] = TRUE => panel i is on DIELEC or BOTH */
  sys->is_dielec = sys->heap.alloc<int>(totalq + 1, AMSC);

  if(flag == ON) {              /* set depth of partitions automatically */
    /* alloc spine of cube pntr array - leave enough room for depth = MAXDEP */
    cubes = sys->heap.alloc<cube****>(MAXDEP + 1, AMSC);

    /* allocate for levels 0, 1, and 2 (always used) */
    for(side = 1, i=0; i <= 2; side *= 2, i++) {
      cubes[i] = sys->heap.alloc<cube***>(side, AMSC);
      for(j=0; j < side; j++) {
        cubes[i][j] = sys->heap.alloc<cube**>(side, AMSC);
        for(k=0; k < side; k++) {
          cubes[i][j][k] = sys->heap.alloc<cube*>(side, AMSC);
        }
      }
    }
    /* side /= 2; */

    /* for each level > 2: allocate for full cubes, count panels in each 
       - quit loop if all lowest level cubes are exact */
    for(isexact = FALSE; isexact == FALSE; side *= 2, i++) {

      if(i > MAXDEP) {
        sys->error("placeq: out of cube pntr space - increase MAXDEP == %d",
                   MAXDEP);
      }

      length = (1.01 * length0)/side;

      cubes[i] = sys->heap.alloc<cube***>(side, AMSC);
      for(j=0; j < side; j++) {
        cubes[i][j] = sys->heap.alloc<cube**>(side, AMSC);
        for(k=0; k < side; k++) {
          cubes[i][j][k] = sys->heap.alloc<cube*>(side, AMSC);
        }
      }

      /* Count the number of charges per cube and allocate if needed */
      for(nextq = charges; nextq != NULL; nextq = nextq->next) {
        xindex = (nextq->x - minx) / length;
        yindex = (nextq->y - miny) / length;
        zindex = (nextq->z - minz) / length;
        nextc = cubes[i][xindex][yindex][zindex];
        if(nextc == NULL) {
          nextc = sys->heap.alloc<cube>(1, AMSC);
          /* TODO: not working any more ...
          if(nextc == NULL) {
            sys->error("placeq: %d levels set up\n", i-1);
          }
          */
          cubes[i][xindex][yindex][zindex] = nextc;
          nextc->upnumvects = 1;
          nextc->upnumeles = sys->heap.alloc<int>(1, AMSC);
          nextc->upnumeles[0] = 1;
        }
        else {
          nextc->upnumeles[0]++;
        }
      }

      /* if the current lowest level is not exact, loop back until it is */
      /*    check for exactness of this level, get cube statistics */
      isexact = TRUE;
      cubes_this_level = 0;
      exact_cubes_this_level = 0;
      for(j = 0; j < side; j++) {
        for(k = 0; k < side; k++) {
          for(l = 0; l < side; l++) {
            if(cubes[i][j][k][l] != NULL) {
              if(cubes[i][j][k][l]->upnumeles[0] > limit) {
                isexact = FALSE;
              }
              else exact_cubes_this_level++;
              cubes_this_level++;
            }
          }
        }
      }

      /*    decide whether to go down another level by checking exact/ttl */
      exact_ratio = (double)exact_cubes_this_level/(double)cubes_this_level;
      if(exact_ratio > EXRTSH) 
          isexact = TRUE;       /* set up to terminate level build loop */
      /* sys->msg("Level %d, %g%% exact\n", i, exact_ratio*100.0); */

      /* clean up cube structs if need to go down another level */
      if(isexact == FALSE) {
        for(j = 0; j < side; j++) {
          for(k = 0; k < side; k++) {
            for(l = 0; l < side; l++) {
              if(cubes[i][j][k][l] != NULL) {
                cubes[i][j][k][l]->upnumeles[0] = 0;
                cubes[i][j][k][l]->upnumvects = 0;
              }
            }
          }
        }
      }
    }
    depth = i - 1;              /* the automatically set depth */
    side /= 2;
  }
  else {                        /* old code - uses sys->depth for depth */
    /* Allocate the cubes, note calloc used because zeros everything. */
    depth = sys->depth;
    cubes = sys->heap.alloc<cube****>(sys->depth+1, AMSC);
    for(side = 1, i=0; i <= depth; side *= 2, i++) {
      cubes[i] = sys->heap.alloc<cube***>(side, AMSC);
      for(j=0; j < side; j++) {
        cubes[i][j] = sys->heap.alloc<cube**>(side, AMSC);
        for(k=0; k < side; k++) {
          cubes[i][j][k] = sys->heap.alloc<cube*>(side, AMSC);
        }
      }
    }
    side /= 2;
    length = (1.01 * length0)/side;

    /* Count the number of charges per cube. */
    for(nextq = charges; nextq != NULL; nextq = nextq->next) {
      xindex = (nextq->x - minx) / length;
      yindex = (nextq->y - miny) / length;
      zindex = (nextq->z - minz) / length;
      nextc = cubes[depth][xindex][yindex][zindex];
      if(nextc == NULL) {
        nextc = sys->heap.alloc<cube>(1, AMSC);
        cubes[depth][xindex][yindex][zindex] = nextc;
        nextc->upnumvects = 1;
        nextc->upnumeles = sys->heap.alloc<int>(1, AMSC);
        nextc->upnumeles[0] = 1;
      }
      else {
        nextc->upnumeles[0]++;
      }
    }
  }
  sys->length = length;
  sys->side = side;
  sys->cubes = cubes;

  /* Allocate space for the charges. */
  for(j=0; j < side; j++) {
    for(k=0; k < side; k++) {
      for(l=0; l < side; l++) {
        nextc = sys->cubes[depth][j][k][l];
        if(nextc != NULL) {  /* Only fill out nonempty cubes. */
          /* Allocate for the charge ptrs, and get q vector pointer. */
          nextc->chgs = sys->heap.alloc<charge*>(nextc->upnumeles[0], AMSC);
          nextc->upnumeles = sys->heap.alloc<int>(1, AMSC);
          /* Zero the numchgs to use as index. */
          nextc->upnumeles[0] = 0;
        }
      }
    }
  }

  /* Put the charges in cubes; check to make sure they are not too big. */
  for(nextq = charges; nextq != NULL; nextq = nextq->next) {
#if 1 == 0
    if(tilelength(nextq) > length) {
      sys->info(
              "\nplaceq: Warning, a panel is larger than the cube supposedly containing it\n");
      sys->info("  cube length = %g panel length = %g\n", 
              length, tilelength(nextq));
      /* disfchg(nextq); */
    }
#endif
    xindex = (nextq->x - minx) / length;
    yindex = (nextq->y - miny) / length;
    zindex = (nextq->z - minz) / length;
    nextc = cubes[depth][xindex][yindex][zindex];

    /* check if current charge is same as those already in the cube `nextc' */
    for(compflag = FALSE, i = (nextc->upnumeles[0] - 1); i >= 0; i--) {
      compq = nextc->chgs[i];
      if((compq->x == nextq->x) &&
         (compq->y == nextq->y) && (compq->z == nextq->z)) {
        sys->info("placeq: Warning, removing identical");
        if(compq->shape == 3) sys->info(" triangular");
        else if(compq->shape == 4) sys->info(" quadrilateral");
        else sys->info(" illegal-shape");
        sys->info(" panel\n  rmved ctr = (%g %g %g) surf = `%s'", 
                compq->x, compq->y, compq->z, hack_path(compq->surf->name));
        sys->info(" trans = (%g %g %g)\n", compq->surf->trans[0],
                compq->surf->trans[1], compq->surf->trans[2]);
        sys->info("  saved ctr = (%g %g %g) surf = `%s'", 
                nextq->x, nextq->y, nextq->z, hack_path(nextq->surf->name));
        sys->info(" trans = (%g %g %g)\n", nextq->surf->trans[0],
                nextq->surf->trans[1], nextq->surf->trans[2]);
        /* Remove charge from linked list. */
        for(compq = charges; compq->next != nextq; compq = compq->next) {};
        compq->next = nextq->next;
        nextq = compq;
        compflag = TRUE;
      }
    }
    if(compflag == FALSE) nextc->chgs[nextc->upnumeles[0]++] = nextq;

  }
  return(depth);
}
      
/*
GetRelations allocates parents links the children. 
*/
void getrelations(ssystem *sys)
{
cube *nextc, *parent, *****cubes = sys->cubes;
int i, j, k, l, side;
  for(i = sys->depth, side = sys->side; i >= 0; i--, side /= 2) {
    for(j=0; j < side; j++) {
      for(k=0; k < side; k++) {
        for(l=0; l < side; l++) {
          nextc = cubes[i][j][k][l];
          if(nextc != NULL) {
        /* Get the parents and children pointers of nonempty cubes. */
            if(i < sys->depth) {
              nextc->numkids = 8; /* all cubes, even empties, are counted */
              nextc->kids = sys->heap.alloc<cube*>(nextc->numkids, AMSC);
              nextc->kids[0] = cubes[i+1][2*j][2*k][2*l]; /* empties get */
              nextc->kids[1] = cubes[i+1][2*j][2*k][2*l+1]; /* null pointers */
              nextc->kids[2] = cubes[i+1][2*j][2*k+1][2*l];
              nextc->kids[3] = cubes[i+1][2*j][2*k+1][2*l+1];
              nextc->kids[4] = cubes[i+1][2*j+1][2*k][2*l];
              nextc->kids[5] = cubes[i+1][2*j+1][2*k][2*l+1];
              nextc->kids[6] = cubes[i+1][2*j+1][2*k+1][2*l];
              nextc->kids[7] = cubes[i+1][2*j+1][2*k+1][2*l+1];
            }
            if(i > 0) {
              parent = cubes[i-1][j/2][k/2][l/2];
              if(parent == NULL) {
                parent = sys->heap.alloc<cube>(1, AMSC);
                cubes[i-1][j/2][k/2][l/2] = parent;
              }
              nextc->parent = parent;
            }
          }
        }
      }
    }
  }
}

/*
Set the position coordinates of the cubes.
*/
void setPosition(ssystem *sys)
{
int i, j, k, l;
int side = sys->side;
double length = sys->length;
cube *nextc;

/* Mark the position of the lowest level cubes. */
  for(i=sys->depth; i >= 0; i--, side /= 2, length *= 2.0) {
    for(j=0; j < side; j++) {
      for(k=0; k < side; k++) {
        for(l=0; l < side; l++) {
          nextc = sys->cubes[i][j][k][l];
          if(nextc != NULL) {
            nextc->x = length * ((double) j + 0.5) + sys->minx;
            nextc->y = length * ((double) k + 0.5) + sys->miny;
            nextc->z = length * ((double) l + 0.5) + sys->minz;
            nextc->level = i;
            nextc->j = j;
            nextc->k = k;
            nextc->l = l;
          }
        }
      }
    }
  }
}

/*
Recursive routine to give indexes to the charges so that those in each 
cube are contiguous. In addition, insure that the charges in each parent 
at each level are numbered contiguously.  This is used to support a 
psuedo-adaptive scheme.  Also get the pointer to the appropriate section
of the charge and potential vector.  Uses the eval vector for the potential
coeffs at the lowest level.  Also index the lowest level cubes.
*/
static void indexkid(ssystem *sys, cube *dad, int *pqindex, int *pcindex)
{
  int i;
  
  if(dad != NULL) {
    if((dad->numkids == 0) && (dad->upnumvects > 0)) {
      dad->upvects = sys->heap.alloc<double*>(1, AMSC);
      dad->nbr_is_dummy = sys->heap.alloc<int*>(1, AMSC);
      dad->upvects[0] = &(sys->q[*pqindex]);
      dad->eval = &(sys->p[*pqindex]); /* changed from local to eval 17Feb90 */
      dad->nbr_is_dummy[0] = &(sys->is_dummy[*pqindex]);
      dad->is_dielec = &(sys->is_dielec[*pqindex]);
      dad->index = (*pcindex)++;
      for(i=0; i < dad->upnumeles[0]; i++) {
        (dad->chgs[i])->index = (*pqindex)++;
      }
    }
    else {
      for(i=0; i < dad->numkids; i++) {
        indexkid(sys, dad->kids[i], pqindex, pcindex);
      }
    }
  }
}


/* 
SetExact marks as exact those cubes containing fewer than numterms
number of charges.  If the number of charges in the kids is less than
numterms, the box is marked as exact and the charges are copied up.
In addition, the vector of local expansion coeffs is set to the
potential vector.  Otherwise, the number of nonzero kids is counted
and put in upnumvects as usual.  
*/
/* added 30Mar91: provisions for loc_exact and mul_exact */
void setExact(ssystem *sys, int numterms)
{
int i, j, k, l, m, n;
int side = sys->side;
int depth = sys->depth;
int numchgs, num_eval_pnts, first;
cube *nc, *nkid, *****cubes = sys->cubes;
int all_mul_exact, all_loc_exact, p, num_real_panels;

  for(i=depth; i > 0; i--, side /= 2) {
    for(j=0; j < side; j++) {
      for(k=0; k < side; k++) {
        for(l=0; l < side; l++) {
          nc = cubes[i][j][k][l];
          if(nc != NULL) {
            if(i == depth) {
              assert(nc->upnumvects != 0);
              /* count the number of true panels in this cube */
              num_real_panels = 0;
              for(p = 0; p < nc->upnumeles[0]; p++) {
                if(!nc->chgs[p]->dummy) num_real_panels++;
              }
              if(num_real_panels <= numterms) {
                nc->mul_exact = TRUE;
                nc->multisize = nc->upnumeles[0];
              }
              else {
                nc->mul_exact = FALSE;
                nc->multisize = multerms(sys->order);
              }
              if(nc->upnumeles[0] <= numterms) {
                nc->loc_exact = TRUE;
                nc->localsize = nc->upnumeles[0];
              }
              else {
                nc->loc_exact = FALSE;
                nc->localsize = multerms(sys->order); 
              }
            }
            else {  
              /* Count the number of charges and nonempty kids. */
              all_loc_exact = all_mul_exact = TRUE;
              num_eval_pnts = numchgs = nc->upnumvects = 0;
              for(m = 0; m < nc->numkids; m++) {
                nkid = nc->kids[m];
                if(nkid != NULL) {
                  nc->upnumvects += 1;
                  if(nkid->mul_exact == FALSE) all_mul_exact = FALSE;
                  else {
                    num_eval_pnts += nkid->upnumeles[0];
                    for(p = 0; p < nkid->upnumeles[0]; p++) {
                      if(!nkid->chgs[p]->dummy) numchgs++;
                    }
                  }
                  if(nkid->loc_exact == FALSE) all_loc_exact = FALSE;
                }
              }
              /* If all nonempty kids exact, # chgs <= # terms, mark exact, 
                 copy chgs, and promote pointers to charge and potential.  
                 Note EXPLOITS special ordering of the pot and charge vectors.
                 */
              if(!all_mul_exact || (numchgs > numterms)) { /* multi req'd */
                nc->mul_exact = FALSE;
                nc->multisize = multerms(sys->order);
              }
              else if(all_mul_exact && (numchgs <= numterms)) { 
                nc->mul_exact = TRUE;
                nc->upnumvects = 1;
                nc->upvects = sys->heap.alloc<double*>(1, AMSC);
                nc->upnumeles = sys->heap.alloc<int>(1, AMSC);
                nc->upnumeles[0] = num_eval_pnts; /* was numchgs 30Mar91 */
                nc->multisize = num_eval_pnts; /* was numchgs */
                nc->chgs = sys->heap.alloc<charge*>(num_eval_pnts, AMSC);
                num_eval_pnts = 0;
                for(m=0, first=TRUE; m < nc->numkids; m++) {
                  nkid = nc->kids[m]; 
                  if(nkid != NULL) {
                    if(first == TRUE) {
                      nc->upvects[0] = nkid->upvects[0];
                      if(nc->nbr_is_dummy == NULL)
                          nc->nbr_is_dummy = sys->heap.alloc<int*>(1, AMSC);
                      nc->nbr_is_dummy[0] = nkid->nbr_is_dummy[0];
                      first = FALSE;
                    }
                    for(n=0; n < nkid->upnumeles[0]; n++) {
                      nc->chgs[num_eval_pnts++] = nkid->chgs[n];
                    }
                  }
                }
              }

              /* do the same for local expansion */
              /* if local exact, must be multi exact => no promotion reqd */
              if(!all_loc_exact || (num_eval_pnts > numterms)) { /* le req'd */
                nc->loc_exact = FALSE;
                nc->localsize = multerms(sys->order);
              }
              else if(all_loc_exact && (num_eval_pnts <= numterms)) { 
                nc->loc_exact = TRUE;
                nc->localsize = num_eval_pnts;
              }
            }
          }
        }
      }
    }
  }
}


/*
Find all the nearest neighbors.
At the bottom level, get neighbors due to a parents being exact.
*/
static void getnbrs(ssystem *sys)
{
cube *nc, *np, *****cubes = sys->cubes;
int depth = sys->depth;
int i, j, k, l, m, n, p, side, es;
int numnbrs;

/* Return if depth = 0, no neighbors. */
  if(depth == 0) return;

/*
At the every level, get the nearest nbrs combined with nbrs due to parents
being exact.
*/
  /* exactness for local expansion is checked - nbrs used only in dwnwd pass */
  for(i = 1, side = 2; i <= depth; i++, side *= 2) {
    for(j=0; j < side; j++) {
      for(k=0; k < side; k++) {
        for(l=0; l < side; l++) {
          nc = cubes[i][j][k][l];
          if(nc != NULL) {
            /* Find sidelength of exact cube. */
            for(es=1, np=nc->parent; np->loc_exact==TRUE; 
                np = np->parent, es *= 2); /* exact -> loc_exact 1Apr91 */
          
            /* Stack up the nearest nbrs plus nbrs in exact cube. */
            numnbrs = 0;
            for(m = MIN((j-NNBRS), es * (j/es));
                m < MAX((j+NNBRS+1), es * (1 + (j / es))); m++) {
              for(n = MIN((k-NNBRS), es * (k/es));
                  n < MAX((k+NNBRS+1), es * (1 + (k/es))); n++) {
                for(p = MIN((l-NNBRS), es * (l/es));
                    p < MAX((l+NNBRS+1), es * (1+(l/es))); p++) {
                  if( (m >= 0) && (n >= 0) && (p >= 0)
                     && (m < side) && (n < side) && (p < side)
                     && ((m != j) || (n != k) || (p != l))
                     && (cubes[i][m][n][p] != NULL)) {
                    cstack[numnbrs++] = cubes[i][m][n][p];
                  }
                }
              }
            }
            nc->numnbrs = numnbrs;
            if(nc->numnbrs > 0)
              nc->nbrs = sys->heap.alloc<cube*>(numnbrs, AMSC);
            for(m=numnbrs-1; m >= 0; m--) nc->nbrs[m] = cstack[m];
          }
        }
      }
    }
  }
}

/*
  returns the number of charges in the lowest level cubes contained in "cp"
*/
static int cntDwnwdChg(cube *cp, int depth)
{
  int i;
  int cnt;

  if(cp->level == depth) return(cp->upnumeles[0]);
  else for(i = 0; i < cp->numkids; i++) 
      cnt += cntDwnwdChg(cp->kids[i], depth);
  return(cnt);
}

/* 
Set up the links between cubes requiring multi work on each level, one
for the cubes requiring local expansion work, one for the cubes requiring
direct methods and one for cubes with potential evaluation points. 
Note, upnumvects and exact must be set!!!
*/
static void linkcubes(ssystem *sys)
{
  cube *nc, **plnc, **pdnc, **pmnc, *****cubes = sys->cubes;
  int i, j, k, l;
  int dindex, side, depth=sys->depth, numterms=multerms(sys->order);

  /* Allocate the vector of heads of cubelists. */
  sys->multilist = sys->heap.alloc<cube*>(sys->depth+1, AMSC);
  sys->locallist = sys->heap.alloc<cube*>(sys->depth+1, AMSC);

  pdnc = &(sys->directlist);
  for(dindex = 1, i=0, side = 1; i <= sys->depth; i++, side *= 2) {
    pmnc = &(sys->multilist[i]);
    plnc = &(sys->locallist[i]);
    for(j=0; j < side; j++) {
      for(k=0; k < side; k++) {
        for(l=0; l < side; l++) {
          nc = cubes[i][j][k][l];
          if(nc != NULL) {
            /* Do the multi expansion if the cube is not treated exactly. */
            if(i > 1) {         /* no multis over the root cube and its kids */
              if(nc->mul_exact == FALSE) { /* exact -> mul_exact 1Apr91 */
                nc->multi = sys->heap.alloc<double>(numterms, AMSC);
                *pmnc = nc;
                pmnc = &(nc->mnext);
              }
            }
            
            /* Do the local expansion on a cube if it has chgs inside, and it's
             not exact and not the root (lev 0) nor one of its kids (lev 1). */
            if(i > 1) {         /* no locals with level 0 or 1 */
              if(nc->loc_exact == FALSE) { /* exact -> loc_exact 1Apr91 */
                *plnc = nc;
                plnc = &(nc->lnext);
                nc->local = sys->heap.alloc<double>(numterms, AMSC);
              }
            }

            /* Add to direct list if at bot level and not empty. */
            if(i == depth) { 
              *pdnc = nc;  /* For the direct piece, note an index. */
              pdnc = &(nc->dnext);
              nc->dindex = dindex++;
            }
          }
        }
      }
    }
  }
}

/*
Determine maximum number of chgs contained in a single cube.
*/
static void setMaxq(ssystem *sys)
{
  int i, j, k, l, side, p, kids_are_exact = FALSE, all_null = FALSE, depth = sys->depth;
  int mul_maxq, mul_maxlq, loc_maxq, loc_maxlq, num_chgs, real_panel_cnt = 0;
  cube *nc, *****cubes = sys->cubes;

  mul_maxq = mul_maxlq = loc_maxq = loc_maxlq = 0;
  for(i = 1, side = 2; i <= depth; i++, side *= 2) {
    for(j=0; j < side; j++) {
      for(k=0; k < side; k++) {
        for(l=0; l < side; l++) {
          nc = cubes[i][j][k][l];
          if(nc != NULL) {
            if(nc->mul_exact == TRUE) {
              num_chgs = 0;
              for(p = 0; p < nc->upnumeles[0]; p++) {
                if(!nc->nbr_is_dummy[0][p]) num_chgs++;
              }
              mul_maxq = MAX(mul_maxq, num_chgs);
              if(i == depth) mul_maxlq = MAX(mul_maxlq, num_chgs); 
            }
            if(nc->loc_exact == TRUE) {
              loc_maxq = MAX(loc_maxq, nc->upnumeles[0]);
              if(i == depth) loc_maxlq = MAX(loc_maxlq,nc->upnumeles[0]); 
            }
          }
        }
      }
    }
  }
  sys->loc_maxq = loc_maxq;     /* max evaluation points, over all loc_exact */
  sys->loc_maxlq = loc_maxlq;   /* max evaluation pnts, over lowest level */
  sys->mul_maxq = mul_maxq;     /* max panels, over all mul_exact cubes */
  sys->mul_maxlq = mul_maxlq;   /* max panels, over lowest level cubes */

  /* find the maximum #panels in all non-exact cubes w/exact (or no) kids */
  sys->max_panel = 0;
  for(j = 2; j <= depth; j++) {
    for(nc = sys->multilist[j]; nc != NULL; nc = nc->mnext) {
      if(nc->level == depth) {
        real_panel_cnt = 0;
        for(i = 0; i < nc->upnumeles[0]; i++) {
          if(!nc->nbr_is_dummy[0][i]) real_panel_cnt++;
        }
        sys->max_panel = MAX(sys->max_panel, real_panel_cnt);
      }
      else {
        kids_are_exact = all_null = TRUE;
        real_panel_cnt = 0;
        for(i = 0; i < nc->numkids && kids_are_exact; i++) {
          if(nc->kids[i] == NULL) continue;
          all_null = FALSE;
          if(!nc->kids[i]->mul_exact) kids_are_exact = FALSE;
          else {                /* count real panels */
            for(l = 0; l < nc->kids[i]->upnumeles[0]; l++) {
              if(!((nc->kids[i]->nbr_is_dummy[0])[l])) real_panel_cnt++;
            }
          }
        }
        if(kids_are_exact && !all_null) {
          sys->max_panel = MAX(sys->max_panel, real_panel_cnt);
        }
      }
    }
  }

  /* find the maximum #eval points in all non-exact cubes w/exact children */
  sys->max_eval_pnt = 0;
  for(j = 2; j <= depth; j++) {
    for(nc = sys->locallist[j]; nc != NULL; nc = nc->lnext) {
      if(nc->level == depth) {
        sys->max_eval_pnt = MAX(sys->max_eval_pnt, nc->upnumeles[0]);
      }
      else {
        kids_are_exact = all_null = TRUE;
        real_panel_cnt = 0;
        for(i = 0; i < nc->numkids && kids_are_exact; i++) {
          if(nc->kids[i] == NULL) continue;
          all_null = FALSE;
          if(!nc->kids[i]->loc_exact) kids_are_exact = FALSE;
          else real_panel_cnt += nc->kids[i]->upnumeles[0];
        }
      }
      if(kids_are_exact && !all_null)
          sys->max_eval_pnt = MAX(sys->max_eval_pnt, real_panel_cnt);
    }
  }
}

/* 
  markup sets the flag to "flag" in the child and its nearest nbrs
*/
static void markUp(cube *child, int flag)
{
  int i;

  child->flag = flag;
  for(i = 0; i < child->numnbrs; i++) {
    child->nbrs[i]->flag = flag;
  }
}

/* 
  forms the true interaction list (see also comment at mulMatEval())
   for cube "child", excluding only empty cubes
  -interaction list pointer is saved in the interList cube struct field
*/
static int getInter(ssystem *sys, cube *child)
{
  int i, j, vects, usekids, lc, jc, kc, ln, jn, kn;
  int numnbr = (child->parent)->numnbrs; /* number of neighbors */
  cube **nbrc = (child->parent)->nbrs; /* list of neighbor pointers */
  cube *sib;                    /* pointer to sibling (same level as child) */
  cube **pstack = &(cstack[0]); /* temporary storage pointer */

  /* mark the child cube and all its neighbors */
  markUp(child, TRUE);

  /* unmarked children of child's parent's neighbors become the ilist */
  for(i = 0; i < numnbr; i++) { /* loop on neighbors */
    /* Check nbr's kids for a marked kid. */
    for(usekids = FALSE, j = 0; j < nbrc[i]->numkids; j++) { 
      sib = (nbrc[i]->kids)[j];
      if((sib != NULL) && (sib->flag == TRUE)) { usekids = TRUE; break; };
    }
    /* Use nbr if no kids marked. */
    /* ...and it's really not a 1st nrst nbr of the parent 
       - this stops parent-sized cubes from getting into the ilist
         when they have empty child-sized cubes that are 2nd or 1st
         nrst nbrs of the child cube 
       - should work with NNBRS = 1 (never allows parent-sized in list)
         and NNBRS > 2 (but cannot allow greater than parent-sized)
       (29May90) */
#if ON == ON
    lc = (child->parent)->l;
    jc = (child->parent)->j;
    kc = (child->parent)->k;
    ln = nbrc[i]->l;
    jn = nbrc[i]->j;
    kn = nbrc[i]->k;
    if((RADINTER == ON) && (usekids == FALSE) &&
       ((lc-1 != ln && lc+1 != ln && lc != ln)
       || (jc-1 != jn && jc+1 != jn && jc != jn)
       || (kc-1 != kn && kc+1 != kn && kc != kn))) {  
      *pstack = nbrc[i];
      pstack++;
    }
#else                           /* USE THIS PART FOR TESTING ONLY */
    if(RADINTER && (usekids == FALSE)) { /* PRODUCES INCORRECT ILISTS!!! */
      *pstack = nbrc[i];
      pstack++;
    }
#endif
    else for(j = 0; j < nbrc[i]->numkids; j++) { /* use nbr's kids. */
      sib = (nbrc[i]->kids)[j]; /* get sib of child cube of interest */
      if((sib != NULL) && (sib->flag == FALSE)) { 
        *pstack = sib;
        pstack++;
      }
    }
  }

  /* clear all the flags */
  markUp(child, FALSE);

  /* allocate and save the interaction list */
  child->interSize = vects = pstack - &(cstack[0]);
  if(vects > 0)
    child->interList = sys->heap.alloc<cube *>(vects, AMSC);
  for(j = 0; j < vects; j++) child->interList[j] = cstack[j];

  return(vects);                /* return number of interaction elements */
}

/*
  generates explicit, true interaction lists for all non-empty cubes w/lev > 1
*/
static void getAllInter(ssystem *sys)
{
  int i, j, k, l, side, depth = sys->depth;
  cube *nc, *****cubes = sys->cubes;
  for(i = 2, side = 4; i <= depth; i++, side *= 2) {
    for(j=0; j < side; j++) {   /* loop through all cubes at levels > 1 */
      for(k=0; k < side; k++) {
        for(l=0; l < side; l++) {
          nc = cubes[i][j][k][l];
          if(nc != NULL) getInter(sys, nc);
        }
      }
    }
  }
}

/* 
  inits the dummy and dielec mask vectors; used to tell which entries to skip
  - mask vectors are redundant (could read flags in charge struct) 
  - done for speed in potential eval loop
*/
static void set_vector_masks(ssystem *sys)
{
  int i;
  cube *cp;

  for(cp = sys->directlist; cp != NULL; cp = cp->dnext) {
    for(i = 0; i < cp->upnumeles[0]; i++) {
      if(!(cp->nbr_is_dummy[0][i] = cp->chgs[i]->dummy))
          cp->is_dielec[i] = 
              (cp->chgs[i]->surf->type == DIELEC 
               || cp->chgs[i]->surf->type == BOTH);
    }
  }

}





