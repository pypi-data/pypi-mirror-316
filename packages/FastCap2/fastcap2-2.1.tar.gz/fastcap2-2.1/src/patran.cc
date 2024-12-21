
/**************************************************************************

  This is the subroutine that handles PATRAN to FastCap interface.  
  Patfront returns a pointer to a linked list of charge structures.

  Written by Songmin Kim, July 24, 1990.

**************************************************************************/
#include "mulGlobal.h"
#include "mulStruct.h"
#include "quickif.h"
#include "patran_f.h"
#include "quickif.h"
#include "patran.h"
#include "vector.h"
#include "matrix.h"

#include <cstring>
#include <cmath>

static void input(ssystem *sys, FILE *stream, char *line, int surf_type, const Matrix3d &rot, const Vector3d &trans, char **title);
static void grid_equiv_check(ssystem *sys);
static void fill_patch_patch_table(ssystem *sys, int *patch_patch_table);
static void assign_conductor(ssystem *sys, int *patch_patch_table);
static void assign_names(ssystem *sys);
static void file_title(ssystem *sys, FILE *stream, char **title);
static void summary_data(ssystem *sys, FILE *stream);
static void node_data(ssystem *sys, FILE *stream, const Matrix3d &rot, const Vector3d &trans);
static void element_data(ssystem *sys, FILE *stream);
static void grid_data(ssystem *sys, FILE *stream, const Matrix3d &rot, const Vector3d &trans);
static void patch_data(ssystem *sys, FILE *stream);
static void CFEG_table(ssystem *sys, FILE *stream);
static void waste_line(int num_line, FILE *stream);
static void name_data(ssystem *sys, FILE *stream);
static int if_same_coord(double coord_1[3], double coord_2[3]);
static int if_same_grid(int ID, GRID *grid_ptr);
static void depth_search(ssystem *sys, int *patch_patch_table, int *current_table_ptr, int conductor_count);
static charge *make_charges_all_patches(ssystem *sys, int surf_type, const char *name_suffix);
static charge *make_charges_patch(ssystem *sys, int NELS, int *element_list, int conductor_ID);
static char *delcr(char *str);

#define BIG 35000              /* Size of element and node serach table. */
#define SMALL_NUMBER 0.005     /* See functions if_same_coord() and 
                                 grid_equiv_check(). */

charge *patfront(ssystem *sys, FILE *stream, const char *header, int surf_type, const Matrix3d &rot, const Vector3d &trans,
                 const char *name_suffix, char **title)
{
  int *patch_patch_table;

  char line[BUFSIZ];
  strncpy(line, header, sizeof(line));

  sys->pts.start_name_this_time = NULL;
  sys->pts.first_grid = sys->pts.first_patch = sys->pts.first_cfeg = TRUE;
  sys->pts.number_grids = sys->pts.number_patches = 0;

  if (!sys->pts.element_search_table) {
    sys->pts.element_search_table = sys->heap.alloc<ELEMENT *>(BIG);
  }
  if (!sys->pts.node_search_table) {
    sys->pts.node_search_table = sys->heap.alloc<NODE *>(BIG);
  }

  input(sys, stream, line, surf_type, rot, trans, title);

  grid_equiv_check(sys);

  /*********************************************************************
    This section of patfront is for assigning conductor numbers to patches
    depending on their connectivity.                                    */

  if(surf_type == CONDTR || surf_type == BOTH) {

    patch_patch_table = sys->heap.alloc<int>(sys->pts.number_patches*sys->pts.number_patches, AMSC);

    fill_patch_patch_table(sys, patch_patch_table);

    assign_conductor(sys, patch_patch_table);

  /*********************************************************************/

    assign_names(sys);
  }

  return make_charges_all_patches(sys, surf_type, name_suffix);
}


/****************************************************************************
 
  This part of code is for reading in Patran Neutral files.

****************************************************************************/

