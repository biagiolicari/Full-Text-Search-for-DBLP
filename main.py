from query import search
from index.sax_handler import *
from index.DBLP_Indexer import *
import xml.sax
from whoosh.index import create_in
from whoosh.fields import *
import os
if __name__ == "__main__":


    if os.path.exists("index/dblp_index/Pubblication_Index") and os.path.exists('index/dblp_index/Venue_Index'):
        search.start()

    else :

        pub_schema, venue_schema = create_scheme()

        if not os.path.exists("index/dblp_index/Pubblication_Index") and not os.path.exists('index/dblp_index/Venue_Index'):
            os.makedirs("index/dblp_index/Pubblication_Index")
            os.makedirs('index/dblp_index/Venue_Index')

        pub_ix = create_in('index/dblp_index/Pubblication_Index', pub_schema)
        venue_ix = create_in('index/dblp_index/Venue_Index', venue_schema)

        pub_writer = pub_ix.writer(procs=4, limitmb=512, multisegment=True)
        venue_writer = venue_ix.writer(procs=4, limitmb=512, multisegment=True)

        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        Handler = Pub_Handler(pub_writer)
        parser.setContentHandler(Handler)

        file = input('Inserire File xml.. :')
        path_xml = os.path.abspath(file)
        if os.path.exists(path_xml):

            parser.parse(path_xml)
            print('Inizio la Commit del Pubblication Index... ')
            pub_writer.commit()
            print('Finita prima parte di indicizzazione..!')

            Handler = Venue_Handler(venue_writer)
            parser.setContentHandler(Handler)
            print("Inizio la seconda parte dell'indicizzazione")
            parser.parse(path_xml)
            print("Inizio la Commit di Venue Index")
            venue_writer.commit()
            print('Finita seconda parte di indicizzazione..!')
            print("Indicizzazione Completata..Enjoy =) ")

        else:
            print('Riprovare ! File Errato')


