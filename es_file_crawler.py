from os import listdir, getcwd
from os.path import isfile, join
import re

from elasticsearch import Elasticsearch


def folder_crawl(repertoire, client, indexName):
    #on recup tout les fichiers du dossiers (en ignorant ceux qui en sont pas)
    nom_fichiers = [f for f in listdir(repertoire) if isfile(join(repertoire, f))] 
    id_docs = 1

    for n_fichier in nom_fichiers :
        
        with open(repertoire + "/" + n_fichier, 'r',encoding='UTF-8') as f: 
            l_fichier = f.readlines()
        
        o_nom_commun = l_fichier[0]
        o_nom_latin = l_fichier[1]
        o_ordre = l_fichier[2]
        o_famille = l_fichier[3]
        o_genre = l_fichier[4]
        o_espece = l_fichier[5]
        o_descripteur = l_fichier[6].split(',')
        o_descripteur_nom = o_descripteur[0]
        o_descripteur_annee = re.sub(r'[^0-9]', '', o_descripteur[1])
        o_statut_conservation = l_fichier[7]
        o_taille = re.sub(r'[^0-9]', '', l_fichier[8])
        
#        if(l_fichier[9]=='-') : 
#            o_envergure=0
#        else :
#            o_envergure=  re.sub(r'[^0-9]', '', l_fichier[9]) # for l in l_fichier[9].split('à'))
        
        o_env_min, o_env_max = split_champ(l_fichier[9])
        o_poids_min, o_poids_max = split_champ(l_fichier[10])
#        if(l_fichier[10]=='-') : 
#            o_poids = 0
#        else :
#            o_poids=re.sub(r'[^0-9]', '', l_fichier[10])# for l in l_fichier[10].split('à'))

        o_longevite=re.sub(r'[^0-9]', '', l_fichier[11])

        o_nom_etranger_liste = l_fichier[12]

        o_description_espece, o_chant, o_habitat, o_comportement, \
        o_vol, o_regime_alimentaire, o_reproduction, o_distribution,\
        o_protection = read_paragraphes(l_fichier)
    
        doc = {
            'nom_commun': o_nom_commun,
            'nom_latin': o_nom_latin, 
            'ordre': o_ordre,
            'famille': o_famille,
            'genre': o_genre,
            'espece': o_espece,
            'descriteur_nom': o_descripteur_nom,
            'descripteur_annee': o_descripteur_annee,
            'status_conservation': o_statut_conservation,
            'taille_cm': o_taille,
            'envergure_min': o_env_min,
            'envergure_max': o_env_max,
            'poids_min': o_poids_min,
            'poids_max': o_poids_max, 
            'longevite': o_longevite,
            'nom_etranger_liste': o_nom_etranger_liste,
            'description_espece': o_description_espece,
            'chant': o_chant,
            'habitat': o_habitat,
            'comportement': o_comportement,
            'vol': o_vol ,
            'regime_alimentaire': o_regime_alimentaire,
            'reproduction': o_reproduction,
            'distribution': o_distribution,
            'protection': o_protection
        }

        resp = client.index(index = indexName, id=id_docs, document=doc)
        id_docs +=1
        #client.index(index="birds_log", document = resp)

def split_champ(ligne) : 
    if('à' in ligne) :
        splited = ligne.split('à')
        min = re.sub(r'[^0-9]', '', splited[0])
        max = re.sub(r'[^0-9]', '', splited[1])
        return min, max
    else :
        return 0,0

def read_paragraphes(tab_lignes_fichier) : 
    compteur = 14
    in_balise = False
    paragraphe =''
    o_description_espece = o_chant = o_habitat = o_comportement = o_vol = o_regime_alimentaire = o_reproduction = o_distribution = o_protection = ''
    while(compteur<len(tab_lignes_fichier)) :
        ligne = tab_lignes_fichier[compteur]
        if(est_balise(ligne)) : 
            in_balise = not in_balise
            if(not in_balise): 
                if "<description-esp>" in ligne :
                    o_description_espece = paragraphe
                elif "<chant>" in ligne : 
                    o_chant = paragraphe 
                elif "<habitat>" in ligne : 
                    o_habitat = paragraphe 
                elif "<comportement>" in ligne : 
                    o_comportement = paragraphe 
                elif "<vol>" in ligne : 
                    o_vol = paragraphe 
                elif "<regime>" in ligne : 
                    o_regime_alimentaire = paragraphe 
                elif "<reproduction>" in ligne : 
                    o_reproduction = paragraphe 
                elif "<distribution>" in ligne : 
                    o_distribution = paragraphe 
                elif "<protection>" in ligne : 
                    o_protection = paragraphe 
            else : 
                paragraphe =''
        else : 
            paragraphe += tab_lignes_fichier[compteur]
        compteur += 1
    return o_description_espece, o_chant, o_habitat, o_comportement, o_vol, o_regime_alimentaire, o_reproduction, o_distribution, o_protection

        
           


def get_paragraphe(compteur, tab_ligne_fichier) : 
    try : 
        compteur += 1
        paragraphe = ''
        while(not est_balise(tab_ligne_fichier[compteur])) :
            paragraphe += tab_ligne_fichier[compteur]
            compteur += 1
        return compteur, paragraphe
    except :
        return compteur, ''

def est_balise(ligne_tableau) :
    return('<' in ligne_tableau and '>' in ligne_tableau)

    