void input(ssystem *sys, FILE *stream, char *line, int surf_type, const Matrix3d &rot, const Vector3d &trans, char **title)
{
  int END=0;

  /* Reads in the first line from each card, and branch off.  ID, IV, KC, 
     N1, N2, N3, N4 and N5 are global variables accessible by subroutines. */

  int type_number = 0;

  while (!END) {
    if(line[0] == '2') {        /* if first line */
      sscanf(line,"%d %d %d %d %d %d %d %d %d", 
           &type_number, &sys->pts.ID, &sys->pts.IV, &sys->pts.KC, &sys->pts.N1, &sys->pts.N2, &sys->pts.N3, &sys->pts.N4, &sys->pts.N5);
      line[0] = '0';
    }
    else fscanf(stream,"%d %d %d %d %d %d %d %d %d", 
                &type_number, &sys->pts.ID, &sys->pts.IV, &sys->pts.KC, &sys->pts.N1, &sys->pts.N2, &sys->pts.N3, &sys->pts.N4, &sys->pts.N5);
      

    switch (type_number) {
    case 25:
      file_title(sys, stream, title);
      break;
    case 26:
      summary_data(sys, stream);
      break;
    case 1:
      node_data(sys, stream, rot, trans);
      break;
    case 2:
      element_data(sys, stream);
      break;
    case 31:
      grid_data(sys, stream, rot, trans);
      break;
    case 33:
      patch_data(sys, stream);
      break;
    case 45:
      CFEG_table(sys, stream);
      break;
    case 21:
      if(surf_type == CONDTR || surf_type == BOTH) name_data(sys, stream);
      else waste_line(sys->pts.KC, stream);
      break;
    case 99:
      END = 1;
      break;
    default:
      waste_line(sys->pts.KC,stream);
      break;
    }
  }
}

/* Simply read in 'num_line' lines from stream and dump. */

void waste_line(int num_line, FILE *stream)
{
  int c, tmp;
  tmp=num_line+1;
  while (tmp) {
    c=getc(stream);
    if (c=='\n') tmp--;}
}


/* Save the title of the Neutral file. */

void file_title(ssystem *sys, FILE *stream, char **title)
{
  char line[BUFSIZ];
  
  fgets(line, sizeof(line), stream);
  *title = sys->heap.strdup(delcr(line));
}


/* Since the summary card has informations on the number of elements and 
   nodes, this function allocates spaces for nodes and elements, and sets up
   the global pointers to these arrays. */

void summary_data(ssystem *sys, FILE *stream)
{
  sys->pts.number_nodes = sys->pts.N1; sys->pts.number_elements = sys->pts.N2;

  sys->pts.list_nodes = sys->heap.alloc<NODE>(sys->pts.number_nodes, AMSC);
  sys->pts.list_elements = sys->heap.alloc<ELEMENT>(sys->pts.number_elements, AMSC);

  sys->pts.current_node = sys->pts.list_nodes;
  sys->pts.current_element = sys->pts.list_elements;

  waste_line(1,stream); 
}


/* Current_node is the global variable that points to the next entry in 
   node array, list_nodes, which is preallocated by summary_data function. 
   Node_search_table is sorted by node ID to make indexing of a node easier. */

void node_data(ssystem *sys, FILE *stream, const Matrix3d &rot, const Vector3d &trans)
{
  double tmp_coord[3];

  fscanf(stream,"%lf %lf %lf",tmp_coord,tmp_coord+1,tmp_coord+2);  
  waste_line(1,stream);

  Vector3d new_coord = rot * Vector3d(tmp_coord) + trans;
  new_coord.store(sys->pts.current_node->coord);
  sys->pts.node_search_table[sys->pts.ID] = sys->pts.current_node;
  sys->pts.current_node++;
}


/* Current_element is the global variable that points to the next entry in 
   element array, list_elements, which is preallocated by summary_data
   function.  Element_search_table is sorted by element ID to make indexing 
   of an element easier.  */

