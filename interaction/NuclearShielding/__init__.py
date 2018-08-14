from .powder import lineshape, setuppowder2
import numpy as np
from pymatgen.analysis import nmr

def static_zg(tensors, number_of_points, sampling_interval, reference_offset,
              nt=64, haeberlen=True):
    
    """
        This method generates and returns a static nuclear shielding spectrum.
        The input arguments are:
        
        tensors  : a list of 'pymatgen.analysis.nmr.ChemicalShielding' tensor object
        number_of_points  : the number of points along the frequency axis
        sampling_interval : the sampling interval along the frequency axis
        reference_offset  : the reference offset along the frequency axis
        nt : number of triangles used in the interpolation scheme
        
        The NMR powder pattern is generated using powder interpolation scheme
        of Alderman, Solum and Grant, J. Chem. Phys, 84, 1985.
        DOI : 10.1063/1.450211
        
        Author : Deepansh Srivastava
    """
    
    tensors  = np.asarray([[tensor.haeberlen_values.sigma_iso,
                            tensor.haeberlen_values.zeta,
                            tensor.haeberlen_values.eta] for tensor in tensors])
                            
    iso, zeta, eta = tensors[:,0], tensors[:,1], tensors[:,2]
#    iso += reference_offset
#    print (iso, zeta, eta)
#    aniso = np.asarray(aniso, dtype=np.float64)
    shape = iso.shape
    
    index = np.where(zeta == 0)
    zeta[index] = sampling_interval*1e-8
    eta[index] = 0.0
    
#
#    aniso = aniso.ravel()
#    if iso is None:
#        iso = np.zeros(aniso.size, dtype=np.float64)
#    else:
#        iso = np.asarray(iso, dtype=np.float64).ravel()
#    eta = np.asarray(eta, dtype=np.float64).ravel()

    if (np.any(eta > 1)):
        print ('error: eta value greater than 1 encountered')
        return
    
    if (np.any(eta < -1)):
        print ('error: eta value less than -1 encountered')
        return
    
    fwidth = np.float64(number_of_points * sampling_interval)
    m = np.int(number_of_points)
    nt = np.int(nt)

    xr, yr, zr, powamp = setuppowder2(nt)

    if m % 2 == 0:
        fstart = -0.5*fwidth + reference_offset
    else:
        fstart = -0.5*(m-1)*fwidth/m + reference_offset

    freq = np.arange(m)*sampling_interval + fstart

    fstart = fstart -0.5 * sampling_interval

    output = lineshape(m, fstart, fwidth, zeta, eta, iso, \
                           xr, yr, zr, powamp)

#    print (output.shape)
    # Normalization
    sumNorm = output[:,0].sum(axis=0)
#    print (sumNorm)
    output = output/sumNorm
    return freq, output.reshape(((m,) + shape))


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
