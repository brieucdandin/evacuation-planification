import sys

# pathfile = "../Instances/"
pathfile = "../"
#filename = sys.argv[1]
# filename = "dense_10_30_3_1.full"
filename = "graphe-TD-sans-DL-data.txt"


f = open(pathfile+filename,"r")

line = f.readline()
if (line.startswith("c [evacuation info]")):
    line = f.readline()
    ll = line.split()
    num_evac_nodes = int(ll[0])
    id_safe_node = int(ll[1])
    evac_info = {} #evac_info={evac_node_id : {'pop':.., 'max_rate':.., 'k':.., 'route':[node1,node2,..]} }
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
        evac_info[id] = {'pop': pop, 'max_rate': max_rate, 'start_date': 0, 'k': k, 'route': vl}
    print(evac_info)

line = f.readline()
if (line.startswith("c [graph]")):
    line = f.readline()
    ll = line.split()
    num_nodes = int(ll[0])
    num_edges = int(ll[1])
    graph = {} #graph = {(node1,node2):{'duedate':.., 'length':.., 'capacity':..}}
    for i in range(num_edges):
        line = f.readline()
        ll = line.split()
        n1 = int(ll[0])
        n2 = int(ll[1])
        duedate = int(ll[2])
        length = float(ll[3])
        capacity = int(float(ll[4]))
        graph[(n1,n2)] = {'due_date': duedate, 'length': length, 'capacity': capacity}
    print(graph)
