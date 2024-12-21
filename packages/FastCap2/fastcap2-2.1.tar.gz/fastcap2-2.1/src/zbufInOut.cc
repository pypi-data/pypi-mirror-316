
#include "mulGlobal.h"
#include "mulStruct.h"
#include "zbufGlobal.h"
#include "zbufInOut.h"
#include "zbufSort.h"
#include "input.h"

#include <cstring>
#include <cmath>
#include <algorithm>

/*
  loads axes' lines
*/
static void setupLine(double ***axi, int index, double x1, double y1, double z1, double x2, double y2, double z2)
{
  axi[index][0][0] = x1;
  axi[index][0][1] = y1;
  axi[index][0][2] = z1;
  axi[index][1][0] = x2;
  axi[index][1][1] = y2;
  axi[index][1][2] = z2;
}

/*
  set the grey levels taking into account the rd_, rc_, and rb_ options
  - levels are scaled to match the range of densities present
  - sets the values of the extremal densities (`black' and `white')
*/
static void figure_grey_levels(ssystem *sys, face **face_list, double *chgs, charge *chglist, int use_density, double *black, double *white)
{
  int first, i;
  charge *panel;

  /* find the minimum and maximum charge density values */
  first = TRUE;
  for(panel = chglist; panel != NULL; panel = panel->next) {
    if(panel->dummy) continue;

    /* skip if panel is on conductor in q picture kill list */
    if(panel->surf->type == CONDTR || panel->surf->type == BOTH) {
      if(sys->kq_num_list.find(panel->cond) == sys->kq_num_list.end()) continue;
    }

    /* skip if removing DIELEC's and panel is on dielectric i/f
       - type both interfaces are considered conductors for removal purposes */
    if(panel->surf->type == DIELEC && sys->rd_) continue;

    if(first == TRUE) {
      first = FALSE;
      if(use_density) *black = *white = chgs[panel->index]/panel->area;
      else *black = *white = chgs[panel->index];
    }
    else {
      if(use_density) {
        *black = std::max(*black, chgs[panel->index]/panel->area);
        *white = std::min(*white, chgs[panel->index]/panel->area);
      }
      else {
        *black = std::max(*black, chgs[panel->index]);
        *white = std::min(*white, chgs[panel->index]);
      }   
    }

  }

  /* assign the grey levels - 0.0 = white, 1.0 = black */
  double dif = *black - *white;
  for(panel = chglist, i = 0; panel != NULL; panel = panel->next) {
    if(panel->dummy) continue;

    /* skip if panel is on conductor in q picture kill list */
    if(panel->surf->type == CONDTR || panel->surf->type == BOTH) {
      if(sys->kq_num_list.find(panel->cond) == sys->kq_num_list.end()) continue;
    }

    /* skip if removing DIELEC's and panel is on dielectric i/f
       - type both interfaces are considered conductors for removal purposes */
    if(panel->surf->type == DIELEC && sys->rd_) continue;

    if(use_density)
        face_list[i]->greylev = (chgs[panel->index]/panel->area - *white)/dif;
    else face_list[i]->greylev = (chgs[panel->index] - *white)/dif;
    i++;
  }
}

/*
  figures the corner coordinates in absolute coordinates
*/
static void getAbsCoord(double *vec, charge *panel, int num)
{
  double *cor = panel->corner[num];
  double *x = panel->X, *y = panel->Y, *z = panel->Z;

  vec[0] = panel->x + cor[0]*x[0] + cor[1]*y[0] + cor[2]*z[0];
  vec[1] = panel->y + cor[0]*x[1] + cor[1]*y[1] + cor[2]*z[1];
  vec[2] = panel->z + cor[0]*x[2] + cor[1]*y[2] + cor[2]*z[2];
}
  
/*
  transfer fastcap panel info to face structs
*/
face **fastcap2faces(ssystem *sys, int *numfaces, charge *chglist, double *q, int use_density, double *black, double *white)
/* int use_density: use_density = TRUE => use q/A not q */
{
  int i;
  charge *chgp;
  face *head, *tail, **faces;
  double ***axes = sys->axes;
  double axeslen = sys->axeslen;

  /* transfer info to face structs (a waste but saves wrtting new fnt end) */
  for(chgp = chglist, head = NULL, *numfaces = 0; chgp != NULL; 
      chgp = chgp->next) {
    if(chgp->dummy) continue;

#if RMWEDGE == ON  //  TODO: remove?
    /* remove all dielectric panels in the first quadrant */
    tavg[0] = tavg[1] = tavg[2] = 0.0;
    for(i = 0; i < chgp->shape; i++) {
      getAbsCoord(lavg, chgp, i);
      for(j = 0; j < 3; j++) tavg[j] += lavg[j];
    }
    if(chgp->surf->type == DIELEC && tavg[0] > 1.3 && tavg[1] > 1.3 
       && tavg[2] > 1.3)
        continue;
#endif

    /* skip if panel is on conductor in q picture kill list */
    if(chgp->surf->type == CONDTR || chgp->surf->type == BOTH) {
      if(sys->kq_num_list.find(chgp->cond) != sys->kq_num_list.end()) continue;
    }

    /* skip if removing DIELEC's and panel is on dielectric i/f
       - type both interfaces are considered conductors for removal purposes */
    if(chgp->surf->type == DIELEC && sys->rd_) continue;

    /* create and link in a new face */
    if(head == NULL) {
      head = sys->heap.alloc<face>(1, AMSC);
      tail = head;
    }
    else {
      tail->next = sys->heap.alloc<face>(1, AMSC);
      tail = tail->next;
    }
    tail->numsides = chgp->shape;
    /* allocate for corner coordinates */
    tail->c = sys->heap.mat(tail->numsides, 3);
    /* xfer corner coordinates */
    for(i = 0; i < tail->numsides; i++) {
      getAbsCoord(tail->c[i], chgp, i);
    }    
    /* figure and store rhs and normal */
    tail->rhs = getPlane(tail->normal, tail->c[0], tail->c[1], tail->c[2]);
    /* load grey level and line width */
    tail->greylev = GREYLEV;
    tail->width = sys->linewd;
    tail->index = *numfaces;
    (*numfaces)++;

  }

  /* extract an array of pointers to the faces */
  faces = sys->heap.alloc<face *>(*numfaces, AMSC);
  for(tail = head, i = 0; tail != NULL; tail = tail->next, i++) 
      faces[i] = tail;

  if (q != NULL) {
    figure_grey_levels(sys, faces, q, chglist, use_density, black, white);
  }

  /* set up axes lines (always done - needed for alignment) */
  setupLine(axes, 0, 0.0, 0.0, 0.0, axeslen, 0.0, 0.0); /* x axis */
  setupLine(axes, 1, 0.0, 0.0, 0.0, 0.0, axeslen, 0.0); /* y axis */
  setupLine(axes, 2, 0.0, 0.0, 0.0, 0.0, 0.0, axeslen); /* z axis */
  setupLine(axes, 3, 0.85*axeslen, -0.15*axeslen, 0.0, 
            1.15*axeslen, 0.15*axeslen, 0.0); /* x marker */
  setupLine(axes, 4, 1.15*axeslen, -0.15*axeslen, 0.0, 
            0.85*axeslen, 0.15*axeslen, 0.0); /* x marker */
  setupLine(axes, 5, 0.0, axeslen, 0.0, 
            -0.15*axeslen, 1.15*axeslen, 0.0); /* y marker */
  setupLine(axes, 6, 0.0, axeslen, 0.0, 
            0.15*axeslen, 1.15*axeslen, 0.0); /* y marker */

  return(faces);
}

