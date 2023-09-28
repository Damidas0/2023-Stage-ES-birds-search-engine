import json
from elasticsearch import Elasticsearch

client = Elasticsearch('http://localhost:9200')



def search_multiple_from_file(client, nom_fichier, nom_index, nom_output) : 
    f = open(nom_output+".txt", "w")
    with open(nom_fichier+".json", 'r') as file:
        queries = json.load(file)

    for i, query in enumerate(queries, start=1) :
        try : 
            resp = client.search(index=nom_index, body = query) 
            f.write(f"{str(resp['took'])} {str(resp['hits']['max_score'])} {str(resp['hits']['total'])} \n")
        except Exception as e: 
            print(f"Error query {i} : {str(e)}")


search_multiple_from_file(client, "queries", "birds", "output-no-analyzer")

