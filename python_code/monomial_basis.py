class mono_poly:
    '''
    The monomial polynomial basis class
    data_field:
        var_list: A list of symbols for different variables
        num_var: The number of variables
        degree: The total degree of the polynomial
        base: A list of terms that the basis consists
        base_vec: A sympy matrix (vector) of each element in the basis.
        coeff: A list of coeffs related to each basis
    '''
    
    
    def _gen_terms(self, var_list, total_degree, term):
        '''
        Description:
            Generate all the terms in a basis of the polynomial space consisted of monomial polynomials.
        Reference:
            None
        Input:
            var_list --- a deque of symbols in the monomials
            total_degree --- the maximun degree of the polynomial
            term --- A list of terms in the basis, start with [1] when being called
        '''
        terms = []
        if len(var_list) == 1:
            term *= var_list[0] ** total_degree
            terms.append(term)
            return terms
        elif total_degree == 0:
            term *= 1
            terms.append(term)
            return terms
        else:
            for i in range(total_degree, -1, -1):
                var_list_further = copy.deepcopy(var_list)
                var = var_list_further.popleft()
                term_further = term * var ** i
                terms += self._gen_terms(var_list_further, total_degree - i, term_further)
            return terms
    

    def __init__(self, deg, num_var, coeff=None):
        '''
        Description:
            Initalize a basis of the polynomail space by the first kind chebyshev polynomials.
        Input:
            deg --- The max degree of the polynomail space
            num_var --- number of variables in the polynomial space
        '''
        self.degree = deg
        self.num_var = num_var
        var_list = deque()
        for i in range(num_var):
            var_list.append(syms('x_' + str(i)))
        self.var_list = var_list
        terms = []
        for i in range(deg, -1, -1):
            terms += self._gen_terms(self.var_list, i, 1)
        self.base = terms
        self.base_vec = spmtx(terms)
        if coeff == None:
            pass

        self.coeff = coeff
    
    
    def c_extract_map(self, poly, basis, num_var=0):
        '''
        Description:
            Extract the coefficients of an element in a monomial basis from the input polynomial
        Input:
            deg --- The max degree of the polynomail space
            num_var --- number of variables in the polynomial space
            num_var --- not really needed
        '''
        p = sp.expand(poly)
        c = p.coeff(basis)
        if len(c.free_symbols) == 0:
            return c
        else:
            return sp.core.numbers.Zero()