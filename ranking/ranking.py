from ranking.Vector import *
from ranking.Fuzzy import *
from ranking.Frequency import *


argument_fuzzy = ['-Fuzzy', '-fuzzy', '-rank:Fuzzy', '-rank:Fuzzy', '-rank:fuzzy']
argument_vector = ['-vector', '-vsm', '-VSM', '-rank:vector', '-rank:Vector']

def choice_ranking(query) :
    argument = query.split()
    num = argument[len(argument)-1].replace('-','')
    topk = 0

    if num.isdigit() :
        topk = int(num)
        del argument[len(argument)-1]
    else :
        topk = 50


    for elem in argument :
        if elem in argument_fuzzy:
            choice=elem
            argument.remove(elem)

        elif elem in argument_vector :
            choice=elem
            argument.remove(elem)

        else :
            choice='standard'

    return (" ".join(str(i) for i in argument)),choice,topk


def print_sorted_result(sort_result, choice):
    if choice in argument_fuzzy:
        for hit in sort_result:
            hit.print()
            print(
                "---------------------------------------------------------------------------------------------------------\n")

    elif choice in argument_vector:
        for hit in sort_result:
            print("\n".join(str(k) for j, k in hit[0].items()))
            print(
                "---------------------------------------------------------------------------------------------------------\n")


    elif choice == 'standard':
        for hit in sort_result:
            print('\n'.join(str(k) for j, k in hit.items()))
            print(
                "---------------------------------------------------------------------------------------------------------\n")

def return_fuzzy_choice(choice) :
    if choice in argument_fuzzy :
        return True

def get_item(hit,choice) :
    if choice in argument_fuzzy:
        item = hit.get_item()
        key = ''
        crossref = ''
        for x,j in item :
            if x == 'key' :
                key = j
            if x == 'crossref' :
                if j != '' :
                    crossref = j
        return [key,crossref,hit.get_item(), hit.getscore()]

class ranking() :
    def __init__(self,query,result,choice,ix,searcher,pub):
        self.searcher = searcher
        self.query = query
        self.result = result
        self.choice = choice
        self.ix = ix
        self.pub = pub

    def rank(self):
        if self.choice in argument_vector:
            if self.pub :
                vsm = Vector(self.searcher,self.result,self.query,self.ix)
                return vsm.rank()
            else:
                vsm_venue = Vector_Venue(self.searcher,self.result,self.query,self.ix)
                return vsm_venue.rank()

        elif self.choice in argument_fuzzy:
            sorted_result = sort_result(self.query,self.result)
            return sorted_result

        elif self.choice == 'standard' :
            freq_sorted_result = Frequency(self.result)
            return freq_sorted_result.sort_result()

