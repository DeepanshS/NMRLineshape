
#include "CSA_static_lineshape.h"
#include <stdio.h>

void lineshape_csa_static(double * spec, \
                          int m, \
                          int nt, \
                          double fstart, \
                          double fwidth, \
                          double iso, \
                          double aniso, \
                          double eta, \
                          int npros) {

  int i,j;
  double** xr;
  xr = createDouble2DMatrix(nt+1, 2*nt+1);
  double** yr = createDouble2DMatrix(nt+1, 2*nt+1);
  double** zr = createDouble2DMatrix(nt+1, 2*nt+1);
  double** powfreq = createDouble2DMatrix(nt+1, 2*nt+1);
  double** powamp = createDouble2DMatrix(nt+1, 2*nt+1);

  double finc, sxx, syy, szz, amp1, amp2, sqrt3;

  SetupPowder2(nt, xr, yr, zr, powamp);

  finc = fwidth/m;
  sqrt3 = sqrt(3.0);

  sxx = iso -0.5 * aniso* (1.0 + eta);
  syy = iso -0.5 * aniso* (1.0 - eta);
  szz = iso + aniso;


  for(i=0; i<nt+1; i++){
    for(j=0; j<2*nt+1; j++){
      powfreq[i][j] = sxx*xr[i][j] + syy*yr[i][j] + szz*zr[i][j];
    }
  }

 /* Interpolate between frequencies by setting up tents */

  for (i=0; i<=nt-1; i++){
    for (j=0; j<=nt-1; j++){
      amp1 = powamp[i+1][j] + powamp[i][j+1] + powamp[i][j];
      amp2 = powamp[i+1][j] + powamp[i][j+1] + powamp[i+1][j+1];

      tent(powfreq[i+1][j], powfreq[i][j+1], powfreq[i][j], \
                  amp1, spec, m, fstart, finc);
      tent(powfreq[i+1][j], powfreq[i][j+1], powfreq[i+1][j+1], \
                  amp2, spec, m, fstart, finc);
    }
  }

  for (i=0; i<=nt-1; i++){
    for (j=nt; j<=2*nt-1; j++){
      amp1 = powamp[i][j] + powamp[i+1][j+1] + powamp[i+1][j];
      amp2 = powamp[i][j] + powamp[i+1][j+1] + powamp[i+1][j];
      tent(powfreq[i][j], powfreq[i+1][j+1], powfreq[i+1][j], \
                  amp1, spec, m, fstart, finc);
      tent(powfreq[i][j], powfreq[i+1][j+1], powfreq[i+1][j], \
                  amp2, spec, m, fstart, finc);
    }
  }
  
  // for ( i = 0; i < 128; i++ ) {
  //     printf("%f\n", spec[i]);
  //   } 
  destroyDouble2DMatrix(xr);
  destroyDouble2DMatrix(yr);
  destroyDouble2DMatrix(zr);
  destroyDouble2DMatrix(powfreq);
  destroyDouble2DMatrix(powamp);
}