void element_data(ssystem *sys, FILE *stream)
{
  int num_nodes, corner[4], i, tmp;
  float tmp1;

  sys->pts.current_element->shape = sys->pts.IV;

  if ((sys->pts.IV != 3) && (sys->pts.IV != 4)) waste_line(sys->pts.KC,stream);
  else {
    fscanf(stream,"%d %d %d %d %f %f %f",
           &num_nodes,&tmp,&tmp,&tmp,&tmp1,&tmp1,&tmp1); 
    sys->pts.current_element->num_nodes = num_nodes;
    
    /* IV==3 and 4 imply triangular and quad elements, respectively. */
    if (sys->pts.IV==3) fscanf(stream,"%d %d %d",corner,corner+1,corner+2);
    else fscanf(stream,"%d %d %d %d",corner,corner+1,corner+2,corner+3);
    
    for (i=0; i<num_nodes; i++) {
      sys->pts.current_element->corner[i] = corner[i];
    }
    sys->pts.element_search_table[sys->pts.ID] = sys->pts.current_element;
    sys->pts.current_element++;
  
    if (sys->pts.N1) waste_line(1,stream);
  }
}

/* Grid data are linked together by next and prev pointers within GRID 
   structure.  Start_grid is the global variable that points to the very 
   first GRID structure created.  */

void grid_data(ssystem *sys, FILE *stream, const Matrix3d &rot, const Vector3d &trans)
{
  static GRID *prev_grid=0;
  GRID *current_grid;
  double coord[3];

  if(sys->pts.first_grid) {
    prev_grid = NULL;
    sys->pts.first_grid = FALSE;
  }

  current_grid = sys->heap.alloc<GRID>(1, AMSC);
  if (sys->pts.number_grids==0) sys->pts.start_grid=current_grid;
  current_grid->ID = sys->pts.ID;
  current_grid->prev = prev_grid;
  if (prev_grid) prev_grid->next = current_grid;

  fscanf(stream, "%lf %lf %lf", coord, coord+1, coord+2);
  Vector3d new_coord = rot * Vector3d(coord) + trans;
  new_coord.store(current_grid->coord);
  prev_grid = current_grid;    
  current_grid->next=0;
  sys->pts.number_grids++;
}


/* Patch data are linked together by next and prev pointers within PATCH 
   structure.  Start_patch is the global variable that points to the very 
   first PATCH structure created.  */

void patch_data(ssystem *sys, FILE *stream)
{
  static PATCH *prev_patch=0;
  PATCH *current_patch;
  double tmp;
  int i, corner[4];

  if(sys->pts.first_patch) {
    prev_patch = NULL;
    sys->pts.first_patch = FALSE;
  }

  current_patch = sys->heap.alloc<PATCH>(1, AMSC);
  if (sys->pts.number_patches==0) sys->pts.start_patch=current_patch;
  current_patch->ID = sys->pts.ID;
  current_patch->prev = prev_patch;
  if (prev_patch) prev_patch->next = current_patch;

  waste_line(9,stream);
  fscanf(stream, "%lg %lg %lg %d %d %d %d",
         &tmp, &tmp, &tmp, corner, corner+1, corner+2, corner+3);
  for (i=0; i<4; i++) current_patch->corner[i] = corner[i];
  prev_patch = current_patch;
  current_patch->next=0;
  sys->pts.number_patches++;
}


/* CFEG data are linked together with next and prev pointers within CFEG 
   structure.  Start_cfeg is the global variable that points to the very
   first CFEG structure created.  CFEG table has the result from meshing 
   a patch. */