/*
  allows recursive reads in a .fig file with line format
  read <filename>
  only lines (not faces or fills) may be read this way
  (ie encountering "FACES" or "fills" inside a recursive file read is an error,
   unless the ignore faces/fills option (f_) has been specified)
  **** above is only vaguely correct ****
  .fig file format for specifying lines, dots and arrows:
  # <comment>
  <fromx> <fromy> <fromz>           (line from point)
  <tox> <toy> <toz> [<line width>] [<arrow size>] [<dot size>]
  ...
  r <file name>                     (hierarchical read)
  e                                 (or \n)
  dot is always on from point; arrow is always on to point
  optional arguments are only partially so: if one arg is given,
    then all those to the left must also be given
  good sizes: width 0, 1 or 2 (goes straight to postscript)
              arrow size 3.0
              dot size 2.0
  to get just a dot, put in tiny length line and arrow size
*/
static void readLines(ssystem *sys, FILE *fp, line **head, line **tail, int *numlines)
{
  int flines = 0, fflag = 1;
  int f_;               /* f_ == 1 => ignore face and fill info */
  char linein[BUFSIZ];
  char readfile[BUFSIZ], tempc[BUFSIZ];
  double arrowsize, dotsize;
  int linewd;
  FILE *fpin;

  f_ = 1;                       /* hardwire to take fill/face info as
                                   equivalent to end of file */

  /* input lines and add to linked list */
  while(fgets(linein, sizeof(linein), fp) != NULL) {
    if(linein[0] == 'e' || linein[0] == '\0') return;
    if(linein[0] == 'r') {      /* do a recursive read */
      if(sscanf(linein, "%s %s", tempc, readfile) != 2) {
        sys->error("readLines: bad recursive read line format:\n%s", linein);
      }
      if((fpin = fopen(readfile, "r")) == NULL) {
        sys->error("readLines: can't open recursive read file\n `%s'\nto read",
                   readfile);
      }
      readLines(sys, fpin, head, tail, numlines);
      fclose(fpin);
      continue;
    }
    if(linein[0] == 'F') {
      if(f_ == 0) {
        sys->error("readLines: attempt to input faces with a recursive read");
      }
      else {
        return;
      }
    }
    if(linein[0] == '#') continue;
    if(linein[0] == 'f') {
      if(f_ == 0) {
        sys->error("readLines: attempt to input fills with a recursive read");
      }
      else {
        return;
      }
    }

    /* input lines of line information */
    if(fflag == 1) {            /* allocate a line struct; input a from line */
      if(*numlines == 0) {
        *tail = sys->heap.alloc<line>(1, AMSC);
        (*head) = (*tail);
        (*tail)->prev = NULL;
      }
      else {
        (*tail)->next = sys->heap.alloc<line>(1, AMSC);
        ((*tail)->next)->prev = (*tail); /* link back */
        (*tail) = (*tail)->next;
      }
      if(sscanf(linein,"%lf %lf %lf",&((*tail)->from[0]), &((*tail)->from[1]), 
                &((*tail)->from[2])) != 3) {
        sys->error("readLines: from line %d bad, '%s'",flines+1,linein);
      }
      (*tail)->index = *numlines;
      fflag = 0;
      flines++;
    }
    else if(fflag == 0) {               /* input a to line */
      /* if arrow heads are used, line width must be specified */
      if(sscanf(linein, "%lf %lf %lf %d %lf %lf",
                &((*tail)->to[0]), &((*tail)->to[1]), 
                &((*tail)->to[2]), &linewd, &arrowsize, &dotsize) != 6) {
        if(sscanf(linein, "%lf %lf %lf %d %lf",&((*tail)->to[0]), 
                  &((*tail)->to[1]), &((*tail)->to[2]), 
                  &linewd, &arrowsize) != 5) {
          if(sscanf(linein, "%lf %lf %lf %d", &((*tail)->to[0]), 
                    &((*tail)->to[1]), &((*tail)->to[2]), &linewd) != 4) {
            if(sscanf(linein, "%lf %lf %lf", &((*tail)->to[0]), 
                      &((*tail)->to[1]), &((*tail)->to[2])) != 3) {
              sys->error("readLines: to line %d bad, '%s'",flines+1, linein);
            }
            linewd = LINE;
          }
          arrowsize = 0.0;
        }
        dotsize = 0.0;
      }
      (*tail)->width = linewd;
      (*tail)->arrow = arrowsize;
      (*tail)->dot = dotsize;
      fflag = 1;
      flines++;
      (*numlines)++;
    }
  }
  if(fflag == 0) {
    sys->error("readLines: file ended with unmatched from line");
  }
}

/*
  opens a .fig file and reads only lines from it - closes if faces/fills found
*/
line **getLines(ssystem *sys, const char *line_file, int *numlines)
{
  int i;
  FILE *fp;
  line *head, *tail, **linesout;

  *numlines = 0;

  if(line_file == NULL) return(NULL);

  if((fp = fopen(line_file, "r")) == NULL) {
    sys->error("getLines: can't open .fig file\n `%s'\nto read",
               line_file);
  }

  readLines(sys, fp, &head, &tail, numlines);
  fclose(fp);

  /* extract array of pointers to line structs */
  linesout = sys->heap.alloc<line *>(*numlines, AMSC);
  for(i = 0; i < *numlines; i++) {
    linesout[i] = head;
    head = head->next;
  }
  return(linesout);
}

