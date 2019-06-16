# Full-Text-Search-for-DBLP
Progetto universitario per la creazione di un Full text search su DBLP


Per installare le dipendenze necessarie al corretto funzionamento dell'aplicativo eseguire i seguenti comandi :

cd PATH/SORGENTE/DBLP_PROJECT
python setup.py install

ad installazione di dipendenze varie finita, eseguire il seguente comando sempre da prompt :

python main.py

il programma si aprirà chiedendo di dare l'absPath del file DBLP.xml qualora l'indice non  sia stato già creato.
Nel caso l'indice sia già creato, il programma, dopo il caricamento dell'indice, chiederà di digitare la query richiesta seguendo una semplice sintassi da rispettare.



ESEMPIO SINTASSI : 

PUBTYPE.[title,author,year,ecc..]:**QUERY** [RANKING...] [TOPK...]


Nell'eventualità in cui non si rispettasse tale sintassi, il programma è predisto alla ricerca nei campi AUTHOR-YEAR-TITLE nei Pubblication e nei Venue, con Ranking pari a FREQUENCY di default e TopK pari a 50.


[RANKING...] = digitare uno dei ranking implementati fra ['-vector','-fuzzy']  :
	ESEMPIO : article.author:"Montressor" -fuzzy ( per usare il ranking fuzzy)


[TOPK...] = inserire un numero decimale intero :
	ESEMPIO : article.author:"Montressor" -10 

