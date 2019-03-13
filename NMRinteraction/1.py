from .powder import lineshape, setuppowder2
import numpy as np
from pymatgen.analysis import nmr

"""
    Function involved in generation of NMR line shapes
    
    Author : Deepansh Srivastava
    email : srivastava.89@osu.edu
"""

def get_iso_zeta_eta(tensors):
    """
        Returns the isotropic, anisotropic and asymmetry parameters of a second rank
        tensor using the Haeberlen convension.
        
    """
    
    tensors= np.asarray([[tensor.haeberlen_values.sigma_iso,
                          tensor.haeberlen_values.zeta,
                          tensor.haeberlen_values.eta] for tensor in tensors])
    return tensors[:,0], tensors[:,1], tensors[:,2]



def create_dimension_vector(dimension):
    """
        This method create the dimension vector. Units are not yet supported
        The input argument is:
        
        dimension  : a dictionary with the following acceptable keywords
            number_of_points  : the number of points along the frequency axis
            sampling_interval : the sampling interval along the frequency axis
            reference_offset  : the reference offset along the frequency axis
    """
    number_of_points = dimension['number_of_points']
    sampling_interval = dimension['sampling_interval']
    reference_offset = dimension['reference_offset']

    fwidth = np.float64(number_of_points * sampling_interval)
    m = np.int(number_of_points)

    if m % 2 == 0:
        fstart = -0.5*fwidth + reference_offset
    else:
        fstart = -0.5*(m-1)*fwidth/m + reference_offset

    freq = np.arange(m)*sampling_interval + fstart

    return freq



def csa_zg_static(tensors, freq_dimension, nt=64):
    
    """
        This method generates and returns a static nuclear shielding spectrum.
        The input arguments are:
        
        tensors  : a list of 'pymatgen.analysis.nmr.ChemicalShielding' tensor object
        freq_dimension = a dimension dictionary with the following acceptable keywords
            number_of_points  : the number of points along the frequency axis
            sampling_interval : the sampling interval along the frequency axis
            reference_offset  : the reference offset along the frequency axis
        nt : number of triangles used in the interpolation scheme
        
        The NMR powder pattern is generated using powder interpolation scheme
        of Alderman, Solum and Grant, J. Chem. Phys, 84, 1985.
        DOI : 10.1063/1.450211
    """
    
    iso, zeta, eta = get_iso_zeta_eta(tensors)
    shape = iso.shape
    
    sampling_interval = freq_dimension['sampling_interval']
    index = np.where(zeta == 0)
    zeta[index] = sampling_interval*1e-8
    eta[index] = 0.0


#    if (np.any(eta > 1)):
#        print ('error: eta value greater than 1 encountered')
#        return
#
#    if (np.any(eta < -1)):
#        print ('error: eta value less than -1 encountered')
#        return


    nt = np.int(nt)
    xr, yr, zr, powamp = setuppowder2(nt)

    freq = create_dimension_vector(freq_dimension)

    fwidth = freq[-1] - freq[0]
    fstart = freq[0] -0.5 * sampling_interval

    output = lineshape(freq.size, fstart, fwidth, zeta, eta, iso, \
                           xr, yr, zr, powamp)

    # Normalization
    sumNorm = output[:,0].sum(axis=0)
    output = output/sumNorm
    return freq, output.reshape(((freq.size,) + shape))



def csa_maf(tensors, iso_dimension, pi_by_2_dimension, nt=64):

    pi_by_2_freq, output = csa_zg_static(tensors, pi_by_2_dimension, nt=64)
    iso_freq = create_dimension_vector(iso_dimension)
    iso, zeta, eta = get_iso_zeta_eta(tensors)

    

    








def spinningSideband():
    pass


#def CzjzekDistribution(sigma, ansioInc, ansioPoints, asymPoints, iso=None,\
#                       interaction=None, freqSamplingInterval=None, freqReferenceOffset=None, \
#                       freqPoints=None):
#
#
#    ansioPoints = np.int(ansioPoints)
#    asymPoits = np.int(asymPoints)
#
#    aniso = (np.arange(ansioPoints, dtype=np.float64) - ansioPoints/2)*ansioInc
#    asym = np.arange(asymPoints, dtype=np.float64)/(asymPoints-1)
#
#    z, e = np.meshgrid(aniso, asym, indexing='ij')
#
#    z2 = z * z
#    e2 = e * e
#    sigma2 = sigma * sigma
#    sigma5 = sigma2**2 * sigma
#    S2 = z2*(1.0 + e2/3.0)
#    rho = (z2**2 * e) * (1.0 - e2/9.0) * np.exp(-(S2/(2.0*sigma2))) / (np.sqrt(2.0*np.pi) * sigma5)
#
#    if interaction is None:
#        return aniso, asym, rho
#
#    iso = np.ones(rho.shape) * iso
#    freqPoints = np.int(freqPoints)
#    if interaction == 'nsa':
#
#        freq, lineshape = static(freqPoints, freqSamplingInterval, \
#                                 freqReferenceOffset, z, e, iso, nt=32)
#
#        czjzekLineshape = (lineshape * rho).sum(axis=(1,2))
#
#        return aniso, asym, rho, freq, czjzekLineshape
