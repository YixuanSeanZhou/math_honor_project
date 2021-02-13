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
import matplotlib.pyplot as plt
import progressbar
from monomial import mono_poly
from chebyshev import cheby_first_kind

def condition_num(A, norm = None):
    '''
    Calculating the condition number
    '''
    min_dim = min(A.shape)
    if A.rank() != min_dim:
        return -1 # since condition number is geq 1, this indicate it is not full rank
    else:
        npA = np.array(A).astype(np.float64)
        cond = np.linalg.norm(np.linalg.pinv(npA)) * np.linalg.norm(npA)
        # cond = A.pinv().norm() * A.norm()
        return cond

def gen_mmoment_matrix(base_vec):
    m_mtx = base_vec * spmtx.transpose(base_vec)
    for i in range(m_mtx.shape[0]):
        for j in range(m_mtx.shape[1]):
            m_mtx[i, j] = sp.expand(m_mtx[i, j])
    
    return m_mtx

def a_vec(m_mtx, base_type, basis, num_var):
    # print("Moment Matrix Shape:")
    # print(m_mtx.shape)
    # print()
    a = []
    for i in range(0, m_mtx.shape[0]):
        for j in range(i, m_mtx.shape[1]):
            #print("Time Extracting Map")
            #start = time.process_time()
            coeff = base_type.c_extract_map(m_mtx[i, j], basis, num_var)
            #print(time.process_time() - start)
            if i != j:
                coeff *= 2
            a.append(coeff)
    return a

def A_mtx(m_mtx, base_type, base, num_var):
    A = []
    #with progressbar.ProgressBar(max_value=len(base)) as bar:
    for b in base:
        A.append(a_vec(m_mtx, base_type, b, num_var))
        #bar.update(i)
    return spmtx(A)

def experiment(m_mtx_base, poly_base, deg, num_var):
    if deg % 2 != 0:
        print("No need to experiment polynomial with even degree")
        return 0

    #print('calculating moment matrix')
    r = m_mtx_base(deg = deg // 2, num_var = num_var)
    m_mtx = gen_mmoment_matrix(r.base_vec)
    #print('calculating A matrix')
    base = poly_base(deg=deg, num_var = num_var)
    A = A_mtx(m_mtx, base_type=base, base=base.base, num_var=base.num_var)
    #print('calculating condition number')
    c_num = condition_num(A)
    # print('found condition num')
    return c_num

if __name__ == '__main__':
    conds = []
    x = []
    #with progressbar.ProgressBar(max_value=3) as bar:
    for i in range(1, 3):
        conds.append(experiment(mono_poly, cheby_first_kind, i*2, 2))
        #bar.update(i+1)
        x.append(i*2)
        # print(round(i * 100 / 3), 10)
    print(conds)
    plt.plot(x, conds)
    plt.show