/*
  figure the bounding box and write ps file line
*/
static void getBndingBox(ssystem *sys, face **faces, int numfaces, line **lines, int numlines, int *lowx, int *lowy, FILE *fp, double ***axes)
{
  int upx, upy;
  double xmax = 0.0, ymax = 0.0, minx = 0.0, miny = 0.0;
  int i, j;

  /* find the smallest and largest x and y coordinates (assumed pos) */
  xmax = ymax = 0.0;
  for(i = 0; i < 7 && sys->x_; i++) { /* check axes */
    for(j = 0; j < 2; j++) {
      if(i == 0 && j == 0) {
        minx = axes[i][j][0];
        miny = axes[i][j][1];
      }
      else {
        minx = std::min(minx, axes[i][j][0]);
        miny = std::min(miny, axes[i][j][1]);
      }
      xmax = std::max(xmax, axes[i][j][0]);
      ymax = std::max(ymax, axes[i][j][1]);
    }
  }
  for(i = 0; i < numfaces; i++) { /* check faces */
    for(j = 0; j < faces[i]->numsides; j++) {
      if(i == 0 && j == 0 && !sys->x_) {
        minx = faces[i]->c[j][0];
        miny = faces[i]->c[j][1];
      }
      else {
        minx = std::min(minx, faces[i]->c[j][0]);
        miny = std::min(miny, faces[i]->c[j][1]);
      }
      xmax = std::max(xmax, faces[i]->c[j][0]);
      ymax = std::max(ymax, faces[i]->c[j][1]);
    }
  }
  for(i = 0; i < numlines; i++) { /* check lines */
    if(i == 0 && !sys->x_ && numfaces == 0) {
      minx = std::min(lines[i]->from[0], lines[i]->to[0]);
      miny = std::min(lines[i]->from[1], lines[i]->to[1]);
    }
    else {
      minx = std::min(minx, lines[i]->from[0]);
      miny = std::min(miny, lines[i]->from[1]);
      minx = std::min(minx, lines[i]->to[0]);
      miny = std::min(miny, lines[i]->to[1]);
    }
    xmax = std::max(xmax, lines[i]->to[0]);
    xmax = std::max(xmax, lines[i]->from[0]);
    ymax = std::max(ymax, lines[i]->to[1]);
    ymax = std::max(ymax, lines[i]->from[1]);
  }

  *lowx = minx-2;               /* note 2pnt offset and truncation */
  *lowy = miny-2;
  upx = xmax+2;
  upy = ymax+2;
  fprintf(fp, "%%%%BoundingBox: %d %d %d %d\n", *lowx, *lowy, upx, upy);
}

/*
  dump axes to ps file
*/
static void dumpAxes(double ***axi, FILE *fp)
{
  int i;

  for(i = 0; i < 7; i++) {      /* loop on axes' lines (pointers too) */
    fprintf(fp, "%g %g moveto\n", axi[i][0][0], axi[i][0][1]);
    fprintf(fp, "%g %g lineto\n", axi[i][1][0], axi[i][1][1]);
    fprintf(fp, "%g setlinewidth %d setlinecap %d setlinejoin ",
              AXEWID, LINCAP, LINJIN);
    fprintf(fp, " 0 setgray  stroke\n");
  }
  /*sys->info("Axes inserted\n");*/
}