void CFEG_table(ssystem *sys, FILE *stream)
{
  static CFEG *prev_cfeg=0;
  CFEG *current_cfeg;
  int tmp, NELS, LPH, LPH_ID, LSHAPE, NDIM, NODES, ICONF;
  int i, *element_list, element_num1, element_num2;

  if(sys->pts.first_cfeg) {
    prev_cfeg = NULL;
    sys->pts.first_cfeg = FALSE;
  }

  waste_line(1,stream);
  fscanf(stream,"%d %d %d %d %d %d %d %d", 
         &NDIM, &LSHAPE, &NODES, &ICONF, &LPH, &LPH_ID, &tmp, &tmp);

  if (LPH != 3) waste_line(sys->pts.KC-2,stream);
  else {
    current_cfeg = sys->heap.alloc<CFEG>(1, AMSC);
    if (!prev_cfeg) sys->pts.start_cfeg=current_cfeg;
    current_cfeg->ID = sys->pts.ID;
    current_cfeg->NELS = sys->pts.IV; NELS = sys->pts.IV;
    current_cfeg->prev = prev_cfeg;
    if (prev_cfeg) prev_cfeg->next = current_cfeg;
    
    /* This is the list of elements associated with this particular patch. */
    element_list = sys->heap.alloc<int>(NELS, AMSC);
    current_cfeg->element_list = element_list;
        
    current_cfeg->LPH = LPH;             
    current_cfeg->LPH_ID = LPH_ID;
    current_cfeg->LSHAPE = LSHAPE;
    current_cfeg->NDIM = NDIM;
    current_cfeg->NODES = NODES;
    current_cfeg->ICONF = ICONF;
    
    if (LSHAPE==3) {                  /* Triangular elements. */
      for (i=1; i<=NELS/2; i++) {
        fscanf(stream, "%d %d %d %d %d %d %d %d %d %d", 
          &tmp,&tmp,&tmp,&tmp,&element_num1,&tmp,&tmp,&tmp,&tmp,&element_num2);
        *element_list++ = element_num1;
        *element_list++ = element_num2;
      }
      if (NELS%2) {
        fscanf(stream, "%d %d %d %d %d",&tmp,&tmp,&tmp,&tmp,&element_num1);
        *element_list++ = element_num1;
      }
    }
    else if (LSHAPE==4) {             /* Quad elements. */
      for (i=1; i<=NELS/2; i++) {
        fscanf(stream, "%d %d %d %d %d %d %d %d %d %d", 
          &tmp,&tmp,&tmp,&tmp,&element_num1,&tmp,&tmp,&tmp,&tmp,&element_num2);
        *element_list++ = element_num1;
        *element_list++ = element_num2;
      }
      if (NELS%2) {
        fscanf(stream, "%d %d %d %d %d",&tmp,&tmp,&tmp,&tmp,&element_num1);
        *element_list++ = element_num1;
      }
    }
    prev_cfeg = current_cfeg;
  }
}

/*
  reads in name data cards and puts information into NAME struct linked list
  - for every component (each must contain at least 1 conductor surface patch)
    stores the component name and patch ID numbers in that component
  - later Song's patch list is used in assign_names() to set the patch 
    conductor ID numbers
  - the output routine looks at the first sm_patch struct associated with
    each NAME struct to determine the number of the corresponding cond name
*/
void name_data(ssystem *sys, FILE *stream)
{
  int iv, i, j, ntype, id, patch_cnt = 0;
  char line[BUFSIZ];
  SM_PATCH *current_patch = NULL;

  if(sys->pts.start_name == NULL) { /* if first time on first patfront() call */
    sys->pts.start_name = sys->heap.alloc<NAME>(1, AMSC);
    sys->pts.current_name = sys->pts.start_name_this_time = sys->pts.start_name;
  }
  else{ 
    sys->pts.current_name->next = sys->heap.alloc<NAME>(1, AMSC);
    sys->pts.current_name = sys->pts.current_name->next;
    if(sys->pts.start_name_this_time == NULL) {     /* if 1st time on this patfront call */
      sys->pts.start_name_this_time = sys->pts.current_name;
    }
  }

  /* get conductor name and store */
  fgets(line, sizeof(line), stream); /* eat CR */
  fgets(line, sizeof(line), stream);
  delcr(line);
  sys->pts.current_name->name = sys->heap.strdup(line);
  
  /* input NTYPE ID pair lines until no more, save patch id's that come in */
  for(i = iv = 0; i < sys->pts.KC-1; i++) {      /* loop on lines */
    for(j = 0; j < 5 && iv < sys->pts.IV/2; j++, iv++) { /* loop on items */
      fscanf(stream, "%d %d", &ntype, &id);
      if(ntype == 3) {          /* if its a patch, save ID */
        if(current_patch == NULL) { /* if 1st patch */
          sys->pts.current_name->patch_list = sys->heap.alloc<SM_PATCH>(1, AMSC);
          current_patch = sys->pts.current_name->patch_list;
        }
        else {
          current_patch->next = sys->heap.alloc<SM_PATCH>(1, AMSC);
          current_patch = current_patch->next;
        }
        current_patch->ID = id;
        patch_cnt++;
      }
    }
  }
  if(patch_cnt == 0) {
    sys->error("name_data: conductor '%s'\n  has no patch - redo naming so that one is included.",
               sys->pts.current_name->name);
  }
}

