
#cdef extern from "stdint.h":
#    ctypedef unsigned long long uint64_t
#    ctypedef long long int64_t
#

from cpython cimport array
cimport c_CSA_static_lineshape as clib
import numpy as np
from numpy import abs
from collections import namedtuple

Haeberlen = namedtuple('Haeberlen', ['isotropic', 'anisotropic', 'asymmetry'])

class Tensor:
	def __init__(self, tensor):
		self.full_tensor = tensor

	@property
	def Haeberlen_convention(self):
		return self.get_iso_aniso_eta_using_Haeberlen_convention()

	def get_iso_aniso_eta_using_Haeberlen_convention(self):
		eig = np.linalg.eigvalsh(self.full_tensor)
		if abs(eig[0]) >= abs(eig[1]) and abs(eig[0]) >= abs(eig[2]):
			zeta = eig[0]
			eta = abs((eig[1] - eig[2])/zeta)
		elif abs(eig[1]) >= abs(eig[0]) and abs(eig[1]) >= abs(eig[2]):
			zeta = eig[1]
			eta = abs((eig[0] - eig[2])/zeta)
		else:
			zeta = eig[2]
			eta = abs((eig[1] - eig[0])/zeta)
		iso = eig.sum()/3

		return Haeberlen(iso, zeta, eta)


class MRSpin:

	__slots__ = (
		'_isotope',
		'_shielding_tensor'
	)

	def __init__(self, isotope='1H',
				shielding_tensor=None):
		"""
			Create a new nuclear isotope.

				>>> from MRSystem import MRSpin
				>>> Si = MRSpin('29Si')

		"""
		self._isotope = isotope
		if shielding_tensor is not None:
			self._shielding_tensor = Tensor(shielding_tensor)

	@property
	def shielding_tensor(self):
		"""
		Set the nuclear shielding tensor of the nuclear isotope.
		
			>>> print(Si.shielding_tensor)

			>>> Si.shielding_tensor = np.random.rand(9).reshape(3,3)
		"""
		return self._shielding_tensor

	@shielding_tensor.setter
	def shielding_tensor(self, tensor):
		tensor = np.asarray(tensor)
		if tensor.shape != (3,3):
			raise Exception(
				'A 3 x 3 tensor is required, given {0} x {1}.'.format(
					tensor.shape[0], tensor.shape[1]
				)
			)
		self._shielding_tensor = Tensor(tensor)


	def spectrum(self, number_of_points,
				 start_frequency, 
				 frequency_bandwidth, npros=1):

		"""
		Computes the NMR spectrum of isotope on the given frequency range.

		The frequencies at which the spectrum is computed is evaluted as
		``freq = np.arange(number_of_points)/number_of_points * frequency_bandwidth + start_frequency``

		:attr:number_of_points: The number of points in the frequency dimension.
		:attr:start_frequency: The start frequency.
		:attr:frequency_bandwidth: The spectral width of the frequency spectrum.

		:returns:freq: The frequency numpy array.
		:returns:amp: The amplitudes of the spectrum at the frequency

			
		"""

		freq = np.arange(number_of_points)/number_of_points * \
					frequency_bandwidth + start_frequency

		nt = 32
		cdef array.array amp = array.array('d', np.zeros(number_of_points))

		iso, aniso, eta = self.shielding_tensor.Haeberlen_convention

		clib.lineshape_csa_static(amp.data.as_doubles, \
								number_of_points, nt, \
								start_frequency, frequency_bandwidth, \
								iso, aniso, eta, 1)
		return freq, amp