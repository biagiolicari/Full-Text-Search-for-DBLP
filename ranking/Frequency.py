from whoosh import scoring
class Frequency() :
    def __init__(self,result):
        self.result = result
        self.sorted_result = []


    def sort_result(self):
        self.sorted_result = sorted(self.result, key= lambda f : f.score, reverse=True)
        return self.sorted_result

    def print(self):
        for hit in self.sorted_result:
           print('\n'.join(str(k) for j,k in hit.items()))


