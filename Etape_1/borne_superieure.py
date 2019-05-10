import sys
import lecture_jeu as lec

# evac_info[id] = {'pop': pop, 'max_rate': max_rate, 'k': k, 'route': vl}
# graph[(n1,n2)] = {'due_date': duedate, 'length': length, 'capacity': capacity}

def borne_superieure(evac_info, graph):
    borne = {}
    duree = 0
    # Pour chaque noeud de départ...
    for noeud_init_key, noeud_init  in evac_info.items():
        evac_rate = noeud_init['max_rate']
        time_to_evacuate_node = 0
        ''' On parcourt le chemin d'évacuation une première fois afin de :
                - trouver la capacité d'arc limitante lors de l'évacuation
                - garder en mémoire le temps total d'évacuation d'un groupe
        '''
        for i in range (noeud_init['k']):
            print("DEBUG - Heing ?\n")
            local_capacity = graph[(noeud_init.route(i), noeud_init.route(i+1))]['capacity']
            time_to_evacuate_node += graph[(noeud_init.route(i), noeud_init.route(i+1))]['length']
            print("DEBUG - De ?\n")
            if evac_rate > local_capacity:
                evac_rate = local_capacity
                print("DEBUG - Paske le logarithme ne paye rien ! Arf arf arf arf arf XDey\n")
        print("DEBUG - 1/4 beurre, 1/4 oeufs, 1/4 farine, 1/4 sucre\n")
        # Évacuation
        # Le premier groupe est évacué en <time_to_evacuate_node>...
        noeud_init['pop'] -= evac_rate
        duree += time_to_evacuate_node
        # ... et les autres occupent le chemin seulement 1 unité de temps en plus, car partent une unité de temps après le départ du groupe précédent.
        if noeud_init['pop'] > 0:
            duree += int(noeud_init['pop']) + 1
    print("DEBUG - Fin fct")
    return duree


def main():
    dataname = sys.argv[1]
    solname = sys.argv[2]
    pathfile = "../"
    print("\n")
    (my_evac,my_graph) = lec.read_data(pathfile + dataname)
    print("\n")
    print(borne_superieure(my_evac,my_graph))
    print("\n")
    print("DEBUG - FIN\n\n")

if __name__== "__main__":
  main()
