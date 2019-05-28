import sys
import time
import copy
from operator import itemgetter
import lecture_jeu as lec
import verification_solution as vs
import creation_fichier_solution as fs

def voisin_date(evac_nodes,arcs,blocs):
    # calcul du temps d'évacuation de chaque noeud
    temps_evac = [(x,(blocs[(x,(evac_nodes[x]['route'][-1][1],'completed'))][0] - (-evac_nodes[x]['pop']//blocs[(x,(evac_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evac_nodes]
    # récupère le noeud qui met le temps le plus long
    noeud_limit = max(temps_evac,key=itemgetter(1))
    # on essaie de faire démarrer l'évacuation une unité plus tôt
    if blocs[(noeud_limit[0],evac_nodes[noeud_limit[0]]['route'][0])][0] > 0:
        new_blocs = copy.deepcopy(blocs)
        for arc in evac_nodes[noeud_limit[0]]['route']:
            new_blocs[(noeud_limit[0],arc)][0] = new_blocs[(noeud_limit[0],arc)][0] - 1
        new_blocs[(noeud_limit[0],(evac_nodes[noeud_limit[0]]['route'][-1][1],'completed'))][0] = new_blocs[(noeud_limit[0],(evac_nodes[noeud_limit[0]]['route'][-1][1],'completed'))][0] - 1
        # si la solution créée est réalisable, c'est un voisin
        if vs.verify_capacities(evac_nodes,arcs,new_blocs):
            return (True,new_blocs)
        # sinon on essaie aussi d'avancer le second plus long
        else:
            noeud_aux = max(temps_evac.remove(noeud_limit),key=itemgetter(1))
            if (blocs[(noeud_aux[0],evac_nodes[noeud_aux]['route'][0])][0]) > 0:
                for arc in evac_nodes[noeud_aux[0]]['route']:
                    new_blocs[(noeud_aux[0],arc)] = (new_blocs[(noeud_aux[0],arc)][0] - 1,new_blocs[(noeud_aux[0],arc)][1])
                new_blocs[(noeud_aux[0],(evac_nodes[noeud_aux[0]]['route'][-1][1],'completed'))] = (new_blocs[(noeud_aux[0],(evac_nodes[noeud_aux[0]]['route'][-1][1],'completed'))][0] - 1,new_blocs[(noeud_aux[0],(evac_nodes[noeud_aux[0]]['route'][-1][1],'completed'))][1])
                # si la solution créée est réalisable, c'est un voisin
                if vs.verify_capacities(evac_nodes,arcs,new_blocs):
                    return (True,new_blocs)
                # sinon arrêt
                else:
                    return (False,{})
            else:
                return (False,{})
    # le plus long commence déjà à 0, on ne peut rien faire
    else:
        return (False,{})

def voisin_taux(evac_nodes,arcs,blocs,step):
    # calcul du temps d'évacuation de chaque noeud
    temps_evac = [(x,(blocs[(x,(evac_nodes[x]['route'][-1][1],'completed'))][0] - (-evac_nodes[x]['pop']//blocs[(x,(evac_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evac_nodes]
    # récupère le noeud qui met le temps le plus long
    noeud_limit = max(temps_evac,key=itemgetter(1))
    # on récupère le taux maximal possible pour le noeud et le taux de la solution prise
    possible_max_rate = min(evac_nodes[noeud_limit[0]]['max_rate'],min([arcs[arc]['capacity'] for arc in evac_nodes[noeud_limit[0]]['route']]))
    current_rate = blocs[(noeud_limit[0],evac_nodes[noeud_limit[0]]['route'][0])][1]
    # si possible, on essaie d'augmenter son taux d'évacuation de la valeur step
    if (current_rate + step) < possible_max_rate:
        new_blocs = copy.deepcopy(blocs)
        for arc in evac_nodes[noeud_limit[0]]['route']:
            new_blocs[(noeud_limit[0],arc)] = (new_blocs[(noeud_limit[0],arc)][0],current_rate + step)
        new_blocs[(noeud_limit[0],(evac_nodes[noeud_limit[0]]['route'][-1][1],'completed'))] = (new_blocs[(noeud_limit[0],(evac_nodes[noeud_limit[0]]['route'][-1][1],'completed'))][0],current_rate + step)
        # si la solution créée est réalisable, c'est un voisin
        (ok,conflits) = vs.verify_capacities_with_return(evac_nodes,arcs,new_blocs)
        if ok:
            print("augmentation taux OK")
            return (True,new_blocs)
        # sinon on essaie de diminuer le taux des noeuds en conflit de la valeur step pour compenser
        else:
            print("augmentation taux PAS OK")
            noeuds_conflits = set([tup[0] for tup in blocs if tup[1] in conflits])
            for x in noeuds_conflits.remove(noeud_limit[0]):
                if new_blocs[(x,evac_nodes[x]['route'][0])][1] - step > 0:
                    new_blocs[(x,evac_nodes[x]['route'][0])] = (new_blocs[(x,evac_nodes[x]['route'][0])][0], new_blocs[(x,evac_nodes[x]['route'][0])][1] - step)
            # si la solution créée est réalisable, c'est un voisin
            if vs.verify_capacities(evac_nodes,arcs,new_blocs):
                print("augmentation taux avec ajustements OK")
                return (True,new_blocs)
            # sinon arrêt
            else:
                print("augmentation taux avec ajustements PAS OK")
                return (False,{})
    # sinon pas de voisin --> essayer avec le second plus tard et avancer les dates de départ
    else:
        return (False,{})

# Fonction qui permet de choisir le premier meilleur voisin
def choix_first_voisin_taux(evac_nodes,arcs,blocs,eval_prev):
    # calcul du temps d'évacuation de chaque noeud
    temps_evac = [(x,(blocs[(x,(evac_nodes[x]['route'][-1][1],'completed'))][0] - (-evac_nodes[x]['pop']//blocs[(x,(evac_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evac_nodes]
    # récupère le noeud qui met le temps le plus long
    noeud_limit = max(temps_evac,key=itemgetter(1))
    # on récupère le taux maximal possible pour le noeud et le taux de la solution prise
    max_rate_noeud_limit = min(evac_nodes[noeud_limit[0]]['max_rate'],min([arcs[arc]['capacity'] for arc in evac_nodes[noeud_limit[0]]['route']]))
    current_rate = blocs[(noeud_limit[0],evac_nodes[noeud_limit[0]]['route'][0])][1]
    # on essaie d'augmenter le noeud le plus lent à son taux d'évacuation maximal
    step = max_rate_noeud_limit - current_rate
    # on boucle tant qu'on a pas atteint le taux maximal et qu'on a pas trouvé de meilleur voisin
    keep_search = step > 0
    best_voisin = {}
    while keep_search:
        # génération d'un voisin
        (possible,voisin) = voisin_taux(evac_nodes,arcs,blocs,step)
        # si la solution est réalisable on l'évalue
        if possible:
            eval_voisin =  vs.calculate_objective(evac_nodes,voisin)
            # si l'évaluation de ce nouveau voisin est meilleure que celle en paramètre (eval_prev) on la retourne
            if eval_voisin > eval_prev:
                keep_search = False
                best_voisin = voisin
            # sinon on réduit la valeur de l'augmentation
            else:
                step = step - 1
                keep_search = step > 0
        # si la solution n'est pas réalisable on réduit la valeur d'augmentation
        else:
            step = step - 1
            keep_search = step > 0
    return best_voisin

def recherche_locale(evac_nodes,arcs,sol_init):
    # solution initiale
    one_sol = vs.create_blocs(evac_nodes,arcs,sol_init['param'])
    one_eval = sol_init['objective']
    best_sol = copy.deepcopy(one_sol)
    best_eval = one_eval
    # répéter
    # (possible,voisin) = voisin_date(evac_nodes,arcs,one_sol)
    (possible,voisin) = voisin_taux(evac_nodes,arcs,one_sol,1)
    if possible:
        print("voisin trouvé")
        one_sol = voisin
        one_eval = vs.calculate_objective(evac_nodes,one_sol)
        if one_eval < best_eval:
            best_sol = copy.deepcopy(one_sol)
            best_eval = one_eval
    else:
        print("pas de voisins")
    # jusqu'à <condition d'arrêt>
    return (best_sol,best_eval)

if __name__== "__main__":
    dataname = sys.argv[1]
    solname = sys.argv[2]
    # pathfile = "../"
    datapathfile = "../InstancesInt/"
    solutionpathfile = "../Solutions/"
    (my_evac,my_graph) = lec.read_data(datapathfile + dataname)
    sol_initiale = lec.read_solution(solutionpathfile + solname)
    sol_finale = recherche_locale(my_evac,my_graph,sol_initiale)
    # print("meilleure solution: ", sol_finale[0], " avec objectif: ", sol_finale[1])
    print("ancien objectif: ",sol_initiale['objective'], " nouvel objectif:", sol_finale[1])
