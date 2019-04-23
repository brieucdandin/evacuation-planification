import sys
import lecture_jeu as lec

def create_blocs(evac_nodes,arcs,sol_info):
    solution = {}
    for x, x_value in evac_nodes.items():
        prev = x
        (evac_rate,start_date) = sol_info[x] #durée traversée = -(-x_value['pop']//evac_rate)
        for ni in x_value['route']:
            solution[(x,(prev,ni))] = (start_date,evac_rate)
            start_date = start_date + arcs[(prev,ni)]['length']
            prev = ni
        solution[(x,(prev,'completed'))] = (start_date,evac_rate)
    return solution

def calculate_objective(evac_nodes,blocs):
    obj_x = [(blocs[tup][0] - (-evac_nodes[tup[0]]['pop']//blocs[tup][1])) for tup in blocs if tup[1][1] == 'completed']
    print("objectives: ", obj_x)
    return max(obj_x)

def verify_capacities(evac_nodes,arcs,blocs):
    used_arcs = set([tup[1] for tup in blocs if tup[1][1] != 'completed'])
    print(used_arcs)
    for a in used_arcs:
        capacity = arcs[a]['capacity']
        seq = [(blocs[tup][0],blocs[tup][1],-(-evac_nodes[tup[0]]['pop']//blocs[tup][1])) for tup in blocs if tup[1] == a]
        start = min(seq)[0]
        end = max(seq)[0] + arcs[a]['length']
        for t in range(start,end):
            nb_pers = 0
            for (st,rate,ft) in seq:
                if (t>=st and t<=(st+ft)):
                    nb_pers = nb_pers + rate
            print(a," time:",t," nb_pers:",nb_pers)
            if (nb_pers>capacity):
                print(a, "problem")


if __name__== "__main__":
    dataname = sys.argv[1]
    solname = sys.argv[2]
    pathfile = "../"
    (my_evac,my_graph) = lec.read_data(pathfile + dataname)
    my_sol = lec.read_solution(pathfile + solname)
    print("ma solution: ", my_sol)
    gantt_blocs = create_blocs(my_evac,my_graph,my_sol['param'])
    print("representation blocs pour la solution ", gantt_blocs)
    print("theoretical objective = " , my_sol['objective'], " minimum objective = ", calculate_objective(my_evac,gantt_blocs))
    verify_capacities(my_evac,my_graph,gantt_blocs)
