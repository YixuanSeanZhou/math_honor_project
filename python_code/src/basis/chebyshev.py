import sympy as sp
from sympy import Matrix as spmtx
from sympy import *
from sympy import symbols as syms
from sympy.utilities.lambdify import lambdify, lambdastr
import math
from collections import deque
import copy
from copy import deepcopy
import random
import numpy as np
import time
from scipy import integrate as sci_int


class cheby_first_kind:
    '''
    The chebyshev first kind polynomial basis class
    data_field:
        var_list: A list of symbols for different variables
        num_var: The number of variables
        degree: The total degree of the polynomial
        base: A list of terms that the basis consists
        base_vec: A sympy matrix (vector) of each element in the basis.
        coeff: A list of coeffs related to each basis
        norm: A dictionary of norm of an element in basis
    '''
    def _gen_terms_biv(self, total_degree):
        '''
        Description:
            Generate all the terms in a bases of bivaraite polynomials using
            bivariate chebyshev polynomial of the first kind
        Reference:
             The construction of multivariate chebyshev is based on what Gergely Mádi-Nagy proposed in his
            "Polynomial bases on the numerical solution of the multivariate discrete moment problem"
        Input:
            total_degree --- the maximun degree of the polynomial
        '''
        var_list = []
        for i in range(len(self.var_list)):
            var_list.append(self.var_list.popleft())
        self.var_list = deque()
        self.var_list.append(var_list[0])
        terms_x_0 = self._gen_terms_uni(total_degree)
        self.var_list.popleft()
        
        self.var_list.append(var_list[1])
        terms_x_1 = self._gen_terms_uni(total_degree)
        self.var_list.popleft()
        
        for var in var_list:
            self.var_list.append(var)
        terms = []
        for order_1 in range(len(terms_x_1)):
            for order_0 in range(len(terms_x_0) - order_1):
                terms.append(terms_x_0[order_0] * terms_x_1[order_1])
                # terms.append(sp.expand(x_0 * x_1))
        return terms
        
    
    def _gen_terms_uni(self, total_degree):
        '''
        Description:
            Generate all the terms in a bases of univaraite polynomials using
            univariate chebyshev polynomial of the first kind
        Reference:
            https://en.wikipedia.org/wiki/Chebyshev_polynomials
        Input:
            total_degree --- the maximun degree of the polynomial
        '''
        if total_degree == 0:
            return [1]
        T = [1, self.var_list[0]]
        for i in range(2, total_degree + 1):
            n_term = 2 * self.var_list[0] * T[i-1] - T[i-2]
            n_term = sp.simplify(n_term)
            n_term = sp.expand(n_term)
            # print(n_term)
            T.append(n_term)
        return T

    
    def __init__(self, deg, num_var, alpha=0, beta=0, coeff=None):
        '''
        Description:
            Initalize a basis of the polynomail space by the first kind chebyshev polynomials.
        Input:
            deg --- The max degree of the polynomail space
            num_var --- number of variables in the polynomial space
        '''
        if num_var > 2:
            raise ValueError("Only support 2 variable max")
        
        self.degree = deg
        self.num_var = num_var
        
        self.var_list = deque()
        for i in range(num_var):
            self.var_list.append(syms('x_' + str(i)))
        
        if num_var == 1:
            terms = self._gen_terms_uni(self.degree)
        elif num_var == 2:
            terms = self._gen_terms_biv(self.degree)

        self.base = terms
        self.base_vec = spmtx(terms) # arrange the terms in a vector format
        
        if coeff == None:
            pass
        self.coeff = coeff
        
        self.norm = dict()
        i = 0
        #with progressbar.ProgressBar(max_value=len(self.base)) as bar:
        for b in self.base:
            self.norm[b] = self._base_norm(b, num_var)
            i+=1
                #bar.update(i)
        
    def _base_norm(self, b, num_var):
        '''
        Description:
            Pre-calculate the norm of an element in the basis using the corresponding inner product.
        Input:
            b --- an element in the basis
            num_var --- univariate vs bivariate
        '''
        if num_var > 2:
            raise ValueError("Only support 2 variable max")
        if num_var == 1:
            weight = sqrt(1 - self.var_list[0] ** 2)
            f = lambdify(self.var_list[0], (b * b) / weight)
            r = sci_int.quad(f, -1, 1, epsabs=1e-4, epsrel=1e-4, limit=15)[0]
            if abs(r) < 1e-4:
                return 0
            else:
                return round(r, 5)
        if num_var == 2:
            weight = sqrt(1 - self.var_list[0] ** 2) * sqrt(1 - self.var_list[1] ** 2)
            f = lambdify(self.var_list, b * b / weight)
            r = sci_int.nquad(f, [[-1,1],[-1, 1]], opts=[{'epsabs':1e-3, 'epsrel':1e-3, 'limit': 15}, 
                                                         {'epsabs':1e-3, 'epsrel':1e-3, 'limit': 15}])[0]
            if abs(r) < 1e-4:
                return 0
            else:
                return round(r, 5)
    
    def c_extract_map(self, poly, basis, num_var):
        '''
        Description:
            Using orthogonality to extract the coefficient of a vector in the basis in the input polynomial.
            The basis should be generated by the constructor of this class.
        Reference:
            "Polynomial bases on the numerical solution of the multivariate discrete moment problem"
        Input:
            poly --- A given polynomial
            basis --- An element in the first kind chebyshve basis 
            num_var --- Univariate vs Bivariate
        '''
        if num_var > 2:
            raise ValueError("Only support 2 variable max")
        if num_var == 1:
            weight = sqrt(1 - self.var_list[0] ** 2)
            f = lambdify(self.var_list[0], (poly * basis) / weight)
            r = sci_int.quad(f, -1, 1, epsabs=1e-5, epsrel=1e-5, limit=20)[0]
            if abs(r) < 1e-5:
                return 0
            else:
                return round(r / self.norm[basis], 5)
        if num_var == 2:
            weight = sqrt(1 - self.var_list[0] ** 2) * sqrt(1 - self.var_list[1] ** 2)
            f = lambdify(self.var_list, poly * basis / weight)

            # points = [-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

            r = sci_int.nquad(f, [[-1,1],[-1, 1]], opts=[{'epsabs':1e-3, 'epsrel':1e-3, 'limit': 15}, 
                                                         {'epsabs':1e-3, 'epsrel':1e-3, 'limit': 15}])[0]
            if abs(r) < 1e-4:
                return 0
            else:
                return round(r / self.norm[basis], 5)


