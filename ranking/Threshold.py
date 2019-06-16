def avg(num1, num2):
    return (num1 + num2) / 2.0

#prende sempre in ingresso una lista di tuple (hitpub, hitven) con hitpub = (pub, score) hitven = (ven, score).
class Threshold:
    def __init__(self, values, k):
        self.pub = [] # ((pubhit, score), (venhit,score)) sorted by pubscore
        self.ven = [] # ((venhit,score), (pubhit,score)) sorted by venscore
        self.results = [] # ad ogni coppia associa la somma di scores ( ((pubhit, score), (venhit,score)) sumscore )
        #self.count = 0 
        self.threshold = 0
        self.k = k #top k results

        self.pub = sorted(values, key=lambda score: score[0][1], reverse=True) #riordino per score di pub
        self.ven = sorted(values, key=lambda score: score[1][1], reverse=True) #riordino per score di ven
        self.index = min(len(self.pub), len(self.ven))

    def run(self):
        for i in range(0,self.index):
            self.threshold = avg(self.pub[i][0][1], self.ven[i][0][1])
            score1 = avg(self.pub[i][0][1], self.pub[i][1][1])
            score2 = avg(self.ven[i][0][1], self.ven[i][1][1])

            if (self.pub[i], score1) not in self.results: #gestisco valori unici
                self.results.append((self.pub[i],score1))
            
            if (self.ven[i],score2) not in self.results:
                self.results.append((self.ven[i], score2))
            
            self.results = sorted(self.results, key=lambda score: score[1], reverse=True) #ottengo valori sortati

            if len(self.results) < self.k:
                continue
            else:
                overThresholdNumber = 0
                for r in self.results: #r[1] = total_score
                    if r[1] > self.threshold:
                        overThresholdNumber +=1
                    else:
                        break
                if overThresholdNumber >= self.k: #se il numero di valori sopra soglia è >= top-k allora END
                    break

        return sorted(self.results, key=lambda score: score[1], reverse = True) #riordino per i nuovi scores