/* This function checks for coordinate-wise equivalent grid points.  Each 
   grid structure has a list of equivalent grids.  If all three coordinates
   from two grid points are within SMALL_NUMBER, defined in patran.h, then 
   they are equivalent.  */

static void grid_equiv_check(ssystem *sys)
{
  GRID *grid_ptr_1, *grid_ptr_2;

  /* First, allocate spaces for equivalent grid arrays. */
  grid_ptr_1 = sys->pts.start_grid;
  while (grid_ptr_1) {
    grid_ptr_1->equiv_ID = sys->heap.alloc<int>(sys->pts.number_grids, AMSC);
    grid_ptr_1->number_equiv_grids = 0;
    grid_ptr_1 = grid_ptr_1->next;
  }

  /* Begin search.  Grid N is compared with grids from N+1 through the end 
     of the list.  */
  grid_ptr_1 = sys->pts.start_grid;
  while (grid_ptr_1) {
    grid_ptr_2 = grid_ptr_1->next;
    while (grid_ptr_2) {
      if (if_same_coord(grid_ptr_1->coord,grid_ptr_2->coord)) {
        *(grid_ptr_1->equiv_ID + grid_ptr_1->number_equiv_grids)
          = grid_ptr_2->ID;
        *(grid_ptr_2->equiv_ID + grid_ptr_2->number_equiv_grids)
          = grid_ptr_1->ID;
        (grid_ptr_1->number_equiv_grids)++;
        (grid_ptr_2->number_equiv_grids)++;
      }
      grid_ptr_2 = grid_ptr_2->next;
    }
    grid_ptr_1 = grid_ptr_1->next;
  }

  /* Print the equivalent grid information. 
  grid_ptr_1 = start_grid;
  while (grid_ptr_1) {
    sys->msg("\nGrid %d : (%d)", grid_ptr_1->ID, grid_ptr_1->number_equiv_grids);
    for (i=0; i<grid_ptr_1->number_equiv_grids; i++) 
      sys->msg (" %d ", *(grid_ptr_1->equiv_ID+i));
    grid_ptr_1 = grid_ptr_1->next;
  } */
}


int if_same_coord(double coord_1[3], double coord_2[3])
{
  int i;

  for (i=0; i<3; i++) 
    if (fabs(coord_1[i] - coord_2[i]) > SMALL_NUMBER) return 0;
  return 1;
}

/*
  makes 1st \n in a string = \0 and then deletes all trail/leading wh space
*/
static char *delcr(char *str)
{
  int i, j, k;
  for(k = 0; str[k] != '\0'; k++) if(str[k] == '\n') { str[k] = '\0'; break; }
  for(i = 0; str[i] == ' ' || str[i] == '\t'; i++); /* count leading spaces */
  if(i > 0) {
    for(j = 0; str[j+i] != '\0'; j++) str[j] = str[j+i];
    str[j] = '\0';
  }
  for(k--; str[k] == ' ' || str[k] == '\t'; k--) str[k] = '\0';
  return(str);
}

/****************************************************************************

  This section of code is responsible for assigning conductor numbers to
  all the patches.

****************************************************************************/

