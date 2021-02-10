# Reading Notes for Polynomial bases on the numerical solution of the multivariate discrete moment problem

## Univariate Chebyshev polynomials

### First Kind

$$
T_n(cos(\theta)) = cos(n\theta) \quad \quad T_n(\frac{x + x^{-1}}{2}) = \frac{x^n + x^{-n}}{2}
$$

The second inequality can be understand if writing $x = e^{i\theta}$ and using the fact that $cos(n\theta) = \frac{1}{2}(e^{in\theta} + e^{-in\theta})$

### Second Kind

$$
U_n(cos(\theta)) = \frac{sin((n+1)\theta)}{sin(\theta)} \quad \quad U_n(\frac{x + x^{-1}}{2}) = \frac{x^{n + 1} - x^{-n-1}}{x - x^{-1}} = x^n + x^{n-2} + \cdots + x^{2-n} + x^{-n}
$$

The second will be understood using $sin(n\theta) = \frac{1}{2}(e^{in\theta} - e^{-in\theta})$





### Bi-variate First Kind Chebyshev

$T_{0,0} = 6, T_{1, 0} = X, T_{0, 1} = Y, T_{1, 1} = \frac{X Y -12}{4} $

$2T_{a+2, 0} ={XT_{a + 1, 0} - 4T_{a, 1}} $

$2T_{0, b+2} = {YT_{0, b+1} - 4T_{1, b}}$

$2T_{a+1, b} = {XT_{a, b} - 2T_{a, b+1} - 2T_{a, b-1}}$

$2T_{a, b+1} = {YT_{a,b} - 2T_{a+1, b-1} -2T_{a-1, b-1}}$



### Bi-variate Second Kind Chebyshev

$U_{0, 0} = 1, U_{1, 0} = \frac{1}{2}X, U_{0, 1} = \frac{1}{2}Y$

$2U_{a+1, 0} = XU_{a, 0} - 2U_{a-1, 1}$ A

$2U_{0, b+1} = YU_{0,b} - 2U_{a+1, b-1}$ 

$2U_{a+1, b} = XU_{a, b} - 2U_{a-1, b+1} - 2U_{a, b-1}$

$2U_{a, b+1} = YU_{a, b} - 2U_{a+1, b -1} - 2U_{a-1, b}$



## Bernstein

Let $H = \{(a_1, ..., a_s) | 0 \leq a_j, a_j integer, a_1 + ... + 1_s = m, j = 1,...,s\} $











