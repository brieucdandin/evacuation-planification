import sys
import lecture_jeu as lec

# evac_info[id] = {'pop': pop, 'max_rate': max_rate, 'k': k, 'route': vl}
# graph[(n1,n2)] = {'due_date': duedate, 'length': length, 'capacity': capacity}

def borne_superieure(evac_info, graph):
    borne = {}
    duree = 0
    # Pour chaque noeud de départ noeud_init :
    for noeud_init_key, noeud_init in evac_info.items():
        pop_to_evac = noeud_init['pop']
        evac_rate = noeud_init['max_rate']
        route_to_evac = noeud_init['route']
        ''' On parcourt le chemin d'évacuation une première fois afin de :
                - trouver la capacité d'arc limitante lors de l'évacuation
                - garder en mémoire le temps total d'évacuation d'un groupe
        '''
        # On parcourt la liste des noeuds permettant l'évacuation de noeud_init pour vérifier si les arcs parcourus limitent ou non le taux d'évacuation du noeud.
        for i in range (noeud_init['k']):
            arc_capacity = graph[route_to_evac[i]]['capacity']
            time_to_evacuate_node = graph[route_to_evac[i]]['length']
            # Mise à jour du taux d'évacuation le plus petit : si le taux d'évacuation du noeud considéré est plus petit que l'ancienne valeur de evac_rate, elle la remplace.
            if evac_rate > arc_capacity:
                evac_rate = arc_capacity

        # Évacuation
        # Le premier groupe est évacué en <time_to_evacuate_node>...
        pop_to_evac -= evac_rate
        duree += time_to_evacuate_node
        # ... et les autres occupent le chemin seulement 1 unité de temps en plus, car partent une unité de temps après le départ du groupe précédent.
        if pop_to_evac > 0:
            duree += pop_to_evac // evac_rate
            # Évacuation du dernier groupe, non vide mais de taille strictement inférieure à la taille max d'un groupe d'évacuation
            if pop_to_evac % evac_rate != 0:
                duree += 1;
    print("Résulat erroné")
    return duree


def main():
    dataname = sys.argv[1]
    pathfile = "../"
    (my_evac,my_graph) = lec.read_data(pathfile + dataname)
    print(borne_superieure(my_evac,my_graph))

if __name__== "__main__":
  main()
