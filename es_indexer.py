import json
import time 
from elasticsearch import Elasticsearch
import es_file_crawler

client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpointeger
)

#Test de réponse
#print(client.info())



def index_bird(client, nom_mapping, nom_index) : 
    with open(nom_mapping+".json","r") as file :
        mapping = json.load(file)

    #Reset index (ingnoré si l'index n'existe pas)
    client.options(ignore_status=[400,404]).indices.delete(index=nom_index)

    #Create index
    response = client.indices.create(
        index=nom_index,
        body=mapping,
        ignore=400
    )


    if 'acknowledged' in response:
        if response['acknowledged'] == True:
            print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])

    # catch API error response
    elif 'error' in response:
        print ("ERROR:", response['error']['root_cause'])
        print ("TYPE:", response['error']['type'])

    start_time = time.time()

    es_file_crawler.folder_crawl("/home/damidas/Bureau/Cours/Stage/Bird/bird/bird", client, nom_index)

    # Arrêtez le chronomètre
    end_time = time.time()
    # Calculez la durée d'exécution
    execution_time = end_time - start_time

    print(f"Le temps d'exécution pour {nom_mapping} était de {execution_time} secondes.")

index_bird(client, "mapping", "birds")
index_bird(client, "mapping-analyzer", "perf-birds")