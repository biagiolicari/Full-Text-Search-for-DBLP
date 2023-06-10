# Full-Text Search for DBLP

This university project aims to create a full-text search system for the DBLP (Digital Bibliography & Library Project) dataset. The system allows users to perform efficient text-based searches on the DBLP dataset, which contains bibliographic information about computer science publications.

## Installation

To install the required dependencies for the proper functioning of the application, follow these steps:

1. Navigate to the source code directory:
	```
	cd PATH/SORGENTE/DBLP_PROJECT
	```

2. Install the dependencies using the following command:
	```
	python setup.py install
	```

3. Once the installation of the various dependencies is complete, run the following command in the terminal:

	```
	python main.py
	```

The program will prompt you to provide the absolute path of the DBLP.xml file if the index has not been created yet. If the index has already been created, the program will load the index and ask you to enter the desired query using a simple syntax.



## Query Syntax

The following syntax should be followed when entering a query:
```
PUBTYPE.[title, author, year, etc.]:QUERY [RANKING...] [TOPK...]
```
If the syntax is not followed correctly, the program will default to searching in the AUTHOR-YEAR-TITLE fields in Publications and Venues, with the ranking set to FREQUENCY by default and TopK set to 50.

#### Example usage:

* To search for articles written by author "Montressor" using fuzzy ranking:
	```
	article.author:"Montressor" -fuzzy
	```
* To limit the search results to the top 10:
	```
	article.author:"Montressor" -10
	```
	
- Note: The available ranking options are '-vector' and '-fuzzy'.

## License
This project is licensed under the [MIT License](LICENSE).