/*
  copy the body of the header to the output file
*/
void copyBody(FILE *fp)
{
  static char str[] = "\
%%%%DocumentProcSets: FreeHand_header 2 0 \n\
%%%%DocumentSuppliedProcSets: FreeHand_header 2 0 \n\
%%%%ColorUsage: Color \n\
%%%%CMYKProcessColor: 0 0 0 0.1  (10%% gray) \n\
%%%%+ 0 0 0 0.2  (20%% gray) \n\
%%%%+ 0 0 0 0.4  (40%% gray) \n\
%%%%+ 0 0 0 0.6  (60%% gray) \n\
%%%%+ 0 0 0 0.8  (80%% gray) \n\
%%%%EndComments \n\
%%%%BeginProcSet: FreeHand_header 2 0 \n\
/FreeHandDict 200 dict def \n\
FreeHandDict begin \n\
/currentpacking where{pop true setpacking}if \n\
/bdf{bind def}bind def \n\
/bdef{bind def}bdf \n\
/xdf{exch def}bdf \n\
/ndf{1 index where{pop pop pop}{dup xcheck{bind}if def}ifelse}bdf \n\
/min{2 copy gt{exch}if pop}bdf \n\
/max{2 copy lt{exch}if pop}bdf \n\
/dr{transform .25 sub round .25 add \n\
exch .25 sub round .25 add exch itransform}bdf \n\
/curveto{dr curveto}bdf \n\
/lineto{dr lineto}bdf \n\
/moveto{dr moveto}bdf \n\
/graystep 1 256 div def \n\
/bottom -0 def \n\
/delta -0 def \n\
/frac -0 def \n\
/left -0 def \n\
/numsteps -0 def \n\
/numsteps1 -0 def \n\
/radius -0 def \n\
/right -0 def \n\
/top -0 def \n\
/x -0 def \n\
/y -0 def \n\
/df currentflat def \n\
/tempstr 1 string def \n\
/clipflatness 3 def \n\
/inverted? \n\
0 currenttransfer exec .5 ge def \n\
/concatprocs{ \n\
/proc2 exch cvlit def/proc1 exch cvlit def \n\
/newproc proc1 length proc2 length add array def \n\
newproc 0 proc1 putinterval newproc proc1 length proc2 putinterval \n\
newproc cvx}bdf \n\
/storerect{/top xdf/right xdf/bottom xdf/left xdf}bdf \n\
/rectpath{newpath left bottom moveto left top lineto \n\
right top lineto right bottom lineto closepath}bdf \n\
/sf{dup 0 eq{pop df dup 3 mul}{dup} ifelse /clipflatness xdf setflat}bdf \n";

static char str2[] = "\
version cvr 38.0 le \n\
{/setrgbcolor{ \n\
currenttransfer exec 3 1 roll \n\
currenttransfer exec 3 1 roll \n\
currenttransfer exec 3 1 roll \n\
setrgbcolor}bdf}if \n\
/gettint{0 get}bdf \n\
/puttint{0 exch put}bdf \n\
/vms{/vmsv save def}bdf \n\
/vmr{vmsv restore}bdf \n\
/vmrs{vmr vms}bdf \n\
/CD{/NF exch def \n\
{exch dup/FID ne{exch NF 3 1 roll put} \n\
{pop pop}ifelse}forall NF}bdf \n\
/MN{1 index length/Len exch def \n\
dup length Len add string dup \n\
Len 4 -1 roll putinterval dup 0 4 -1 roll putinterval}bdf \n\
/RC{256 string cvs(|______)anchorsearch \n\
{1 index MN cvn/NewN exch def cvn \n\
findfont dup maxlength dict CD dup/FontName NewN put dup \n\
/Encoding MacVec put NewN exch definefont pop}{pop}ifelse}bdf \n\
/RF{dup FontDirectory exch known{pop}{RC}ifelse}bdf \n\
/FF{dup 256 string cvs(|______)exch MN cvn dup FontDirectory exch known \n\
{exch}if pop findfont}bdf \n\
userdict begin /BDFontDict 20 dict def end \n\
BDFontDict begin \n\
/bu{}def \n\
/bn{}def \n\
/setTxMode{pop}def \n\
/gm{moveto}def \n\
/show{pop}def \n\
/gr{pop}def \n\
/fnt{pop pop pop}def \n\
/fs{pop}def \n\
/fz{pop}def \n\
/lin{pop pop}def \n\
end \n\
/MacVec 256 array def \n\
MacVec 0 /Helvetica findfont \n\
/Encoding get 0 128 getinterval putinterval \n\
MacVec 127 /DEL put MacVec 16#27 /quotesingle put MacVec 16#60 /grave put \n\
/NUL/SOH/STX/ETX/EOT/ENQ/ACK/BEL/BS/HT/LF/VT/FF/CR/SO/SI \n\
/DLE/DC1/DC2/DC3/DC4/NAK/SYN/ETB/CAN/EM/SUB/ESC/FS/GS/RS/US \n\
MacVec 0 32 getinterval astore pop \n\
/Adieresis/Aring/Ccedilla/Eacute/Ntilde/Odieresis/Udieresis/aacute \n\
/agrave/acircumflex/adieresis/atilde/aring/ccedilla/eacute/egrave \n\
/ecircumflex/edieresis/iacute/igrave/icircumflex/idieresis/ntilde/oacute \n\
/ograve/ocircumflex/odieresis/otilde/uacute/ugrave/ucircumflex/udieresis \n\
/dagger/degree/cent/sterling/section/bullet/paragraph/germandbls \n\
/register/copyright/trademark/acute/dieresis/notequal/AE/Oslash \n\
/infinity/plusminus/lessequal/greaterequal/yen/mu/partialdiff/summation \n";

static char str3[] = "\
/product/pi/integral/ordfeminine/ordmasculine/Omega/ae/oslash \n\
/questiondown/exclamdown/logicalnot/radical/florin/approxequal/Delta/guillemotleft \n\
/guillemotright/ellipsis/nbspace/Agrave/Atilde/Otilde/OE/oe \n\
/endash/emdash/quotedblleft/quotedblright/quoteleft/quoteright/divide/lozenge \n\
/ydieresis/Ydieresis/fraction/currency/guilsinglleft/guilsinglright/fi/fl \n\
/daggerdbl/periodcentered/quotesinglbase/quotedblbase \n\
/perthousand/Acircumflex/Ecircumflex/Aacute \n\
/Edieresis/Egrave/Iacute/Icircumflex/Idieresis/Igrave/Oacute/Ocircumflex \n\
/apple/Ograve/Uacute/Ucircumflex/Ugrave/dotlessi/circumflex/tilde \n\
/macron/breve/dotaccent/ring/cedilla/hungarumlaut/ogonek/caron \n\
MacVec 128 128 getinterval astore pop \n\
/fps{currentflat exch dup 0 le{pop 1}if \n\
{dup setflat 3 index stopped \n\
{1.3 mul dup 3 index gt{pop setflat pop pop stop}if}{exit}ifelse \n\
}loop pop setflat pop pop \n\
}bdf \n\
/fp{100 currentflat fps}bdf \n\
/rfp{clipflatness currentflat fps}bdf \n\
/fcp{100 clipflatness fps}bdf \n\
/fclip{{clip}fcp}bdf \n\
/feoclip{{eoclip}fcp}bdf \n\
end %%. FreeHandDict \n\
%%%%EndProcSet \n\
%%%%BeginSetup \n\
FreeHandDict begin \n\
/ccmyk{dup 5 -1 roll sub 0 max exch}ndf \n\
/setcmykcolor{1 exch sub ccmyk ccmyk ccmyk pop setrgbcolor}ndf \n\
/setcmykcoloroverprint{4{dup -1 eq{pop 0}if 4 1 roll}repeat setcmykcolor}ndf \n\
/findcmykcustomcolor{5 /packedarray where{pop packedarray}{array astore readonly}ifelse}ndf \n\
/setcustomcolor{exch aload pop pop 4{4 index mul 4 1 roll}repeat setcmykcolor pop}ndf \n\
/setseparationgray{1 exch sub dup dup dup setcmykcolor}ndf \n\
/setoverprint{pop}ndf \n\
/currentoverprint false ndf \n\
/colorimage{pop pop \n\
[5 -1 roll/exec cvx 6 -1 roll/exec cvx 7 -1 roll/exec cvx 8 -1 roll/exec cvx \n\
/exch cvx/pop cvx/exch cvx/pop cvx/exch cvx/pop cvx/invbuf cvx]cvx image} \n\
%%. version 47.1 of Postscript defines colorimage incorrectly (rgb model only) \n\
version cvr 47.1 le{userdict begin bdf end}{ndf}ifelse \n\
/customcolorimage{pop image}ndf \n\
/separationimage{image}ndf \n\
/newcmykcustomcolor{6 /packedarray where{pop packedarray}{array astore readonly}ifelse}ndf \n\
/inkoverprint false ndf \n\
/setinkoverprint{pop}ndf \n\
/overprintprocess{pop}ndf \n\
/setspotcolor \n\
{spots exch get 0 5 getinterval exch setcustomcolor}ndf \n\
/currentcolortransfer{currenttransfer dup dup dup}ndf \n\
/setcolortransfer{systemdict begin settransfer end pop pop pop}ndf \n";

static char str4[] = "\
/setimagecmyk{dup length 4 eq \n\
{aload pop} \n\
{aload pop spots exch get 0 4 getinterval aload pop 4 \n\
{4 index mul 4 1 roll}repeat 5 -1 roll pop} ifelse \n\
systemdict /colorimage known{version cvr 47.1 gt}{false}ifelse \n\
not{pop 1 currentgray sub}if \n\
/ik xdf /iy xdf /im xdf /ic xdf \n\
}ndf \n\
/setcolor{dup length 4 eq \n\
{aload overprintprocess setcmykcolor} \n\
{aload 1 get spots exch get 5 get setinkoverprint setspotcolor} \n\
ifelse}ndf \n\
/bc2[0 0]def \n\
/bc4[0 0 0 0]def \n\
/c1[0 0 0 0]def \n\
/c2[0 0 0 0]def \n\
/absmax{2 copy abs exch abs gt{exch}if pop}bdf \n\
/calcstep \n\
{c1 length 4 eq \n\
{ \n\
0 1 3 \n\
{c1 1 index get \n\
c2 3 -1 roll get \n\
sub \n\
}for \n\
absmax absmax absmax \n\
} \n\
{ \n\
bc2 c1 1 get 1 exch put \n\
c1 gettint c2 gettint \n\
sub abs \n\
}ifelse \n\
graystep div abs round dup 0 eq{pop 1}if \n\
dup /numsteps xdf 1 sub dup 0 eq{pop 1}if /numsteps1 xdf \n\
}bdf \n\
/cblend{ \n\
c1 length 4 eq \n\
{ \n\
0 1 3 \n\
{bc4 exch \n\
c1 1 index get \n\
c2 2 index get \n\
1 index sub \n\
frac mul add put \n\
}for bc4 \n\
}{ \n\
bc2 \n\
c1 gettint \n\
c2 gettint \n\
1 index sub \n\
frac mul add \n\
puttint bc2 \n\
}ifelse \n\
setcolor \n\
}bdf \n";

static char str5[] = "\
/logtaper{/frac frac 9 mul 1 add log def}bdf \n\
/imbits 1 def \n\
/iminv false def \n\
/invbuf{0 1 2 index length 1 sub{dup 2 index exch get 255 exch sub 2 index 3 1 roll put}for}bdf \n\
/cyanrp{currentfile cyanbuf readhexstring pop iminv{invbuf}if}def \n\
/magentarp{cyanbuf magentabuf copy}bdf \n\
/yellowrp{cyanbuf yellowbuf copy}bdf \n\
/blackrp{cyanbuf blackbuf copy}bdf \n\
/fixtransfer{ \n\
dup{ic mul ic sub 1 add}concatprocs exch \n\
dup{im mul im sub 1 add}concatprocs exch \n\
dup{iy mul iy sub 1 add}concatprocs exch \n\
{ik mul ik sub 1 add}concatprocs \n\
currentcolortransfer \n\
5 -1 roll exch concatprocs 7 1 roll \n\
4 -1 roll exch concatprocs 6 1 roll \n\
3 -1 roll exch concatprocs 5 1 roll \n\
concatprocs 4 1 roll \n\
setcolortransfer \n\
}bdf \n";

fprintf(fp, "%s%s%s%s%s", str, str2, str3, str4, str5);

}

