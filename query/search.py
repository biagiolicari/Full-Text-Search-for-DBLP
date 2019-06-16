#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from whoosh.index import open_dir
from whoosh.fields import *
import whoosh.qparser
from ranking.ranking import *
from query.getqueries import divqueries, setqueries,getquerywords
from ranking.merge_result import *
from ranking.Threshold import *

import os


def create_scheme():
    schema = Schema(  # date=DATETIME(stored=True),
        pubtype=TEXT(stored=True),
        key=ID(stored=True),
        author=TEXT(stored=True, phrase=False),
        title=TEXT(stored=True, phrase=False),
        pages=TEXT,
        year=TEXT(phrase=False),
        # volume=TEXT(stored=True),
        crossref=TEXT(stored=True))

    schema_venue = Schema(  # date=DATETIME(stored=True),
        pubtype=TEXT(stored=True),
        key=ID(stored=True),
        author=TEXT(stored=True, phrase=False),
        title=TEXT(stored=True, phrase=False),
        journal=TEXT(stored=True, phrase=False),
        publisher=TEXT(stored=True, phrase=False))

    return schema,schema_venue

def start():

    print("Opening dblp index")

    pubIx = open_dir("index/dblp_index/Pubblication_Index")
    venIx = open_dir("index/dblp_index/Venue_Index")
    query_immesse = 10
    while query_immesse >= 0 :

    
        searcher = pubIx.searcher(weighting = scoring.Frequency)
        searcher2 = venIx.searcher(weighting = scoring.Frequency)

        phrase = input("Insert query:\n>>")
        phrase_no_rank,choice,topk = choice_ranking(phrase)
        queries = divqueries(phrase_no_rank)
        print(queries)

        q1, q2 = setqueries(queries)
        print(q1 + '\t' + q2)
        print('\n')

        schema = create_scheme()[0]
        parser = whoosh.qparser.MultifieldParser( ['author','title','year'], schema=pubIx.schema) #default is title
        query = parser.parse(q1)
        results = searcher.search(query, limit = None)

        schema = create_scheme()[1]
        parser = whoosh.qparser.MultifieldParser( ['author','title','year'], schema=venIx.schema) #default is title
        query = parser.parse(q2)
        results2 = searcher2.search(query, limit = None)

        t,g = getquerywords(queries)

        rank = ranking(query=t, result= results, choice= choice, ix= pubIx.doc_count(), searcher= searcher, pub= True)
        sorted_result = rank.rank()
        #print_sorted_result(sorted_result,choice)

        rank = ranking(query=g, result= results2, choice= choice, searcher= searcher2, ix= venIx.doc_count(), pub= False)
        sorted_result2=rank.rank()
        #print_sorted_result(sorted_result2,choice)

        result = merge_results(pub_result= sorted_result, choice= choice, venue_result= sorted_result2)

        Ta_result = Threshold(result,topk).run()

        f = open('Result.txt','a',encoding='utf-8')

        for i in Ta_result[0:topk] :


            if i[0][0][0] is None :
                final=i[0][1][0]

            elif i[0][1][0] is None :
                if return_fuzzy_choice(choice) :
                    final=i[0][0][0][0]
                else :
                    final=i[0][0][0]

            else:
                if return_fuzzy_choice(choice) :
                    final = list(set(i[0][0][0][0]+i[0][1][0])) #list(set().union(i[0][0][0],i[0][1][0]))
                else:
                    final = list(set(i[0][0][0] + i[0][1][0]))

            print_result_TA(final,i[1],f)

        f.close()

        import subprocess
        subprocess.run(['more',str(os.path.abspath('Result.txt'))],shell=True)
        status_cmd = subprocess.CompletedProcess(['more',str(os.path.abspath('Result.txt'))],returncode=0).returncode

        if status_cmd == 0 :
            os.remove(os.path.abspath('Result.txt'))

        query_immesse -=1

def print_result_TA(final,score,f) :

    for tag,value in final :
        if value == '' or tag == 'key' :
            pass
        else :
            f.write(u'\n{}'.format(tag) + ':\n')
            f.write( str(value).rstrip()+'\n' )


    f.write('\nScore : {}'.format(score))
    f.write('\n---------------------------------------------------------------------------------------------------------------\n')



