import sys
import time
import lecture_jeu as lec
import verification_solution as vs
import creation_fichier_solution as fs

def borne_inf(evac_nodes,arcs,name):
    start_time = time.time()
    params_sol = {} # creation des parametres solution avec taux d'evacuation maximal (ie le min entre le max rate du noeud et la capacité min des arcs empruntés) et date de depart 0
    for x, x_value in evac_nodes.items():
        prev = x
        x_arcs = []
        for ni in x_value['route']:
            if (prev<ni):
                x_arcs.append((prev,ni))
            else:
                x_arcs.append((ni,prev))
            prev = ni
        params_sol[x] = (min(x_value['max_rate'],min([arcs[(na,nb)]['capacity'] for (na,nb) in x_arcs])),0)
    gantt_blocs = vs.create_blocs(evac_nodes,arcs,params_sol)
    inf = vs.calculate_objective(evac_nodes,gantt_blocs)
    if vs.verify_capacities(evac_nodes,arcs,gantt_blocs):
        nature_of_solution = "valid"
    else:
        nature_of_solution = "invalid"
    end_time = time.time()
    fs.write_solution(name, params_sol, nature_of_solution, inf, end_time-start_time, "borne inferieure","test!&0")
    return inf

if __name__== "__main__":
    dataname = sys.argv[1]
    # pathfile = "../"
    pathfile = "../InstancesInt/"
    (my_evac,my_graph) = lec.read_data(pathfile + dataname)
    print("borne inf:", borne_inf(my_evac,my_graph,dataname + "-borne_inf"))
