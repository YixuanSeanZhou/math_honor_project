import os
import json
import sys
import getopt
import csv

import matplotlib.pyplot as plt
import progressbar

from src.utils.experiment import experiment
from src.basis.polynomial_base import basis



def main(v, pb, mb, type_of_exp, a, b):

    poly_b = basis[pb]
    mtx_b = basis[mb]
    conds = []
    x = []

    if int(v) == 1:

        if not bool(int(type_of_exp)):
            with progressbar.ProgressBar(max_value=7) as bar:
                for i in range(1, 8):
                    conds.append(experiment(mtx_b, poly_b, i*2, 1, a, b))
                    x.append(i * 2)
                    bar.update(i)

            plt.title(str(mb) + ' - ' + str(pb))
            plt.plot(x, conds)

            plt.savefig('./results/univariate/' + mb + '_' + pb + '.png')
            with open('./results/univariate/'+ mb + '_' + pb + '.csv', mode='w') as csvfile:
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerow(['degree', 'con_num'])
                for i, x in enumerate(x):
                    row = [x, conds[i]]
                    csvwriter.writerow(row)
        else:
            for kp, vp in basis.items():
                for km, vm in basis.items():

                    conds = []
                    x = [] 
                    with progressbar.ProgressBar(max_value=7) as bar:
                        for i in range(1, 8):
                            conds.append(experiment(vm, vp, i*2, 1, a, b))
                            x.append(i * 2)
                            bar.update(i)

                    if km == 'jacobi':
                        km += '_a_' + str(a) + '_b_' + str(b)
                    if kp == 'jacobi':
                        kp += '_a_' + str(a) + '_b_' + str(b)
                    plt.title(str(km) + ' - ' + str(kp))
                    plt.plot(x, conds)

                    plt.savefig('./results/univariate/' + km + '_' + kp + '.png')
                    plt.clf()
                    with open('./results/univariate/'+ km + '_' + kp + '.csv', mode='w') as csvfile:
                        csvwriter = csv.writer(csvfile) 
                        csvwriter.writerow(['degree', 'con_num'])
                        for i, x in enumerate(x):
                            row = [x, conds[i]]
                            csvwriter.writerow(row)
        
    else:
        if not bool(int(type_of_exp)):
            with progressbar.ProgressBar(max_value=5) as bar:
                for i in range(1, 6):
                    conds.append(experiment(mtx_b, poly_b, i*2, 2, a, b))
                    x.append(i * 2)
                    bar.update(i)

            plt.title(str(mb) + ' - ' + str(pb))
            plt.plot(x, conds)

            plt.savefig('./results/bivariate/' + mb + '_' + pb + '.png')
            with open('./results/bivariate/'+ mb + '_' + pb + '.csv', mode='w') as csvfile:
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerow(['degree', 'con_num'])
                for i, x in enumerate(x):
                    row = [x, conds[i]]
                    csvwriter.writerow(row)


if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hp:m:v:t:a:b:",["polynomial_basis=", "matrix_basis=", "num_var="])
    except getopt.GetoptError:
        sys.exit(1)
    for opt, arg in opts:
        a = 0
        b = 0
        if opt == '-h':
            #print(desc_str)
            sys.exit()
        elif opt in ("-p", "--polynomial_basis"):
            pb = arg
        elif opt in ("-m", "--matrix_basis"):
            mb = arg
        elif opt in ("-v", "--num_var"):
            v = arg
        elif opt in ("-t", "--t"):
            type_of_exp = arg
        elif opt in ("-a"):
            a = float(arg)
        elif opt in ("-b"):
            b = float(arg)

        

    main(v, pb, mb, type_of_exp, a, b)