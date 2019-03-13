
#include <math.h>
#include <string.h>

extern void SetupPowder2(int nt, \
                  double **xr, \
                  double **yr, \
                  double **zr, \
                  double **rrr);

extern void tent(double freq1, \
          double freq2, \
          double freq3, \
          double amp, \
          double *spec, \
          int points, \
          double fstart, \
          double finc);