import sys
import lecture_jeu as lec

def create_blocs(evac_nodes,arcs,sol_info):
    # dict de tuples (date de départ,taux d'évacuation) pour tous les arcs traversés
    # solution[(id_node,(node1,node2))] = (start_date,evac_rate)
    # 1 bloc = 1 arc traversé par 1 noeud à évacuer et 1 date de depart avec 1 taux d'évacuation,
    solution = {}
    for x, x_value in evac_nodes.items():
        (evac_rate,start_date) = sol_info[x] #durée traversée = -(-x_value['pop']//evac_rate)
        for x_arc in x_value['route']:
            solution[(x,x_arc)] = (start_date,evac_rate)
            start_date = start_date + arcs[x_arc]['length']
        solution[(x,(x_value['route'][-1][1],'completed'))] = (start_date,evac_rate)
    return solution

def calculate_objective(evac_nodes,blocs):
    # pour avoir du O(n)
    obj_x = [(blocs[(x,(evac_nodes[x]['route'][-1][1],'completed'))][0] - (-evac_nodes[x]['pop']//blocs[(x,(evac_nodes[x]['route'][-1][1],'completed'))][1])) for x in evac_nodes]
    # obj_x = [(blocs[tup][0] - (-evac_nodes[tup[0]]['pop']//blocs[tup][1])) for tup in blocs if tup[1][1] == 'completed']
    print("objectives: ", obj_x)
    return max(obj_x)

def verify_max_rates(evac_nodes,arcs,sol_info):
    for x, x_value in evac_nodes.items():
        ok = True
        evac_rate = sol_info[x][0]
        # on verifie que evac_rate est inferieur au taux d'evacuation maximal du noeud
        if (evac_rate <= evac_nodes[x]['max_rate']):
            ok = True
            # on verifie que le taux d'evacuation est inferieur aux capacites des arcs traverses
            for x_arc in x_value['route']:
                if evac_rate > arcs[x_arc]['capacity']:
                    ok = False
        else:
            ok = False
        return ok

def verify_capacities(evac_nodes,arcs,blocs):
    used_arcs = set([tup[1] for tup in blocs if tup[1][1] != 'completed'])
    # print("used arcs: ", used_arcs)
    valid = True
    for a in used_arcs:
        capacity = arcs[a]['capacity']
        # seq = liste de (start_date,evac_rate,durée_traversée) de chaque bloc se déroulant sur l'arc a
        seq = [(blocs[tup][0],blocs[tup][1],-(-evac_nodes[tup[0]]['pop']//blocs[tup][1])) for tup in blocs if tup[1] == a]
        start = min(seq)[0] # début du passage sur l'arc a
        end = max([s+d for (s,r,d) in seq]) # fin du passage sur l'arc a
        # print("seq: ", seq)
        for t in range(start,end):
            nb_pers = 0
            # pour chaque bloc de l'arc a, on compte le nombre de personnes qui traversent
            for (st,rate,ft) in seq:
                if (t>=st and t<(st+ft)):
                    nb_pers = nb_pers + rate
            # print(a," time:",t," nb_pers:",nb_pers)
            # si le nombre de personne est supérieur à la capacité de l'arc, la solution n'est pas réalisable
            if (nb_pers>capacity):
                # print(a, "problem capacity =", capacity)
                valid = False
    return valid

if __name__== "__main__":
    dataname = sys.argv[1]
    solname = sys.argv[2]
    pathfile = "../"
    (my_evac,my_graph) = lec.read_data(pathfile + dataname)
    my_sol = lec.read_solution(pathfile + solname)
    print("ma solution: ", my_sol)
    if verify_max_rates(my_evac,my_graph,my_sol['param']):
        print("taux d'evacuation OK")
    else:
        print("taux d'evacuation PAS OK")
    gantt_blocs = create_blocs(my_evac,my_graph,my_sol['param'])
    print("representation blocs pour la solution ", gantt_blocs)
    print("theoretical objective = " , my_sol['objective'], " minimum objective = ", calculate_objective(my_evac,gantt_blocs))
    realisable = verify_capacities(my_evac,my_graph,gantt_blocs)
    if realisable:
        print("solution réalisable")
    else:
        print("solution non réalisable")
