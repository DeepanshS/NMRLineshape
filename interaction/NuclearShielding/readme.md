The file powder.f90 contains the code for powder interpolation scheme by Alderman, Solum and Grant, J. Chem. Phys, 84, 1985. DOI : [10.1063/1.450211](https://aip.scitation.org/doi/10.1063/1.450211)

To compile the fortran, execute the following in the command line. A fortran compiler must be installed for this to work.

`f2py -m powder -c powder.f90 --f90flags='-fopenmp' -lgomp`