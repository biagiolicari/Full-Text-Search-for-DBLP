from fuzzywuzzy import fuzz

'''
phrase = input("Insert query:\n>>")
queries = divqueries(phrase)
print(queries)
t,v=getquerywords(queries)
'''
class FuzzyMatch() :
    def __init__(self,query,obj):
        self.score = fuzz.token_set_ratio(query, "\n".join(str(j) for n, j in obj))
        self.obj = obj
        self.result = "\n".join(str(j) for n, j in obj)

    def getscore(self):
        return self.score

    def get_item(self):
        return self.obj

    def print(self):
        print(self.result)

    def score(self):
        return self.score


def sort_result(query,result) :
    sorted_result = []
    apj = []
    for elem in result:
        apj.append(FuzzyMatch(query,elem.items()))

    sorted_result = sorted(apj,key= lambda f : f.getscore(), reverse=True)
    return sorted_result