#if defined(UNUSED)
/*
  numbers the faces for checking 
*/
static void numberFaces(face **faces, int numfaces, FILE *fp)
{
  int i, j, mid[2];
  double cent[2];

  /* put face number at average point of each face */
  for(i = 0; i < numfaces; i++) {
    /* figure midpoint, truncate (truncation not really necessary) */
    for(j = 0, cent[0] = cent[1] = 0.0; j < faces[i]->numsides; j++) {
      cent[0] += faces[i]->c[j][0]; /* x coordinate sum */
      cent[1] += faces[i]->c[j][1]; /* y coordinate sum */
    }
    mid[0] = cent[0]/(((double) faces[i]->numsides)); /* average x */
    mid[1] = cent[1]/(((double) faces[i]->numsides)); /* average y */
    /* dump a label with associated garbage */
    fprintf(fp, "%%%%IncludeFont: Times-Roman\n");
    fprintf(fp, "/f1 /|______Times-Roman dup RF findfont def\n{\n");
    fprintf(fp, "f1 [%g 0 0 %g 0 0] makesetfont\n", FONT, FONT);
    fprintf(fp, "%d %d moveto\n", mid[0], mid[1]);
    fprintf(fp, "0 0 32 0 0 (F%d) ts\n}\n", i);
    fprintf(fp, "[0 0 0 1]\nsts\nvmrs\n");
  }
}
#endif

/*
  number a face for checking - used to cover up obscured faces' numbers
*/
static void numberFace(face *fac, FILE *fp)
{
  int j, mid[2];
  double cent[2];

  /* figure midpoint, truncate (truncation not really necessary) */
  for(j = 0, cent[0] = cent[1] = 0.0; j < fac->numsides; j++) {
    cent[0] += fac->c[j][0]; /* x coordinate sum */
    cent[1] += fac->c[j][1]; /* y coordinate sum */
  }
  mid[0] = cent[0]/(((double) fac->numsides)); /* average x */
  mid[1] = cent[1]/(((double) fac->numsides)); /* average y */
  /* dump a label with associated garbage */
  fprintf(fp, "%%%%IncludeFont: Times-Roman\n");
  fprintf(fp, "/f1 /|______Times-Roman dup RF findfont def\n{\n");
  fprintf(fp, "f1 [%g 0 0 %g 0 0] makesetfont\n", FONT, FONT);
  fprintf(fp, "%d %d moveto\n", mid[0], mid[1]);
  fprintf(fp, "0 0 32 0 0 (%d) ts\n}\n", fac->index);
  fprintf(fp, "[0 0 0 1]\nsts\nvmrs\n");

}

#if defined(UNUSED)
/*
  dumps adjacency graph as a ps file - uses both input order and graph order
*/
static void dumpAdjGraph(face **faces, int numfaces, FILE *fp)
{
  int f, i;
  double x, y;                  /* current point in plot */
  double stepx, stepy;          /* step in x and y directions */
  double font;                  /* font size */

  /* start the input numbered graph refered to lower left corner
     - row numbers on right because it's easier */
  /* set up the sizes - font never bigger than FONT; stepx, stepy <=1.25FONT */
  stepx = std::min(1.25*FONT, (IMAGEX-OFFSETX)/(double)numfaces);
  stepy = std::min(1.25*FONT, (IMAGEY-OFFSETY)/(double)numfaces);
  font = std::min(stepx, stepy)/1.25;
  x = OFFSETX + numfaces*stepx; 
  y = OFFSETY + numfaces*stepy;

  /* number columns - mark those divisible by ten */
  for(f = 0; f < numfaces; f++) {
    if(f % 10 == 0 && f != 0) fprintf(fp, "%g %g dia\n", x-f*stepx, y+stepy);
  }

  /* number each row and fill it in - input ordering
  for(f = 0; f < numfaces; f++) { */
    /* dump a row label with associated garbage
    fprintf(fp, "%%%%IncludeFont: Times-Roman\n");
    fprintf(fp, "/f1 /|______Times-Roman dup RF findfont def\n{\n");
    fprintf(fp, "f1 [%g 0 0 %g 0 0] makesetfont\n", FONT, FONT);
    fprintf(fp, "%g %g moveto\n", x+stepx, y-faces[f]->index*stepy);
    fprintf(fp, "0 0 32 0 0 (%d) ts\n}\n", faces[f]->index);
    fprintf(fp, "[0 0 0 1]\nsts\nvmrs\n"); */
    /* dump dot if an edge
    for(i = 0; i < faces[f]->numbehind; i++) {
      fprintf(fp, "%g %g dot\n", 
              x-(faces[f]->behind)[i]->index*stepx, y-faces[f]->index*stepy);
    }
  } */
  /* dump title
  fprintf(fp, "%%%%IncludeFont: Times-Roman\n");
  fprintf(fp, "/f1 /|______Times-Roman dup RF findfont def\n{\n");
  fprintf(fp, "f1 [%g 0 0 %g 0 0] makesetfont\n", FONT, FONT);
  fprintf(fp, "%g %g moveto\n", OFFSETX, y+FONT);
  fprintf(fp, "0 0 32 0 0 (Input Ordering) ts\n}\n");
  fprintf(fp, "[0 0 0 1]\nsts\nvmrs\n"); */

  /* y += (numfaces*stepy + 3*FONT);    */ /* offset 2nd array */

  /* number each row and fill it in - graph ordering */
  for(f = 0; f < numfaces; f++) {
    fprintf(fp, "%%%%IncludeFont: Times-Roman\n");
    fprintf(fp, "/f1 /|______Times-Roman dup RF findfont def\n{\n");
    fprintf(fp, "f1 [%g 0 0 %g 0 0] makesetfont\n", FONT, FONT);
    fprintf(fp, "%g %g moveto\n", x+stepx, y-faces[f]->depth*stepy);
    fprintf(fp, "0 0 32 0 0 (%d) ts\n}\n", faces[f]->depth);
    fprintf(fp, "[0 0 0 1]\nsts\nvmrs\n");
    for(i = 0; i < faces[f]->numbehind; i++) {
      fprintf(fp, "%g %g dot\n", 
              x-(faces[f]->behind)[i]->depth*stepx, y-faces[f]->depth*stepy);
    }
  }
  fprintf(fp, "%%%%IncludeFont: Times-Roman\n");
  fprintf(fp, "/f1 /|______Times-Roman dup RF findfont def\n{\n");
  fprintf(fp, "f1 [%g 0 0 %g 0 0] makesetfont\n", FONT, FONT);
  fprintf(fp, "%g %g moveto\n", OFFSETX, y+FONT);
  fprintf(fp, "0 0 32 0 0 (Graph Ordering) ts\n}\n");
  fprintf(fp, "[0 0 0 1]\nsts\nvmrs\n");
}
#endif

