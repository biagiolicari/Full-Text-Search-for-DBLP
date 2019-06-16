# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 17:28:27 2019

@author: Biagio
"""

import xml.sax
from whoosh.index import create_in
from whoosh.fields import *


pubblication = ["article", "incollection", "phdthesis", "mastersthesis"]
venue = ['book','inproceedings']

class Venue_Handler( xml.sax.ContentHandler ):

   
   def __init__(self,writer):
      self.venueflag = False
      self.key = ""
      self.tag = ''
      self.author = ''
      self.title = ""
      self.journal = ''
      self.publisher = ''
      self.parent = False
      self.writer = writer
   
    
   def startDocument(self) :
       print('Indicizzazione dei Venue iniziata...')


   def endDocument(self):
        print('Parsing Completato...')    
   
    
   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag in venue :
          for single_tag in venue :
              if tag == single_tag :
                  self.venueflag = True
                  self.key = str(attributes['key'])
                  self.tag = tag
              else :
                  pass
              
      if tag in pubblication :          
          for single_tag in pubblication :
              if tag == single_tag :
                  self.parent = True
                  self.key = str(attributes['key']) 
                  self.tag = tag


   # Call when an elements ends
   def endElement(self, tag):
      if tag in venue :
          for single_tag in venue :
              if tag == single_tag :
                  
                  self.writer.add_document(pubtype = self.tag,
                                    key = self.key,                                    
                                    author = self.author, 
                                    title = self.title,
                                    publisher = self.publisher)
                  
                  self.venueflag = False
                  self.author = ''
                  self.title = ''
                  self.publisher = ''
                  self.key = ''
                  self.tag = ''
                  
                  
      if tag in pubblication :
          for single_tag in pubblication :
              if tag == single_tag :
                  
                  self.writer.add_document(pubtype = self.tag,
                                    key = self.key, 
                                    journal = self.journal)
                                    
                  self.parent = False
                  self.journal = ''
                  self.key = ''
                  self.tag = ''
             


# Call when a character is read
   def characters(self, content):
       if self.venueflag :
           if self.CurrentData == "author":
               self.author += str(content)
           elif self.CurrentData == "title":
                   self.title += str(content)
           elif self.CurrentData == "publisher":
                   self.publisher += str(content) 
       elif self.parent :
            if self.CurrentData == 'journal' :
                self.journal += content


class Pub_Handler( xml.sax.ContentHandler):

   
   def __init__(self,writer):
      self.parentflag = False
      self.key = ""
      self.tag = ''
      self.author = ''
      self.title = ""
      self.crossref = ''
      self.pages = ''
      self.year = ''
      self.writer = writer
      
   
    
   def startDocument(self) :
       print('Indicizzazione Pubblication iniziata...')



   def endDocument(self):
        print('Parsing Completato...')    
   
    
   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      for single_tag in pubblication :
          if tag == single_tag :
              self.parentflag = True
              self.key = str(attributes['key'])
              self.tag = tag
          


   # Call when an elements ends
   def endElement(self, tag):
          if self.tag == tag :

           self.writer.add_document(pubtype = self.tag,
                                    key = self.key,                                    
                                    author = self.author, 
                                    title = self.title,
                                    pages = self.pages,
                                    crossref = self.crossref,
                                    year = self.year)
             
           self.parentflag = False
           
           self.author = ''
           self.title = ''
           self.pages = ''
           self.crossref = ''
           self.year = ''
           self.key = ''
           self.tag = ''
         
           

# Call when a character is read
   def characters(self, content):
       if self.parentflag :
           if self.CurrentData == "author":
               self.author += str(content)
           elif self.CurrentData == "title":
                   self.title += str(content)
           elif self.CurrentData == "pages":
                   self.pages += str(content) 
           elif self.CurrentData == "crossref":
                   self.crossref += str(content)
           elif self.CurrentData == "year":
                   self.year += str(content) 