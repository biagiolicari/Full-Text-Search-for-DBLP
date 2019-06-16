from whoosh.searching import *
from whoosh.analysis import *
import re
from math import *
#w sarà un termine, s sarà self.query
def freq(w, s):
    res = re.compile(r'\b({0})\b'.format(str(w)), flags=re.IGNORECASE).findall(str(s))

    if res == []:
        return 0
    return len(res)

class Vector():

    def __init__(self, searcher, results, query, numDoc): #dall'esterno il numero di documenti è index.doc_count()

        self.searcher = searcher
        self.results = results
        self.query = query #query deve essere una stringa di termini separati da spazi (così come appaiono nella query)
        self.numDoc = numDoc

        self.analyzer = StandardAnalyzer()
        self.words = [token.text for token in self.analyzer(query)] # torna una lista di parole della query senza stopwords
        self.setwords = set(self.words) # set di parole senza duplicati

        self.words_and_freq = [] #lista di tuple che per ogni parola nella query

        #calcolo della frequenza e di idf di una parola nella query
        for w in self.setwords:
            f = freq(w,self.query)
            df = self.searcher.get_parent().doc_frequency("author", w) + self.searcher.get_parent().doc_frequency("title", w) #not for year
            if df == 0:
                idf = 0
            else:
                idf = log(self.numDoc/df)
            self.words_and_freq.append((w, f, idf)) # ora words_and_freq contiene parola, quante volte compare nella query e il suo idf

    def rank(self):
        if self.results.is_empty():
            print("No results for ranking")
            return

        #split della query (contenente termini)
        #inizializzazione lista di tuple (<Hit>, score)
        results_and_scores = []
        for hit in self.results:
            numeratore = 0
            den1 = 0
            den2 = 0

            for wf in self.words_and_freq:
                wdt = (freq(wf[0], hit["author"]) + freq(wf[0], hit["title"])) * wf[2]
                wqf = wf[1]*wf[2]
                numeratore = numeratore + (wdt * wqf)
                den1 = den1 + wdt ** 2
                den2 = den2 + wqf ** 2
            
            try:
                score = numeratore / (sqrt(den1) * sqrt(den2))
            except ZeroDivisionError:
                score = 0
            finally:             
                results_and_scores.append((hit, score))
        
        results_and_scores = sorted(results_and_scores, key=lambda score: score[1], reverse=True)
        '''
        for i in range(0,200):
            print(results_and_scores[i])
        '''
        return results_and_scores
        
class Vector_Venue:
    def __init__(self, searcher, results, query, numDoc): #dall'esterno il numero di documenti è index.doc_count()

        self.searcher = searcher
        self.results = results
        self.query = query #query deve essere una stringa di termini separati da spazi (così come appaiono nella query)
        self.numDoc = numDoc

        self.analyzer = StandardAnalyzer()
        self.words = [token.text for token in self.analyzer(query)] # torna una lista di parole della query senza stopwords
        self.setwords = set(self.words) # set di parole senza duplicati

        self.words_and_freq = [] #lista di tuple che per ogni parola nella query

        #calcolo della frequenza e di idf di una parola nella query
        for w in self.setwords:
            f = freq(w,self.query)
            df = self.searcher.get_parent().doc_frequency("title", w) + self.searcher.get_parent().doc_frequency("publisher", w) #not for year
            if df == 0:
                idf = 0
            else:
                idf = log(self.numDoc/df)
            self.words_and_freq.append((w, f, idf)) # ora words_and_freq contiene parola, quante volte compare nella query e il suo idf

    def rank(self):
        if self.results.is_empty():
            print("No results for ranking")
            return

        #split della query (contenente termini)
        #inizializzazione lista di tuple (<Hit>, score)
        results_and_scores = []
        for hit in self.results:
            numeratore = 0
            den1 = 0
            den2 = 0

            for wf in self.words_and_freq:
                wdt = (freq(wf[0], hit["title"]) + freq(wf[0], hit["publisher"])) * wf[2]
                wqf = wf[1]*wf[2]
                numeratore = numeratore + (wdt * wqf)
                den1 = den1 + wdt ** 2
                den2 = den2 + wqf ** 2
            
            try:
                score = numeratore / (sqrt(den1) * sqrt(den2))
            except ZeroDivisionError:
                score = 0
            finally:             
                results_and_scores.append((hit, score))
            

            #print(hit, score)
        
        results_and_scores = sorted(results_and_scores, key=lambda score: score[1], reverse=True)
        '''
        for i in range(0,200):
            print(results_and_scores[i])
        '''

        return results_and_scores
        

    
        
        