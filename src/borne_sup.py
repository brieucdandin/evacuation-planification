import sys
import time
import lecture_jeu as lec
import verification_solution as vs
import creation_fichier_solution as fs

def borne_sup(evac_nodes,arcs,name):
    start_time = time.time()
    # used_arcs: dict des arcs utilisés avec la liste des noeuds d'évacuation qui l'utilisent
    # used_arcs[(n1,n2)] = [a,b,c]
    # nodes_route: dict pour chaque noeud à évaluer, liste des arcs empruntés
    used_arcs = {};
    for x, x_value in evac_nodes.items():
        for x_arc in x_value['route']:
            if x_arc in used_arcs:
                used_arcs[x_arc].append(x)
            else:
                used_arcs[x_arc] = [x]
    params_sol = {} # creation des parametres solution avec taux d'evacuation maximal (ie le min entre le max rate du noeud et la capacité min des arcs empruntés) et date de depart 0
    # params_sol[x] = (min_evac_rate,0) avec min_evac_rate le taux minimal sur tous les arcs partagés
    for x, x_value in evac_nodes.items():
        # print(x,":",x_value['route'])
        # print([arcs[arc]['capacity']//len(used_arcs[arc]) for arc in x_value['route']])
        rate = min([arcs[arc]['capacity']//len(used_arcs[arc]) for arc in x_value['route']])
        params_sol[x] = (min(rate,evac_nodes[x]['max_rate']),0)
        # print(x," rate: ",params_sol[x],"max rate: ",evac_nodes[x]['max_rate'])
    gantt_blocs = vs.create_blocs(evac_nodes,arcs,params_sol)
    sup = vs.calculate_objective(evac_nodes,gantt_blocs)
    if vs.verify_capacities(evac_nodes,arcs,gantt_blocs):
        nature_of_solution = "valid"
    else:
        nature_of_solution = "invalid"
        print("invalid")
    end_time = time.time()
    fs.write_solution(name, params_sol, nature_of_solution, sup, end_time-start_time, "borne superieure","test!")
    return sup

# Borne sup avec dates de départs un par un et taux minimal
def borne_sup_date_taux(evac_nodes,arcs,name):
    start_time = time.time()
    used_arcs = {};
    for x, x_value in evac_nodes.items():
        for x_arc in x_value['route']:
            if x_arc in used_arcs:
                used_arcs[x_arc].append(x)
            else:
                used_arcs[x_arc] = [x]
    start_date = 0
    params_sol = {}
    for x, x_value in evac_nodes.items():
        rate = min([arcs[arc]['capacity']//len(used_arcs[arc]) for arc in x_value['route']])
        params_sol[x] = (min(rate,evac_nodes[x]['max_rate']),start_date)
        start_date = sum([arcs[arc]['length'] for arc in x_value['route']]) + (-(-x_value['pop']//rate)) + start_date
    gantt_blocs = vs.create_blocs(evac_nodes,arcs,params_sol)
    sup = vs.calculate_objective(evac_nodes,gantt_blocs)
    if vs.verify_capacities(evac_nodes,arcs,gantt_blocs):
        nature_of_solution = "valid"
        print("valid")
    else:
        nature_of_solution = "invalid"
        print("invalid")
    end_time = time.time()
    fs.write_solution(name, params_sol, nature_of_solution, sup, end_time-start_time, "borne superieure dates","test!")
    return sup

def borne_sup_dates(evac_nodes,arcs,name):
    start_time = time.time()
    start_date = 0
    params_sol = {}
    for x, x_value in evac_nodes.items():
        rate = min([arcs[arc]['capacity'] for arc in x_value['route']])
        params_sol[x] = (min(rate,evac_nodes[x]['max_rate']),start_date)
        start_date = sum([arcs[arc]['length'] for arc in x_value['route']]) + (-(-x_value['pop']//rate)) + start_date
    gantt_blocs = vs.create_blocs(evac_nodes,arcs,params_sol)
    sup = vs.calculate_objective(evac_nodes,gantt_blocs)
    if vs.verify_capacities(evac_nodes,arcs,gantt_blocs):
        nature_of_solution = "valid"
        print("valid")
    else:
        nature_of_solution = "invalid"
        print("invalid")
    end_time = time.time()
    fs.write_solution(name, params_sol, nature_of_solution, sup, end_time-start_time, "borne superieure dates","test!")
    return sup

if __name__== "__main__":
    dataname = sys.argv[1]
    # pathfile = "../"
    pathfile = "../InstancesInt/"
    (my_evac,my_graph) = lec.read_data(pathfile + dataname + ".full")
    # print("borne sup:", borne_sup(my_evac,my_graph,dataname + "-sol_sup"))
    print("borne sup:", borne_sup_dates(my_evac,my_graph,dataname + "-sol_sup"))
