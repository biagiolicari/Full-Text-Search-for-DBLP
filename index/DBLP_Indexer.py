#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 12:34:10 2019

@author: biagio
"""


import xml.sax
from whoosh.index import create_in
from whoosh.fields import *
import os

def create_scheme():
    schema = Schema(#date=DATETIME(stored=True), 
                                    pubtype=TEXT(stored=True),
                                    key=ID(stored=True), 
                                    author=TEXT(stored=True, phrase=False),
                                    title=TEXT(stored=True, phrase=False),
                                    pages=TEXT,
                                    year=TEXT(phrase=False),
                                    #volume=TEXT(stored=True),
                                    crossref=TEXT(stored=True) )
    
    schema_venue = Schema(#date=DATETIME(stored=True), 
                                    pubtype=TEXT(stored=True),
                                    key=ID(stored=True), 
                                    author=TEXT(stored=True,phrase=False),
                                    title=TEXT(stored=True,phrase=False),
                                    journal=TEXT(stored=True,phrase=False),
                                    publisher = TEXT(stored=True,phrase=False))
    return schema,schema_venue

        
if ( __name__ == "__main__"):
    pub_schema,venue_schema = create_scheme()
    
    if not os.path.exists("dblp_index/Pubblication_Index") and not os.path.exists('dblp_index/Venue_Index'):
        os.makedirs("dblp_index/Pubblication_Index")
        os.makedirs('dblp_index/Venue_Index')
        
    pub_ix = create_in('dblp_index/Pubblication_Index',pub_schema)
    venue_ix = create_in('dblp_index/Venue_Index',venue_schema)
    
    pub_writer = pub_ix.writer(procs=4, limitmb=512, multisegment = True)
    venue_writer = venue_ix.writer(procs=4, limitmb=512, multisegment=True)
    
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        
    Handler = sax_handler.Pub_Handler(pub_writer)
    parser.setContentHandler( Handler )
    
    file = input('Inserire File xml.. :')
    path_xml = os.path.abspath(file)
    if os.path.exists(path_xml) :

        parser.parse(path_xml)
        print('Inizio la Commit del Pubblication Index... ')
        pub_writer.commit()
        print('Finita prima parte di indicizzazione..!')
        
        Handler = sax_handler.Venue_Handler(venue_writer)
        parser.setContentHandler( Handler )
        print("Inizio la seconda parte dell'indicizzazione")
        parser.parse(path_xml)
        print("Inizio la Commit di Venue Index")
        venue_writer.commit()
        print('Finita seconda parte di indicizzazione..!')
        print("Indicizzazione Completata..Enjoy =) ")
        
    else :
        print('Riprovare ! File Errato')
