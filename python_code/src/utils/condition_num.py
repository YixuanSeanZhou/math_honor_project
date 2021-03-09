import numpy as np

def condition_num(A, norm = None):
    '''
    Given A a sympy matrix, calculate the condition number of it.
    Author:
        Yixuan Zhou
    '''

    min_dim = min(A.shape)
    if A.rank() != min_dim:
        return -1 # since condition number is geq 1, this indicate it is not full rank
    else:
        npA = np.array(A).astype(np.float64)
        cond = np.linalg.norm(np.linalg.pinv(npA)) * np.linalg.norm(npA)
        # cond = A.pinv().norm() * A.norm()
        return cond