class cheby_second_kind:
    '''
    The chebyshev first kind polynomial basis class
    data_field:
        var_list: A list of symbols for different variables
        num_var: The number of variables
        degree: The total degree of the polynomial
        base: A list of terms that the basis consists
        base_vec: A sympy matrix (vector) of each element in the basis.
        coeff: A list of coeffs related to each basis
    '''
    def _gen_terms_biv(self, total_degree):
        '''
        Description:
            Generate all the terms in a bases of bivaraite polynomials using
            bivariate chebyshev polynomial of the second kind
        Reference:
             The construction of multivariate chebyshev is based on what Gergely Mádi-Nagy proposed in his
            "Polynomial bases on the numerical solution of the multivariate discrete moment problem"
        Input:
            total_degree --- the maximun degree of the polynomial
        '''
        var_list = []
        for i in range(len(self.var_list)):
            var_list.append(self.var_list.popleft())
        self.var_list = deque()
        self.var_list.append(var_list[0])
        terms_x_0 = self._gen_terms_uni(total_degree)
        self.var_list.popleft()
        
        self.var_list.append(var_list[1])
        terms_x_1 = self._gen_terms_uni(total_degree)
        self.var_list.popleft()
        
        for var in var_list:
            self.var_list.append(var)
        terms = []
        for order_1 in range(len(terms_x_1)):
            for order_0 in range(len(terms_x_0) - order_1):
                terms.append(terms_x_0[order_0] * terms_x_1[order_1])
                # terms.append(sp.expand(x_0 * x_1))
        return terms
    
    
    def _gen_terms_uni(self, total_degree):
        '''
        Description:
            Generate all the terms in a bases of univaraite polynomials using
            univariate chebyshev polynomial of the second kind
        Reference:
            https://en.wikipedia.org/wiki/Chebyshev_polynomials
        Input:
            total_degree --- the maximun degree of the polynomial
        '''
        if total_degree == 0:
            return [1]
        U = [1, 2 * self.var_list[0]]
        for i in range(2, total_degree + 1):
            n_term = 2 * self.var_list[0] * U[i-1] - U[i-2]
            n_term = sp.simplify(n_term)
            n_term = sp.expand(n_term)
            U.append(n_term)
        return U
    

    def __init__(self, deg, num_var, alpha=0, beta=0, coeff=None):
        '''
        Description:
            Initalize a basis of the polynomial space by the second kind chebyshev polynomials.
        Input:
            deg --- The max degree of the polynomail space
            num_var --- number of variables in the polynomial space
        '''
        if num_var > 2:
            raise ValueError("Only support 2 variable max")
        
        self.degree = deg
        self.num_var = num_var
        
        self.var_list = deque()
        for i in range(num_var):
            self.var_list.append(syms('x_' + str(i)))
        
        if num_var == 1:
            terms = self._gen_terms_uni(self.degree)
        elif num_var == 2:
            terms = self._gen_terms_biv(self.degree)

        self.base = terms
        self.base_vec = spmtx(terms) # arrange the terms in a vector format
        if coeff == None:
            pass
        self.coeff = coeff

        self.norm = dict()
        i = 0
        #with progressbar.ProgressBar(max_value=len(self.base)) as bar:
        for b in self.base:
            self.norm[b] = self._base_norm(b, num_var)
                #bar.update(i)
                #i+=1
    
    
    def _base_norm(self, b, num_var):
        '''
        Description:
            Pre-calculate the norm of an element in the basis using the corresponding inner product.
        Input:
            b --- an element in the basis
            num_var --- univariate vs bivariate
        '''
        if num_var > 2:
            raise ValueError("Only support 2 variable max")
        if num_var == 1:
            weight = sqrt(1 - self.var_list[0] ** 2)
            f = lambdify(self.var_list[0], (b * b) * weight)
            r = sci_int.quad(f, -1, 1, epsabs=1e-4, epsrel=1e-4, limit=15)[0]
            if r < 1e-4:
                return 0
            else:
                return round(r, 5)
        if num_var == 2:
            weight = sqrt(1 - self.var_list[0] ** 2) * sqrt(1 - self.var_list[1] ** 2)
            f = lambdify(self.var_list, b * b * weight)
            r = sci_int.nquad(f, [[-1,1],[-1, 1]], opts=[{'epsabs':1e-4, 'epsrel':1e-4, 'limit': 15}, 
                                                         {'epsabs':1e-4, 'epsrel':1e-4, 'limit': 15}])[0]
            if r < 1e-4:
                return 0
            else:
                return round(r, 5)
    
    def c_extract_map(self, poly, basis, num_var):
        '''
        Description:
            Using orthogonality to extract the coefficient of a vector in the basis in the input polynomial.
            The basis should be generated by the constructor of this class.
        Reference:
            "Polynomial bases on the numerical solution of the multivariate discrete moment problem"
        Input:
            poly --- A given polynomial
            basis --- An element in the first kind chebyshve basis 
            num_var --- Univariate vs Bivariate
        '''
        if num_var > 2:
            raise ValueError("Only support 2 variable max")
        if num_var == 1:
            weight = sqrt(1 - self.var_list[0] ** 2)
            f = lambdify(self.var_list[0], (poly * basis) * weight)
            r = sci_int.quad(f, -1, 1, epsabs=1e-5, epsrel=1e-5, limit=20)[0]
            if abs(r) < 1e-5:
                return 0
            else:
                return round(r / self.norm[basis], 5)
        if num_var == 2:
            weight = sqrt(1 - self.var_list[0] ** 2) * sqrt(1 - self.var_list[1] ** 2)
            f = lambdify(self.var_list, poly * basis * weight)
            r = sci_int.nquad(f, [[-1,1],[-1, 1]], opts=[{'epsabs':1e-4, 'epsrel':1e-4, 'limit': 15}, 
                                                         {'epsabs':1e-4, 'epsrel':1e-4, 'limit': 15}])[0]
            if abs(r) < 1e-4:
                return 0
            else:
                return round(r / self.norm[basis], 5)