/*
  dump face graph as a text file
*/
void dumpFaceText(ssystem *sys, face **faces, int numfaces)
{
  int f, i, first = 0, k;

  sys->msg("depth order (input order) - lower numbers are deeper\n");
  for(f = 0; f < numfaces; f++) {
    sys->msg("%d (%d):", faces[f]->depth, faces[f]->index);
    for(i = 0; i < faces[f]->numbehind && faces[f]->behind != NULL; i++) {
      sys->msg(" %d (%d)", (faces[f]->behind)[i]->depth,
              (faces[f]->behind)[i]->index);
      if(i % 5 == 0 && i != 0) sys->msg("\n");
    }
    if((i-1) % 5 != 0 || i == 1) sys->msg("\n");
  }

  /* check to see that ordering is consistent with deeper lists */
  for(f = 0; f < numfaces; f++) {
    for(k = 0; k < faces[f]->numbehind; k++) {
      if(faces[f]->depth >= (faces[f]->behind)[k]->depth) {
        if(first == 0) {
          first = 1;
          sys->msg("\nVertices whose depth lists are inconsistent\n");
        }
        sys->msg("%d (%d):", faces[f]->depth, faces[f]->index);
        for(i = 0; i < faces[f]->numbehind && faces[f]->behind != NULL; i++) {
          sys->msg(" %d (%d)", (faces[f]->behind)[i]->depth,
                  (faces[f]->behind)[i]->index);
          if(i % 5 == 0 && i != 0) sys->msg("\n");
        }
        if((i-1) % 5 != 0 || i == 1) sys->msg("\n");
        break;
      }
    }
  }

}

/*
  dumps a line of chars in the Aldus FreeHand ps format
*/
void dump_line_as_ps(FILE *fp, char *psline, double x_position, double y_position, double font_size)
{
  fprintf(fp, "%%%%IncludeFont: Times-Roman\n");
  fprintf(fp, "/f1 /|______Times-Roman dup RF findfont def\n{\n");
  fprintf(fp, "f1 [%g 0 0 %g 0 0] makesetfont\n", font_size, font_size);
  fprintf(fp, "%g %g moveto\n", x_position, y_position);
  fprintf(fp, "0 0 32 0 0 (%s) ts\n}\n", psline);
  fprintf(fp, "[0 0 0 1]\nsts\nvmrs\n");
}

/*
  dump nblocks blocks with shades between white and black, labeled with density
*/
static void dump_shading_key(ssystem *sys, FILE *fp, int nblocks, int precision, double font_size, int use_density, double black, double white)
{
  int i;
  double x_right, y_top, block_hgt, block_x, block_y, string_x, diddle_x;
  double grey_step, grey_lev, density, density_step, white_width;
  char linein[BUFSIZ], ctrl[BUFSIZ];

  x_right = OFFSETX + IMAGEX;
  y_top = OFFSETY + IMAGEY;
  block_hgt = KEYHGT/(double)nblocks;
  block_x = x_right - KEYWID;
  block_y = y_top;
  /*string_x = block_x - font_size*(6.0/2.0 + (double)precision);*/
  string_x = block_x + font_size/2.0;

  /* writing raw ps so 1.0 = white, 0.0 = black */
  grey_lev = 0.0;
  grey_step = 1.0/(double)(nblocks-1);
  density = black;
  density_step = (black-white)/(double)(nblocks-1);
  /*white_width = 3.0 + (double)precision;*/
  white_width = KEYWID;

  /* write the key title */
  if(use_density) {
    strcpy(linein, "DENSITY, statC/m^2");
    diddle_x = font_size;
  }
  else {
    strcpy(linein, "CHARGE, statC");
    diddle_x = font_size/2.0;
  }
  dump_line_as_ps(fp, linein, string_x-diddle_x, y_top + font_size/2.0, 
                  font_size);

  for(i = 0; i < nblocks; i++) {
    /* write a fill with border for the key block */
    /* dump the fill */
    fprintf(fp, "%g %g moveto\n", block_x, block_y);
    fprintf(fp, "%g %g lineto\n", block_x + KEYWID, block_y);
    fprintf(fp, "%g %g lineto\n", block_x + KEYWID, block_y - block_hgt);
    fprintf(fp, "%g %g lineto\n", block_x, block_y - block_hgt);
    fprintf(fp, "closepath\n");
    fprintf(fp, " %g setgray fill\n", grey_lev);

    /* dump the white out for the label */
    fprintf(fp, "%g %g moveto\n", block_x, block_y);
    fprintf(fp, "%g %g lineto\n", block_x + white_width, block_y);
    fprintf(fp, "%g %g lineto\n", 
            block_x + white_width, block_y - font_size - font_size/10.0);
    fprintf(fp, "%g %g lineto\n", 
            block_x, block_y - font_size - font_size/10.0);
    fprintf(fp, "closepath\n");
    fprintf(fp, " 1.0 setgray fill\n");

    /* dump the outline */
    fprintf(fp, "%g %g moveto\n", block_x, block_y);
    fprintf(fp, "%g %g lineto\n", block_x + KEYWID, block_y);
    fprintf(fp, "%g %g lineto\n", block_x + KEYWID, block_y - block_hgt);
    fprintf(fp, "%g %g lineto\n", block_x, block_y - block_hgt);
    fprintf(fp, "closepath\n");
    fprintf(fp, "%g setlinewidth %d setlinecap %d setlinejoin ",
            sys->linewd, LINCAP, LINJIN);
    fprintf(fp, " 0 setgray  stroke\n");

    /* dump the label */
    sprintf(ctrl, "%%.%dg", precision);
    sprintf(linein, ctrl, density);
    dump_line_as_ps(fp, linein, string_x, block_y - font_size, font_size);

    block_y -= block_hgt;
    density -= density_step;
    grey_lev += grey_step;
  }
}

