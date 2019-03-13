
#include "powder_setup.h"
#include <stdio.h>

void SetupPowder2(int nt, \
                  double **xr, \
                  double **yr, \
                  double **zr, \
                  double **rrr) {

  int i, j;
  double x, y, z, x2, y2, z2, r2;

  /* Do the (x + y + z = nt) face of the octahedron
  !z -> 0 to nt-1
  !y -> 0 to nt-z
  !x -> nt - y - z
  !*/

  for( j = 0; j <= nt-1; j++) {
    // printf("%i\n", j);
    for( i = 0; i <= nt-j; i++) {
      x = nt-i-j;
      y = i;
      z = j;
      x2 = x*x;
      y2 = y*y;
      z2 = z*z;
      r2 = x2 + y2 + z2;
      xr[i][j] = x2/r2;
      yr[i][j] = y2/r2;
      zr[i][j] = z2/r2;
      rrr[i][j] = 1.0/(r2*sqrt(r2));
    }
  }

  /* Do the (-x + y + z = nt) face of the octahedron
  !z -> 0 to nt-1
  !y -> 0 to nt-z
  !x -> -nt + y + z
  !*/

  for( j = 0; j <= nt-1; j++) {
    // printf("%i,  %i\n", nt, j);
    for( i = nt-j+1; i <= nt; i++) {
      x = nt-i-j;
      y = nt-j;
      z = nt-i;
      x2 = x*x;
      y2 = y*y;
      z2 = z*z;
      r2 = x2 + y2 + z2;
      xr[i][j] = x2/r2;
      yr[i][j] = y2/r2;
      zr[i][j] = z2/r2;
      rrr[i][j] = 1.0/(r2*sqrt(r2));
    }
  }

  /* Do the (-x - y + z = nt) face of the octahedron
  !*/


  for( j = nt; j < 2*nt; j++) {
    // printf("%i\n", j);
    for( i = j-nt+1; i < nt; i++) {
      x = -nt-i+j;
      y = nt-j;
      z = nt-i;
      x2 = x*x;
      y2 = y*y;
      z2 = z*z;
      r2 = x2 + y2 + z2;
      xr[i][j] = x2/r2;
      yr[i][j] = y2/r2;
      zr[i][j] = z2/r2;
      rrr[i][j] = 1.0/(r2*sqrt(r2));
    }
  }

  /* Do the (x - y + z = nt) face of the octahedron
  !*/

  for( j = nt; j < 2*nt; j++) {
    // printf("%i\n", j);
    for( i = 1; i <= j-nt; i++) {
      x = -nt-i+j;
      y = -i;
      z = 2*nt-j;
      x2 = x*x;
      y2 = y*y;
      z2 = z*z;
      r2 = x2 + y2 + z2;
      xr[i][j] = x2/r2;
      yr[i][j] = y2/r2;
      zr[i][j] = z2/r2;
      rrr[i][j] = 1.0/(r2*sqrt(r2));
    }
  }

  xr[0][nt] = 0.0;
  yr[0][nt] = 0.0;
  zr[0][nt] = 1.0;
  r2 = nt;
  rrr[0][nt] = 1.0/(r2*r2*r2);

  for( j = 0; j < nt; j++){
      i = 2*nt-j;
      xr[0][i] = xr[0][j];
      yr[0][i] = yr[0][j];
      zr[0][i] = zr[0][j];
      rrr[0][i] = rrr[0][j];
  }

  for( i = 0; i <= nt; i++) {
      xr[nt][nt+i] = xr[i][0];
      yr[nt][nt+i] = yr[i][0];
      zr[nt][nt+i] = zr[i][0];
      rrr[nt][nt+i] = rrr[i][0];
  }

  i = 2*nt;
  for( j = 1; j < nt; j++) {
      xr[nt-j][i] = xr[nt][j];
      yr[nt-j][i] = yr[nt][j];
      zr[nt-j][i] = zr[nt][j];
      rrr[nt-j][i] = rrr[nt][j];
  }
}



void tent(double freq1, \
          double freq2, \
          double freq3, \
          double amp, \
          double *spec, \
          int points, \
          double fstart, \
          double finc) {

// double precision, dimension(0:points-1), intent(inout) :: spec

double df1, df2, f1, f2, top, t;
int p, pmid, pmax, i, j;

double f[3] = {0.0, 0.0, 0.0};
// double precision, dimension(0:2) :: f


f[0] = freq1;
f[1] = freq2;
f[2] = freq3;

for( j = 1; j <= 2; j++) {
    t = f[j];
    i=j-1;
    while(i >= 0 && f[i] > t){
        f[i+1] = f[i];
        i--;
    }
    f[i+1]=t;
}

top = amp*2.0 / (f[2]-f[0]);
p = floor( (f[0]-fstart) / finc );
pmid = floor( (f[1]-fstart) /finc);
pmax = floor( (f[2]-fstart) /finc);
df1 = 0.;
df2 = 0.;
if( (f[1]-f[0]) != 0.) df1 = top / (2.0 * (f[1]-f[0]) );
if( (f[2]-f[1]) != 0.) df2 = top / (2.0 * (f[2]-f[1]) );

if((pmax < points) && (p >= 0)) {
    if(p != pmid) {
        f2 = finc * ( (double)p +1.) + fstart;
        spec[p] += (f2-f[0]) * (f2-f[0]) * df1;
        p++;
        f1 = f2;
        while(p != pmid) {
            f2 = finc * ( (double)p + 1.) + fstart;
            spec[p] += finc * ( (f2-f[0]) + (f1-f[0]) ) * df1;
            p++;
            f1 = f2;
        }
        spec[p] += (f[1]-f1) * ( (f[1]-f[0]) + (f1-f[0]) ) * df1;
    } else {
        spec[p] += (f[1]-f[0]) * top/2.0;
    }

    if(p != pmax) {
        f2 = finc * ( (double)pmid + 1.) + fstart;
        spec[p] += (f2-f[1]) * ( (f[2]-f2) +(f[2]-f[1]) )* df2;
        p++;
        f1 = f2;
        while(p != pmax) {
            f2 = finc * ( (double)p + 1.) + fstart;
            spec[p] += finc * ( (f[2]-f1) + (f[2]-f2) ) * df2;
            p++;
            f1 = f2;
        }
        spec[p] += ( f[2]-f1 ) * (f[2]-f1) * df2;
    } else {
        spec[p] += ( f[2]-f[1] ) * top/2.0;
    }
  }
  // printf("spec %f\n", spec[p]);
}
