#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def unitequoted(queries):
    newqueries = []
    quoted = False
    for q in queries:
        if quoted:
            dim = len(newqueries)-1
            newqueries[dim] = newqueries[dim] + " " + q
            if q.endswith('"'):
                quoted = False
            continue
                
        if q.startswith('"'):
            newqueries.append(q)
            if not q.endswith('"'):
                quoted = True
            continue
        newqueries.append(q)
    return newqueries

def checkquotes(s):
    dim = len(s)
    i = 0
    while (i<dim):
        if s[i] == ':':
            if s[i+1] == '"':
                s = s[0:i+1] + ' '+s[i+1:dim]
                dim = len(s)
                #print("trovato")
        i = i+1
    return s
        
def divqueries(s):
    s = checkquotes(s)
    #print(s)
    words = s.split()
    #print(words)
    words = unitequoted(words)
    #print(words)
    queries = []
    nextw = False
    for w in words:
        if nextw:
            dim = len(queries)-1
            queries[dim] = queries[dim] + w
            nextw = False
            continue
        
        if w.endswith(":"):
            queries.append(w)
            nextw = True
            continue
        queries.append(w)
    return queries

def getword(q):
    count=0
    dimq = len(q)
    while(q[count] != ':' and count < dimq-1):
        count = count + 1
    if count == dimq-1:
        return q 
    if count < dimq-1:
        return q[count+1:dimq]

def removequotes(words):
    #print(words)
    #rimozione dei quoted
    dimw = len(words)
    i = 0
    while (i < dimw):
        if words[i] == '"':
            words = words[0:i] + words[i+1:dimw]
            dimw = dimw-1
        i = i+1
    return words

def getquerywords(queries): #queries è la lista di ritorno di divqueries
    pubwords = ""
    venwords = ""
    for q in queries:
        word = getword(q)
        if q.startswith("article") or q.startswith("incollection") or q.startswith("inproceedings") or q.startswith("phdThesis") or q.startswith("mastersYhesis") or q.startswith("publication"):
            pubwords = pubwords + word + " "
        elif q.startswith("venue"):
            venwords = venwords + word + " "
        else:
            pubwords = pubwords + word + " "
            venwords = venwords + word + " "
    
    pubwords = removequotes(pubwords)
    venwords = removequotes(venwords)
    return (pubwords,venwords)

types = ["article", "incollection", "inproceedings", "phdthesis", "mastersthesis"]
def setqueries(queries):
    pub = ""
    ven = ""
    for q in queries:
        
        dim = len(q)
        
        if q.startswith("publication.") or q.startswith("publication:"):
            pub = pub + q[12:dim] + " OR "
            
        elif q.startswith("article.") or q.startswith("article:"):
            pub = pub + "(pubtype:article AND " + q[8:dim] + ") OR "
        
        elif q.startswith("incollection.") or q.startswith("incollection:"):
            pub = pub + "(pubtype:incollection AND " + q[13:dim] + ") OR "
            
        elif q.startswith("inproc.") or q.startswith("inproc:"):
            pub = pub + "(pubtype:inproceedings AND " + q[7:dim] + ") OR "
        
        elif q.startswith("phThesis.") or q.startswith("phThesis:"):
            pub = pub + "(pubtype:phdthesis AND " + q[9:dim] + ") OR "
    
        elif q.startswith("masterThesis.") or q.startswith("masterThesis:"):
            pub = pub + "(pubtype:masterthesis AND " + q[13:dim] + ") OR "
        
        elif q.startswith("venue.") or q.startswith("venue:"):
            ven = ven + q[6:dim] + " OR "
    
        else:
            pub = pub + q + " OR "
            ven = ven + q + " OR "
        
    dimpub = len(pub)
    pub = pub[0:dimpub-3]
        
    dimven = len(ven)
    ven = ven[0:dimven-3]
        
    return pub, ven 