/* This function fills the table that shows the connectivity of patches.
   If two patches share at least one common corner point, then they are 
   connected.  It is done by going through all the grid points and finding 
   patches that are connected by the grid point.  The end result table is
   symmetric.  */   

void fill_patch_patch_table(ssystem *sys, int *patch_patch_table)
{
  int patch_count, patch_count_save, *current_table_ptr, *corner, i;
  GRID *grid_ptr;
  PATCH *patch_ptr;

  grid_ptr = sys->pts.start_grid;
  while (grid_ptr) {
    
    /* Patch_count is generic counter of current position in the patch array,
       start_patch.  Patch_count_save is index of the last patch that had 
       the current grid as its corner.  */
    patch_count = 0;
    patch_count_save = 0;
    current_table_ptr = 0;
    patch_ptr = sys->pts.start_patch;

    while (patch_ptr) {
      corner = patch_ptr->corner;
      for (i=0; i<4; i++) 
        if (if_same_grid(*corner++,grid_ptr)) {
          if (current_table_ptr) {  /* Have we already found another patch 
                                       with the same grid as its corner?  */
            *(current_table_ptr+patch_count)=1;
            *(patch_patch_table + (patch_count * sys->pts.number_patches)
              + patch_count_save)=1;
          }
          current_table_ptr = patch_patch_table + patch_count*sys->pts.number_patches;
          patch_count_save = patch_count;
        }
      patch_ptr = patch_ptr->next;
      patch_count++;
    }
    grid_ptr = grid_ptr->next;
  }
}


/* Return 1 if ID matches grid_ptr's ID or IDs of its equivalent grids, 
   and 0 otherwise. */

int if_same_grid(int ID, GRID *grid_ptr)
{
  int *equiv_ID, i;

  if ((grid_ptr->ID)==ID) return 1;
  else {
    equiv_ID = grid_ptr->equiv_ID;
    for (i=0; i<grid_ptr->number_equiv_grids; i++) 
      if (ID == equiv_ID[i]) return 1;
    return 0;
  }
}


/* This function searches through the patch_patch_table and finds groups of
   patches that are connected only among themselves. */

void assign_conductor(ssystem *sys, int *patch_patch_table)
{
  PATCH *patch_ptr;
  int patch_count=0, *current_table_ptr;

  sys->pts.conductor_count=1;

  /* Sets all the patches to conductor 0, meaning that it is yet to be 
     assigned a conductor_ID.  */
  patch_ptr = sys->pts.start_patch;
  while (patch_ptr) {
    patch_ptr->conductor_ID = 0;
    patch_ptr = patch_ptr->next;
  }

  /* Current_table_ptr points the row that needs to be searched through. 
     That row is associated with the current patch in need of a conductor
     number.  */
  current_table_ptr = patch_patch_table;
  patch_ptr = sys->pts.start_patch;
  while (patch_ptr) {
    if ((patch_ptr->conductor_ID) == 0) {  /* If the patch is not assigned 
                                              a conductor number. */
      patch_ptr->conductor_ID = sys->pts.conductor_count;
      depth_search(sys,patch_patch_table,current_table_ptr,sys->pts.conductor_count);
      sys->pts.conductor_count++;
    }
    patch_count++;
    current_table_ptr = patch_patch_table + patch_count*sys->pts.number_patches;
    patch_ptr = patch_ptr->next;
  }

  /* Prints the conductor information.
  patch_ptr = start_patch;
  while (patch_ptr) {
    sys->msg("\nPatch %d   Conductor %d",
           patch_ptr->ID, patch_ptr->conductor_ID);
    patch_ptr = patch_ptr->next;
  } */
}


/* This function searches through patch_patch_table recursively to
   find all patches that are somehow connected the current patch. */

