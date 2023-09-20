from elasticsearch import Elasticsearch
import es_file_crawler

client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpointeger
)

#Test de réponse
#print(client.info())

mapping = {
    "settings": {
        "number_of_shards": 1
    },
    "mappings": {
        "properties": {
            "nom_commun": {"type": "text"},
            "nom_latin": {"type": "text"}, 
            "ordre": {"type": "text"},
            "famille": {"type": "text"},
            "genre": {"type": "text"},
            "espece": {"type": "text"},
            "descriteur_nom": {"type": "text"},
            "descripteur_annee": {"type": "integer"},

            "status_conservation": {"type": "keyword"},

            "taille_cm": {"type": "integer"},
            "envergure_min": {"type": "integer"},
            "envergure_max": {"type": "integer"},

            "poids_min": {"type": "integer"}, 
            "poids_max": {"type": "integer"}, 

            "longevite": {"type": "integer"},

            "nom_etranger_liste": {"type": "text"},

            #Paragraphes
            "description_espece": {"type": "text"},
            "chant": {"type": "text"},
            "habitat": {"type": "text"},
            "comportement": {"type": "text"},
            "vol": {"type": "text"},
            "regime_alimentaire": {"type": "text"},
            "reproduction": {"type": "text"},
            "distribution": {"type": "text"},
            "protection": {"type": "text"}
        }
        
    }
}

#Reset index (ingnoré si l'index n'existe pas)
client.options(ignore_status=[400,404]).indices.delete(index='test-index')

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


