# Math Honor Project

Author: [Yixuan Zhou](http://yixuanseanzhou.github.io/)
Supervisor: [Mareike Dressler](https://web.maths.unsw.edu.au/~mdressler/)

## Getting Started
The project require `python3.7+` and the installation of `jupyter notebook`.

To install the dependencies using the `requirements.txt` file, do
```
pip install -r requirements.txt
```

## About

The project is about calculating the stability of the linear systems for various bases combination when executing the process of comparing of coefficients to verify whether a polynomial can be written in a sum of squares. 


## Usage

First navigate to `python_code` directory. Then one can run the `exp_runner.py` with different configurations listed as follows: 
- `-p` specify the polynomial basis of the problem, this should be one of the following: `cheby_first_kind`, `cheby_second_kind`, `jacobi`, `legendre`, `monomial`.
- `-m` specify the moment matrix basis that is used to check sum of squares, it should be one of the following: `cheby_first_kind`, `cheby_second_kind`, `jacobi`, `legendre`, `monomial`.
- `a`, `b` are both floats to use only if `jacobi` is used. 
- `v` should be either `1` or `2` depending on whether the experiment is for univariate or bivariate case.
- `t` should be set to one if `jacobi` were to be used.

After the experiments are completed, one can refer to the `results` folder for a log of results.