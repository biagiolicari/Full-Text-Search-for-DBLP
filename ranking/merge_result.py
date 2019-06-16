from ranking.ranking import *
import random

argument_fuzzy = ['-Fuzzy', '-fuzzy', '-rank:Fuzzy', '-rank:Fuzzy', '-rank:fuzzy']
argument_vector = ['-vector', '-vsm', '-VSM', '-rank:vector', '-rank:Vector']


def create_dict(venue, choice):
    """Creo un dizionario per il venue del tipo <chiave-(elementi,score), in base al ranking scelto"""
    diz = {}
    for i in venue:
        if choice in argument_fuzzy:
            item = list(get_item(i, choice))
            item.pop(1)
            diz[str(item.pop(0))] = item

        elif choice in argument_vector:
            diz[str(i[0]['key'])] = (i[0].items(), i[1])

        elif choice == 'standard':
            diz[str(i['key'])] = (i.items(), i.score)
    return diz


def merge_results(pub_result, choice, venue_result):

    """Per ogni hit dei pub mi memorizzo la key e il crossref andando a fare un check sulle chiavi presenti nel dizionario creato prima
       per verificare l'esistenza di un elem pub che ha chiave in venue, nel caso ciò sia presente
       aggiungo alla lista result una tupla del tipo ( (hit_result, hit_score) , (hit_venue, hit_venue_score) )"""
    diz = create_dict(venue_result, choice)
    result = []
    not_visited = set()
    for i in pub_result:
        if choice == 'standard':
            key_pub = i['key']
            crossref = str(i['crossref']).rstrip()

            if key_pub in diz.keys():
                result.append(((i.items(),i.score),diz[key_pub]))
                del diz[key_pub]

            elif crossref in diz.keys():
                result.append(((i.items(),i.score), diz[crossref]))
                del diz[crossref]

            else :
                result.append(((i.items(),i.score),(None,0)))

        elif choice in argument_fuzzy:
            item = list(get_item(i, choice))
            crossref = str(item.pop(1)).rstrip()
            key_pub = item.pop(0)
            score = item.pop(1)


            if key_pub in diz.keys():
                result.append((( item,score),diz[key_pub]))
                del diz[key_pub]

            elif crossref in diz.keys():
                result.append((( item,score),diz[crossref]))
                del diz[crossref]

            else:
                result.append(((item,score),(None,0)))

        elif choice in argument_vector:
            key_pub = i[0]['key']
            crossref = str(i[0]['crossref']).rstrip()

            if key_pub in diz.keys() :
                result.append( ( (i[0].items(), i[1]), diz[key_pub] ) )
                del diz[key_pub]

            elif crossref in diz.keys() :
                result.append( ( (i[0].items(), i[1]), diz[crossref] ) )
                del diz[crossref]

            else :
                result.append(((i[0].items(),i[1]), (None,0)))

    for i in diz.items() :
        result.append( ( (None,0), (i[1][0], i[1][1])))


    return result
