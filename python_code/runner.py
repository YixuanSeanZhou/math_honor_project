import os
import json
import sys
import getopt
import csv

import matplotlib.pyplot as plt
import progressbar

from src.utils.experiment import experiment
from src.basis.polynomial_base import basis



def main(v, pb, mb, a):
    #classes = []
    #for key, val in basis:
    #for c_m in classes:
    #    for c_p in classes:
    #        conds = []
    #        x = []
    #        with progressbar.ProgressBar(max_value=7) as bar:
    #            for i in range(1, 8):
    #                conds.append(experiment(c_m, c_p, i*2, 1))
    #                x.append(i * 2)
    #                bar.update(i)
    #        plt.title(str(c_m.__name__) + ' - ' + str(c_p.__name__))
    #        plt.plot(x, conds)
    #        plt.savefig('univariate/' + str(c_m.__name__) + '_' + str(c_p.__name__) + '.png')
    #        plt.show()

    poly_b = basis[pb]
    mtx_b = basis[mb]
    conds = []
    x = []

    if int(v) == 1:

        if not bool(int(a)):
            with progressbar.ProgressBar(max_value=7) as bar:
                for i in range(1, 8):
                    conds.append(experiment(mtx_b, poly_b, i*2, 1))
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
                            conds.append(experiment(vm, vp, i*2, 1))
                            x.append(i * 2)
                            bar.update(i)

                    plt.title(str(mb) + ' - ' + str(pb))
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
        if not bool(int(a)):
            with progressbar.ProgressBar(max_value=5) as bar:
                for i in range(1, 6):
                    conds.append(experiment(mtx_b, poly_b, i*2, 2))
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
        opts, args = getopt.getopt(argv,"hb:m:v:a:",["polynomial_basis=", "matrix_basis=", "num_var="])
    except getopt.GetoptError:
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            #print(desc_str)
            sys.exit()
        elif opt in ("-b", "--polynomial_basis"):
            pb = arg
        elif opt in ("-m", "--matrix_basis"):
            mb = arg
        elif opt in ("-v", "--num_var"):
            v = arg
        elif opt in ("-a", "--all"):
            a = arg

    main(v, pb, mb, a)