void depth_search(ssystem *sys, int *patch_patch_table,int *current_table_ptr,int conductor_count)
{
  PATCH *patch_ptr;
  int i, *new_table_ptr;

  patch_ptr=sys->pts.start_patch;
  new_table_ptr=patch_patch_table;
  for (i=0; i<sys->pts.number_patches; i++) {
    if ((*(current_table_ptr+i)) != 0) {  /* If the current patch is connected
                                             to i'th patch. */
      if (patch_ptr->conductor_ID == 0) {  /* If the patch is yet to be 
                                              assigned a conductor number. */
        patch_ptr -> conductor_ID = conductor_count;
        new_table_ptr = patch_patch_table+i*sys->pts.number_patches;

        /* Call depth_search recursively to continue searching for 
           connected patches. */
        depth_search(sys,patch_patch_table,new_table_ptr,sys->pts.conductor_count);
      }
    }
    patch_ptr=patch_ptr->next;
  }
}

/*
  used with new naming functions---finds the patran name in the patran list
  - this code used to be in mksCapDump()
*/
static char *getPatranName(ssystem *sys, int cond_num)
{
  NAME *cname;

  cname = sys->pts.start_name_this_time;
  while(cname != NULL) {
    if((cname->patch_list)->conductor_ID == cond_num) return(cname->name);
    else cname = cname->next;
  }

  sys->msg("getPatranName: conductor %d has no name\n", cond_num);
  return(NULL);

}

/****************************************************************************

  The following functions create the linked list of charges that can be 
  used in Keith's FastCap program.

****************************************************************************/

charge *make_charges_all_patches(ssystem *sys, int surf_type, const char *name_suffix)
/* int *num_cond: master conductor counter */
{
  CFEG *cfeg_ptr;
  int NELS, LPH_ID, conductor_ID = 0, *element_list;
  char cond_name[BUFSIZ];
  PATCH *patch_ptr;
  charge *first_pq = 0, *current_pq = 0;

  cfeg_ptr = sys->pts.start_cfeg;
  while (cfeg_ptr) {
    if (cfeg_ptr->LPH == 3) {
      NELS = cfeg_ptr->NELS;
      LPH_ID = cfeg_ptr->LPH_ID;

      /* Find the patch structure that is associated with the current cfeg
         pointer in order to find the conductor number. */
      patch_ptr = sys->pts.start_patch;
      while (patch_ptr) {
        if (patch_ptr->ID == LPH_ID) {
          if(surf_type == CONDTR || surf_type == BOTH) {
            strcpy(cond_name, getPatranName(sys, patch_ptr->conductor_ID));
            strcat(cond_name, name_suffix);
            conductor_ID = sys->get_conductor_number(cond_name);
          }
          else conductor_ID = 0;
          break;
        }
        patch_ptr = patch_ptr->next;
      }
/*      sys->msg("\nCEFG %d  LPH %d LPH_ID %d Conductor_ID %d",
             cfeg_ptr->ID,cfeg_ptr->LPH,cfeg_ptr->LPH_ID,conductor_ID); */

      /* For each patch, call the subroutine to handle the detail. 
         Make sure all the lists of charges are linked. */
      element_list = cfeg_ptr->element_list;
      if (!first_pq) {
        first_pq = make_charges_patch(sys, NELS, element_list, conductor_ID);
        current_pq = first_pq + NELS - 1;
      }
      else {
        current_pq->next = 
          make_charges_patch(sys, NELS, element_list, conductor_ID);
        current_pq = (current_pq->next) + NELS - 1;
      } 
    }
    cfeg_ptr=cfeg_ptr->next;
  }
  /* Put a nil pointer at the end.  */
  current_pq->next = 0;
  return first_pq;
}


/* This function creates the linked list of charges for a single patch. */