/*
  numbers the lines for checking 
*/
static void numberLines(line **lines, int numlines, FILE *fp)
{
  int i, mid[2];

  /* put line number on midpoint of each line */
  for(i = 0; i < numlines; i++) {
    /* figure midpoint, truncate (truncation not really necessary) */
    mid[0] = ((lines[i]->from)[0] + (lines[i]->to)[0])/2;
    mid[1] = ((lines[i]->from)[1] + (lines[i]->to)[1])/2;
    /* dump a label with associated garbage */
    fprintf(fp, "%%%%IncludeFont: Times-Roman\n");
    fprintf(fp, "/f1 /|______Times-Roman dup RF findfont def\n{\n");
    fprintf(fp, "f1 [%g 0 0 %g 0 0] makesetfont\n", FONT, FONT);
    fprintf(fp, "%d %d moveto\n", mid[0], mid[1]);
    fprintf(fp, "0 0 32 0 0 (%d) ts\n}\n", lines[i]->index);
    fprintf(fp, "[0 0 0 1]\nsts\nvmrs\n");
  }
}

/*
  lobotomized version of dumpPs in orthoPs.c - dumps lines/arrows
*/
static void dumpLines(ssystem *sys, FILE *fp, line **lines, int numlines)
{
  int i, j, w_;
  double temp[3], temp1[3], x, y;

  if(fp == NULL) {
    sys->error("dumpLines: null ps file pointer");
  }

  w_ = 0;                       /* hardwire for no width override */

  /* dump the lines  */
  for(i = 0; i < numlines; i++) {
    fprintf(fp, "%%%% begin line %d\n", lines[i]->index);
    fprintf(fp, "0 sf\nnewpath\n");
    x = (lines[i]->from)[0];
    y = (lines[i]->from)[1];
    fprintf(fp, "%g %g moveto\n", x, y);
    x = (lines[i]->to)[0];
    y = (lines[i]->to)[1];
    fprintf(fp, "%g %g lineto\n", x, y);
    fprintf(fp, "gsave\n");
    if(lines[i]->width == DASHED) {
      if(w_ == 0) 
          fprintf(fp, "%d setlinewidth 1 setlinecap 0 setlinejoin 3.863693",
              DASWTH);
      else fprintf(fp, "%d setlinewidth 1 setlinecap 0 setlinejoin 3.863693",
              OVRWTH);
      fprintf(fp, 
              " setmiterlimit [0 0 0 1]setcolor [2 4] 0 setdash {stroke}fp\n");
    }
    else {
      if(w_ == 0)
          fprintf(fp, "%d setlinewidth 1 setlinecap 0 setlinejoin 3.863693",
                  lines[i]->width);
      else
          fprintf(fp, "%d setlinewidth 1 setlinecap 0 setlinejoin 3.863693",
                  OVRWTH);
      fprintf(fp, " setmiterlimit [0 0 0 1]setcolor  {stroke}fp\n");
    }
    fprintf(fp, "grestore\n");
    if(lines[i]->arrow > 0.0) { /* put arrow head on to side if desired */
      /* figure unit vector from `to' point to `from' point */
      for(j = 0; j < 2; j++) temp[j] = lines[i]->from[j]-lines[i]->to[j];
      temp1[0] = sqrt(temp[0]*temp[0]+temp[1]*temp[1]);
      for(j = 0; j < 2; j++) temp[j] /= temp1[0];
      for(j = 0; j < 2; j++)    /* figure unit perpendicular */
          temp1[j] = 
              1.0/(temp[j]*sqrt(1.0/(temp[0]*temp[0])+1.0/(temp[1]*temp[1])));
      temp1[0] = -temp1[0];
      /* draw the arrow */
      fprintf(fp, "%%%% Begin arrow head for line %d\n", i);
      fprintf(fp, "%g %g moveto\n", lines[i]->to[0], lines[i]->to[1]);
      fprintf(fp, "%g %g lineto\n", 
              lines[i]->to[0]+lines[i]->arrow*ALEN*temp[0]
              +lines[i]->arrow*(AWID/2)*temp1[0],
              lines[i]->to[1]+lines[i]->arrow*ALEN*temp[1]
              +lines[i]->arrow*(AWID/2)*temp1[1]);
      fprintf(fp, "%g %g lineto\n", 
              lines[i]->to[0]+lines[i]->arrow*ALEN*temp[0]
              -lines[i]->arrow*(AWID/2)*temp1[0],
              lines[i]->to[1]+lines[i]->arrow*ALEN*temp[1]
              -lines[i]->arrow*(AWID/2)*temp1[1]);
      fprintf(fp, "closepath\n");
      fprintf(fp, " 0 setgray fill\n");
      /* put dot on from end of line, if called for */
      if(lines[i]->dot > 0.0)
          fprintf(fp, "%g %g %g 0 360 arc closepath fill\n",
                  lines[i]->from[0], lines[i]->from[1], lines[i]->dot*DOTSIZ);
    }
  }
}
  

