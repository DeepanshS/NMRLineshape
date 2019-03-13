
#include "c_array.h" 

// to use calloc, malloc, and free methods
#include <stdlib.h>

// float 1d array
float* createFloat1DArray(int m)
{
    float* values = calloc(m, sizeof(float));
    return values;
}

// double 1d array
double* createDouble1DArray(int m)
{
    double* values = calloc(m, sizeof(double));
    return values;
}

// float 2d matrix
float** createFloat2DMatrix(int m, int n)
{
    float* values = calloc(m*n, sizeof(float));
    float** rows = malloc(n*sizeof(float*));
    for (int i=0; i<n; ++i)
    {
        rows[i] = values + i*m;
    }
    return rows;
}

// double array
double** createDouble2DMatrix(int n, int m)
{
  double* values = calloc(m*n, sizeof(double));
    double** rows = malloc(n*sizeof(double*));
    for (int i=0; i<n; ++i)
    {
        rows[i] = values + i*m;
    }
    return rows;
}

void destroyFloat1DArray(float* arr)
{
    free(arr);
}

void destroyDouble1DArray(double* arr)
{
    free(arr);
}

void destroyFloat2DMatrix(float** arr)
{
    free(*arr);
    free(arr);
}
void destroyDouble2DMatrix(double** arr)
{
    free(*arr);
    free(arr);
}

// test modify array
void modify2DMatrix(double **arr, int n, int m)
{
  int i, j;
  for( i = 0; i < n; i++) {
    for( j = 0; j < m; j++) {
      arr[i][j] = i+j;
    }
  }
}

void modify1DArray(double *arr, int m)
{
  int i;
  for( i = 0; i < m; i++) {
      arr[i] = i;
    }
}

// // main 
// int main() {
//   int i, j, m, n;
//   m=13;
//   n=2;
//   double** arr = createDouble2DMatrix(n,m);
//   // arr = array(3,3);
//   for ( i = 0; i < n; i++ ) {
//     for ( j = 0; j < m; j++ ) {
//       arr[i][j] = 1.0;
//       printf("%f\n", arr[i][j]);
//     }
//   }
//   printf("\n new \n");
//   modify2DMatrix(arr, n, m);

//   for ( i = 0; i < n; i++ ) {
//     for ( j = 0; j < m; j++ ) {
//       printf("%f\n", arr[i][j]);
//     }
//   }
//   destroyDouble2DMatrix(arr);



//   double* arr1 = createDouble1DArray(m);
//   // arr = array(3,3);
//   for ( i = 0; i < m; i++ ) {
//       arr1[i] = 1.0;
//       printf("%f\n", arr1[i]);
//     }
  
//   printf("\n new \n");
//   modify1DArray(arr1, m);

//   for ( i = 0; i < m; i++ ) {
//       printf("%f\n", arr1[i]);
//     }

//   destroyDouble1DArray(arr1);

//   return 0;
// }
