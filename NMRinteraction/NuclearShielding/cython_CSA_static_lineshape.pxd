cdef extern from "CSA_static_lineshape.h":
    void lineshape_csa_static(double * spec, \
                                int m, \
                                int nt, \
                                double fstart, \
                                double iso, \
                                double fwidth, \
                                double aniso, \
                                double eta, \
                                int npros) 
