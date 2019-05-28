import sys
import time
import copy
from operator import itemgetter
import lecture_jeu as lec
import verification_solution as vs
import creation_fichier_solution as fs


if __name__== "__main__":
    dataname = sys.argv[1]
    solname = sys.argv[2]
    # pathfile = "../"
    datapathfile = "../InstancesInt/"
    solutionpathfile = "../Solutions/"
    (my_evac,my_graph) = lec.read_data(datapathfile + dataname)
    sol_finale = (my_evac,my_graph)
    # print("meilleure solution: ", sol_finale[0], " avec objectif: ", sol_finale[1])
    print("ancien objectif: ",sol_initiale['objective'], " nouvel objectif:", sol_finale[1])
