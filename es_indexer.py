import json
from elasticsearch import Elasticsearch
import es_file_crawler

client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpointeger
)

#Test de réponse
#print(client.info())

with open("mapping.json","r") as file :
    mapping = json.load(file)


#Reset index (ingnoré si l'index n'existe pas)
client.options(ignore_status=[400,404]).indices.delete(index='birds')

#Create index
response = client.indices.create(
    index="birds",
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


es_file_crawler.folder_crawl("/home/damidas/Bureau/Cours/Stage/Bird/bird/bird", client, "birds")