/*
  dump faces in ps Aldus FreeHand format - assumes header body in afhpsheader
*/
void dumpPs(ssystem *sys, face **faces, int numfaces, line **lines, int numlines, FILE *fp, const char **argv, int argc, int use_density, double black, double white)
{
  int i, f, lowx, lowy;
  double ***axes = sys->axes;
  char linein[BUFSIZ];
  
  /* print the lines before the bounding box */
  fprintf(fp, "%%!PS-Adobe-2.0 EPSF-1.2\n");
  fprintf(fp, "%%%%Creator: FreeHand\n");
  fprintf(fp, "%%%%Title: test.ps\n");
  fprintf(fp, "%%%%CreationDate: 4/19/90 10:47 AM\n");

  getBndingBox(sys, faces, numfaces, lines, numlines,
               &lowx, &lowy, fp, axes); /* prnt bnding box */
  copyBody(fp);                 /* copys the body of the header from
                                   "afhpsheader" */
  
  /* dump the text header if needed */
  if(sys->n_ || sys->g_ || sys->c_ || sys->q_) {
    fprintf(fp, "/textopf false def\n/curtextmtx{}def\n/otw .25 def\n");
    fprintf(fp, "/msf{dup/curtextmtx xdf makefont setfont}bdf\n");
    fprintf(fp, "/makesetfont/msf load def\n");
    fprintf(fp, "/curtextheight{.707104 .707104 curtextmtx dtransform\n");
    fprintf(fp, "dup mul exch dup mul add sqrt}bdf\n");
    fprintf(fp, "/ta{1 index\n{tempstr 0 2 index put tempstr 2 index\n");
    fprintf(fp, "gsave exec grestore\ntempstr stringwidth rmoveto\n");
    fprintf(fp, "5 index eq{6 index 6 index rmoveto}if\n");
    fprintf(fp, "3 index 3 index rmoveto\n");
    fprintf(fp, "}forall 7{pop}repeat}bdf\n");
    fprintf(fp, 
            "/sts{setcolor textopf setoverprint/ts{awidthshow}def exec}bdf\n");
    fprintf(fp, "/stol{setlinewidth setcolor textopf setoverprint newpath\n");
    fprintf(fp, "/ts{{false charpath stroke}ta}def exec}bdf\n");
  }

  /* print rest of header (starting with after /currentpacking where...) */
  fprintf(fp, "/currentpacking where{pop false setpacking}if\n");
  fprintf(fp, "%%%%EndSetup\n");
  fprintf(fp, "/spots[1 0 0 0 (Process Cyan) false newcmykcustomcolor\n");
  fprintf(fp, "0 1 0 0 (Process Magenta) false newcmykcustomcolor\n");
  fprintf(fp, "0 0 1 0 (Process Yellow) false newcmykcustomcolor\n");
  fprintf(fp, 
          "0 0 0 1 (Process Black) false newcmykcustomcolor\n]def\nvms\n");

  /* dump command line as a comment */
  fprintf(fp, "%%%% ");
  for(i = 0; i < argc; i++) fprintf(fp, " %s", argv[i]);
  fprintf(fp, "\n");

  if(sys->x_) dumpAxes(axes, fp); /* dump axes if called for */

  /* for each face - dump fill, then outline - assumes depth ordering */
  for(f = 0; f < numfaces; f++) {
    if(!sys->f_) {
      /* dump the fill */
      fprintf(fp, "%%%% Begin face %d\n", f);
      /* fprintf(fp, "0 sf\nnewpath\n"); */
      /* fprintf(fp, "newpath\n");*/
      fprintf(fp, "%g %g moveto\n", faces[f]->c[0][0], faces[f]->c[0][1]);
      for(i = 1; i < faces[f]->numsides; i++) {
        fprintf(fp, "%g %g lineto\n", faces[f]->c[i][0], faces[f]->c[i][1]);
      }
      fprintf(fp, "closepath\n");
      /* fprintf(fp, "gsave\n");*/
      /* fprintf(fp, "[0 0 0 %g]setcolor  {fill}fp\ngrestore\n", GREYLEV); */
      /* fprintf(fp, "[0 0 0 %g]setcolor  fill\n", GREYLEV);*/
      fprintf(fp, " %g setgray fill\n", 1.0-faces[f]->greylev);
      /* fprintf(fp, "grestore\n");*/
    }

    /* dump the outline */
    /* fprintf(fp, "0 sf\nnewpath\n"); */
    /* fprintf(fp, "newpath\n");*/
    fprintf(fp, "%g %g moveto\n", faces[f]->c[0][0], faces[f]->c[0][1]);
    for(i = 1; i < faces[f]->numsides; i++) {
      fprintf(fp, "%g %g lineto\n", faces[f]->c[i][0], faces[f]->c[i][1]);
    }
    fprintf(fp, "closepath\n");
    /* fprintf(fp, "gsave\n");*/
    if(faces[f]->width == DASHED) {
      fprintf(fp, "%d setlinewidth %d setlinecap %d setlinejoin 3.863693",
              DASWTH, LINCAP, LINJIN);
      /* fprintf(fp, 
         " setmiterlimit [0 0 0 1]setcolor [2 4] 0 setdash {stroke}fp\n");*/
      fprintf(fp, 
              " setmiterlimit [0 0 0 1]setcolor [2 4] 0 setdash stroke\n");
    }
    else {
      /* fprintf(fp, "%g setlinewidth %d setlinecap %d setlinejoin 3.863693",
         faces[f]->width, LINCAP, LINJIN); */
      fprintf(fp, "%g setlinewidth %d setlinecap %d setlinejoin ",
              faces[f]->width, LINCAP, LINJIN);
      /* fprintf(fp, "[0 0 0 1]setcolor  {stroke}fp\ngrestore\n"); */
      /* fprintf(fp, "[0 0 0 1]setcolor  stroke\n");*/
      fprintf(fp, " 0 setgray  stroke\n");
      /* fprintf(fp, "grestore\n");*/
    }
    if(sys->n_) numberFace(faces[f], fp);
  }

  dumpLines(sys, fp, lines, numlines);

  /* if this is just to check placement, number the faces */
  if(sys->n_) {
    /* numberFaces(faces, numfaces, fp); */
    numberLines(lines, numlines, fp);
    /*sys->info("Faces and lines numbered\n");*/
  }

  /* if fills were not included, say so
  if(f_) sys->info("Face fills not written to ps file\n"); */

  /* print shading key if not disabled and charge density info was inputed */
  if(sys->q_ && !sys->rk_ && !sys->m_)
      dump_shading_key(sys, fp, KEYBLKS, KEYPREC, KEYFONT, use_density, black, white);
    
  /* print footer */
  if(sys->c_) {                      /* print command line if asked for */
    for(f = 0, linein[0] = '\0'; f < argc; f++) {
      strcat(linein, argv[f]);
      strcat(linein, " ");
    }
    dump_line_as_ps(fp, linein, OFFSETX+2*CMDFONT, IMAGEY-2*CMDFONT, CMDFONT);
    /*sys->info("Command line printed\n");*/
  }
   
  fprintf(fp, "vmr\nend  %% FreeHandDict\n");
  if(!sys->s_) {
    fprintf(fp, "showpage\n");
    /*sys->info("Showpage inserted\n");*/
  }
  fprintf(fp, "%%%%EndDocument: _\n");
}

