'''
This file contains the access to all the polynomial basis.
'''

from .chebyshev import cheby_first_kind, cheby_second_kind
from .legendre import legendre
from .monomial import mono_poly

basis = {
    'monomial': mono_poly,
    'legendre': legendre,
    'cheby_first_kind': cheby_first_kind,
    'cheby_second_kind': cheby_second_kind
}