charge *make_charges_patch(ssystem *sys, int NELS, int *element_list, int conductor_ID)
{
  charge *pq, *current_pq;
  int i,element_number,*element_corner_ptr;
  ELEMENT *element_ptr;
  NODE *node_ptr;

  pq = sys->heap.alloc<charge>(NELS, AMSC);

  /* Make sure that they are linked. */
  current_pq = pq;
  for (i=0; i<NELS-1; i++) {
    current_pq = pq + i;
    current_pq->next = current_pq+1;
  }

  /* NELS stands for number of elements. */
  for (i=0; i<NELS; i++) {
    (pq+i)->cond = conductor_ID;
    
    /* Original element number in Neutral file can be a negative number.  */
    if ((element_number= *(element_list+i))<0) element_number= -element_number;
    element_ptr = sys->pts.element_search_table[element_number];
    element_corner_ptr = element_ptr->corner;
    
    /* Pointers to the corner points' coordinates are set.  */

    if ((element_ptr->shape) == 4) {  /* Quadrilateral panels. */
      (pq+i)->shape = 4;
      node_ptr = sys->pts.node_search_table[*(element_corner_ptr++)];
      VCOPY((pq+i)->corner[0], node_ptr->coord);
      node_ptr = sys->pts.node_search_table[*(element_corner_ptr++)];
      VCOPY((pq+i)->corner[1], node_ptr->coord);
      node_ptr = sys->pts.node_search_table[*(element_corner_ptr++)];
      VCOPY((pq+i)->corner[2], node_ptr->coord);
      node_ptr = sys->pts.node_search_table[*(element_corner_ptr++)];
      VCOPY((pq+i)->corner[3], node_ptr->coord);
    }
    else {  /* Triangular panels. */
/*sys->msg("\nTTT\n");*/
      (pq+i)->shape = 3;
      node_ptr = sys->pts.node_search_table[*(element_corner_ptr++)];
      VCOPY((pq+i)->corner[0], node_ptr->coord);
      node_ptr = sys->pts.node_search_table[*(element_corner_ptr++)];
      VCOPY((pq+i)->corner[1], node_ptr->coord);
      node_ptr = sys->pts.node_search_table[*(element_corner_ptr++)];
      VCOPY((pq+i)->corner[2], node_ptr->coord);
    }
  }
  return pq;
}


/* 
  assigns correct conductor number to all patches in name structs
  - really already done implicitly in name_data by setting up sm_patch lists
  - conductor_ID of first patch is used as the number associated w/the name
  - checks for no names and names including several conductor's panels
  - checks one linked list against another, potentially n^2 => named
    regions should be kept small (as few patches as possible)
*/
static void assign_names(ssystem *sys)
{
  int quit, current_conductor, cnt = 0;
  PATCH *current_patch;
  SM_PATCH *current_name_patch;
  NAME *cur_name = sys->pts.start_name_this_time;

  if(sys->pts.start_name_this_time == NULL) {
    sys->error("assign_names: no conductor names specified");
  }

  /* for each name struct, find cond no of each patch (can be n^2 loop) */
  while(cur_name != NULL) {
    current_name_patch = cur_name->patch_list;
    current_conductor = 0;
    while(current_name_patch != NULL) {
      current_patch = sys->pts.start_patch;
      quit = 0;
      while(current_patch != NULL && quit == 0) {
        if(current_patch->ID == current_name_patch->ID) {
          current_name_patch->conductor_ID = current_patch->conductor_ID;
          if(current_conductor == 0) { /* if this is 1st name struct patch */
            current_conductor = current_patch->conductor_ID;
          }
          else if(current_conductor != current_patch->conductor_ID) {
            sys->error("assign_names: alleged conductor '%s'\n  has patches from more than one conductor - rename more carefully", cur_name->name);
          }
          quit = 1;
        }
        current_patch = current_patch->next;
      }
      if(quit == 0) {
        sys->error("assign_names: in conductor '%s'\n  can't find named patch in master list", cur_name->name);
      }
      current_name_patch = current_name_patch->next;
    }
    cur_name = cur_name->next;
    cnt++;
  }

  /* check to see if all conductors have a name and if too many names */
  if(cnt < sys->pts.conductor_count - 1) {
    sys->error("assign_names: %d conductors have no names",
               sys->pts.conductor_count - 1 - cnt);
  }
  if(cnt > sys->pts.conductor_count - 1) {
    sys->error("assign_names: %d names given for %d conductors",
               cnt, sys->pts.conductor_count - 1);
  }

}
