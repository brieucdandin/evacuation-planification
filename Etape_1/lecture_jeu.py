import sys

def read_data(filename):
    evac_info = {} #evac_info={evac_node_id : {'pop':.., 'max_rate':.., 'k':.., 'route':[node1,node2,..]} }
    graph = {} #graph = {(node1,node2):{'duedate':.., 'length':.., 'capacity':..}}
    f = open(filename,"r")
    line = f.readline()
    if (line.startswith("c [evacuation info]")):
        line = f.readline()
        ll = line.split()
        num_evac_nodes = int(ll[0])
        id_safe_node = int(ll[1])
        for i in range(num_evac_nodes):
            line = f.readline()
            ll = line.split()
            id = int(ll[0])
            pop = int(ll[1])
            max_rate = int(ll[2])
            k = int(ll[3])
            vl = []
            for j in range(4,4+k):
                vl.append(int(ll[j]))
            ''' Informations sur un noeud à évacuer donné :
                    population
                    vitesse maximale d'évacuation
                    nombe de noeuds par lesquels il faut passer pour l'évacuer
                    noeuds par lesquels il faut passer pour l'évacuer
            '''
            evac_info[id] = {'pop': pop, 'max_rate': max_rate, 'k': k, 'route': vl}
        # print(evac_info)
    line = f.readline()
    if (line.startswith("c [graph]")):
        line = f.readline()
        ll = line.split()
        num_nodes = int(ll[0])
        num_edges = int(ll[1])
        for i in range(num_edges):
            line = f.readline()
            ll = line.split()
            n1 = int(ll[0])
            n2 = int(ll[1])
            duedate = int(ll[2])
            length = int(ll[3])
            capacity = int(ll[4])
            ''' Informations sur un arc donné :
                    date limite
                    longueur (qui entraîne le temps de parcours trivialement)
                    capacité
            '''
            if (n1<n2):
                graph[(n1,n2)] = {'due_date': duedate, 'length': length, 'capacity': capacity}
            else:
                graph[(n2,n1)] = {'due_date': duedate, 'length': length, 'capacity': capacity}
        # print(graph)
    return (evac_info,graph)

def read_solution(filename):
    f = open(filename,"r")
    sol_info = {} #{'solution_name': .., 'method': .., 'nb_evac_nodes': 3, 'objective': 37, 'comment': .., 'processing_time': 1000, 'nature': 'valid', 'param': {1: (8, 3), 2: (5, 0), 3: (3, 0)}}
    line = f.readline()
    sol_info['solution_name'] = line.rstrip('\n')
    line = f.readline()
    sol_info['nb_evac_nodes'] = int(line)
    node_info = {}
    ll = []
    for i in range(sol_info['nb_evac_nodes']):
        line = f.readline()
        ll = line.split()
        node_info[int(ll[0])] = (int(ll[1]),int(ll[2]))
    sol_info['param'] = node_info
    line = f.readline()
    sol_info['nature'] = line.rstrip('\n')
    line = f.readline()
    sol_info['objective'] = int(line)
    line = f.readline()
    sol_info['processing_time'] = int(line)
    line = f.readline()
    sol_info['method'] = line.rstrip('\n')
    line = f.readline()
    sol_info['comment'] = line.rstrip('\n')
    return sol_info

def main():
    # pathfile = "../InstancesInt/"
    dataname = sys.argv[1]
    solname = sys.argv[2]
    pathfile = "../"
    print("in main, run read_data")
    (my_evac,my_graph) = read_data(pathfile + dataname)
    print("my graph ", my_graph)
    my_sol = read_solution(pathfile + solname)
    print(my_sol)

if __name__== "__main__":
  main()
