from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from os import listdir
from os.path import isfile, join
# import required module
import unidecode

    
#faire du multi index pour animaux de fr/eur/monde etc. d'après l'orga du site (qu'on peusse cocher) 
    

#on veut pas charger les images / le JS et on va le mettre en arrière plan (il y a 11000 pages à atteindre)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images" : 2})
chrome_options.add_argument('--headless')



def crawl_table(driver, max_depths, log) : 
    global chrome_options
    liste_lien = driver.find_elements(By .TAG_NAME, 'table')
    if (liste_lien == "" or max_depths == 0): 
        return get_fiche(driver, log)
    else :
        subdriver = webdriver.Chrome(chrome_options=chrome_options, executable_path = "chromedriver.exe")
        for element in liste_lien : 
            lien = element.find_elements(By .TAG_NAME, 'a')
            for l in lien : 
                subdriver.get(l.get_attribute('href'))
                crawl_table(subdriver, max_depths - 1, log)


def get_fiche(driver, log):
    o_nom = driver.find_element(By .CLASS_NAME, 'titre').text
    o_nom_lat = driver.find_element(By .CLASS_NAME, 'binominal').text+ "\n"
    log.write (o_nom)
    o_protec_indice = getIndiceProtection(driver)
    
    try : #espce ordre toussa
        fiche_internet = driver.find_element(By .CLASS_NAME, 'biometrie') #Recup fiche 
        table = fiche_internet.find_elements(By .TAG_NAME, 'li') 
        tab_p = fiche_internet.find_elements(By .TAG_NAME, 'p')
        o_ordre = getChamp(table[0]) + "\n"
        o_famille = getChamp(table[1]) + "\n"
        o_genre = getChamp(table[2])+ "\n"
        o_espece = getChamp(table[3]) + "\n"
    except : 
        o_ordre = o_famille = o_genre = o_espece = "-\n"
        log.write(" ELEMENTS_F")

    try: #info sur taillepoid
        o_taille = getChamp2(table[4]) + "\n"
        o_env = getChamp2(table[5]) + "\n"
        o_poid = getChamp2(table[6]) + "\n"
    except:
        o_taille = o_env = o_poid  = "-\n"
        log.write("INF_F")

    try : #longevite
        o_longevite = tab_p[5].text +"\n"
        if(o_longevite == '\n') : 
            o_longevite = "-\n"
    except : 
        o_longevite = "-\n"
        log.write("LONG_NF")
    
    try : #Découverte
        o_descripteur = fiche_internet.find_element(By .CLASS_NAME, 'authority').text +"\n"
    except : 
        o_descripteur = "-\n"
        pass
    
        
    try : #noms étrangers
        o_nom_etranger = driver.find_element(By .CLASS_NAME, 'box_synonyme').text+ "\n"
    except : 
        o_nom_etranger = "-\n"
        log.write(" NOMS_E_F")


    o_desc = getCategorie(driver, 'description-esp', log) 
    o_chant = getCategorie(driver, 'chant', log)
    o_habitat = getCategorie(driver, 'habitat', log)
    o_comportement = getCategorie(driver, 'comportement', log)
    o_alim = getCategorie(driver, 'regime', log)
    o_repr = getCategorie(driver, 'reproduction', log)
    o_vol = getCategorie(driver, 'vol', log)
    o_distrib = getCategorie(driver, 'distribution', log)
    o_protec = getCategorie(driver, 'protection', log)

    #creation fichier mémoire
    name = o_nom
    name = name.replace(" ", "_")
    name = name.lower()
    log.write("\n")
    fichier = open("piaf/"+ name + ".txt", encoding='UTF-8', mode = 'w')
    fichier.write(o_nom+"\n"+ o_nom_lat+ o_ordre+ o_famille+ o_genre + o_espece)
    fichier.write(o_descripteur)
    fichier.write(o_protec_indice+'\n' + o_taille + o_env + o_poid +o_longevite+o_nom_etranger)
    fichier.write(o_desc+ o_chant + o_habitat +o_comportement +o_vol+ o_alim + o_repr + o_distrib + o_protec)
    fichier.close()
    
#Fonction qui balise et renvoi le texte associé à une catégorie de page
def getCategorie(driver, nom_champ, fichier_log) :
    try :  
        champ = driver.find_element(By .ID, nom_champ)
        balise = "<" + nom_champ + ">"
        return ("\n" + balise +"\n" + champ.text +"\n"+ balise + "\n")
    except : 
        fichier_log.write(" "+nom_champ[:5].upper()+"_NF")
        return ""

def getIndiceProtection(driver) :
    listeInd = ['ex', 'ew', 'cr', 'en', 'vu', 'nt', 'lc', 'ne']
    for i in listeInd : 
        if (len(driver.find_elements(By .CLASS_NAME, 'on_iucn_' + i)) > 0) : 
            return i
    return ''

def getChamp2(ligne) : 
    champ2 = ligne.text.split(' ')[2:]
    champ2 = ' '.join(champ2)
    return champ2

def getChamp(ligne) : 
    return ligne.find_element(By .TAG_NAME, 'p').text





def exploration_site(driver, iteration, log) : #version pour pas repartir de 0
    liste_lien = driver.find_elements(By .CLASS_NAME, 'on-liste' )
    global chrome_options
    i=0
    for e in liste_lien : 
        
        i+=1
        if i == 2 : 
            break   
        else : 
            liste_lien = e.find_elements(By .TAG_NAME, 'div')#on va chercher chaque ligne 
            j=0
            for element in liste_lien : #pour chacune des lignes on récup la fiche récursivement
                j+=1 
                if j < iteration : 
                    continue
                else :
                    lien = element.find_element(By .TAG_NAME, 'a')
                    subdriver = webdriver.Chrome(chrome_options = chrome_options, executable_path = "chromedriver.exe")
                    subdriver.get(lien.get_attribute('href'))
                    crawl_table(subdriver, 2, log)

#Suppression des texte non voulu                
def clean_doc(repertoire):
    symbol_suppr = ['♀', '♂']
    symbol_suppr_avec_ligne_suiv = ['♫']
    ligne_suppr=['adulte plum. nuptial\n', 'EX EW CR EN VU NT LC NE\n', 'à l\'état sauvage\n', 'Statut de conservation IUCN\n', \
        'Voix chant et cris\n', 'Description identification\n', 'Alimentationmode et régime\n', 'Reproduction nidification\n', \
        'Menaces - protection\n', 'adulte plum. transition\n', 'adulte plum. internuptial\n', 'Comportement traits de caractère\n'\
        'plum. internuptial\n']
    #on recup tout les fichiers du dossiers (en ignorant ceux qui en sont pas)
    nom_fichiers = [f for f in listdir(repertoire) if isfile(join(repertoire, f))] 
    print(os.getcwd())
    for n_fichier in nom_fichiers :
        
        with open(repertoire + n_fichier, 'r',encoding='UTF-8') as f: 
            l_fichier = f.readlines()
        with open(repertoire + n_fichier, 'w', encoding='UTF-8') as f: 
            doit_suppr = False
            in_balise = False 
            for ligne in l_fichier : 
                nb_bal = nb_balise(ligne)
                l_split = ligne.split(" ")
                
                #On recopie la ligne ssi elle est pas a supprimer càd qu'elle :
                if ((not in_balise or nb_bal == 1) or \
                #est pas dans une balise OU
                (not doit_suppr and \
                #ne doit pas être suppr (d'après contenu ligne d'avant) ET
                len(l_split)>1 and\
                #si c un pas seul mot ET
                ligne[0] not in symbol_suppr and\
                #ne commence pas par un symbole maudit ET
                ligne[0] not in symbol_suppr_avec_ligne_suiv and\
                #no commence pas avec un symbole maudit et qui maudit ligne d'après ET
                ligne not in ligne_suppr)) : 
                    doit_suppr = False
                    f.write(ligne)
                
                
                if (nb_bal == 1) : 
                    in_balise = not in_balise
                
                else : 
                    doit_suppr = False
                    if ligne[0] in symbol_suppr_avec_ligne_suiv :
                        doit_suppr = True

def accentless(repertoire) :
    nom_fichiers = [f for f in listdir(repertoire) if isfile(join(repertoire, f))] 
    for n_fichier in nom_fichiers:
        #with open(repertoire+n_fichier, 'w', encoding='UTF-8') as f:
        new_nom_f = unidecode.unidecode(n_fichier)
        print(new_nom_f)
        os.rename(repertoire+n_fichier, repertoire+new_nom_f)
            


def nb_balise(ligne) : #permet de savoir s'il y a un mot de la forme "<balise>"
    nb_balise = 0
    ligne = ligne.split(" ")
    for mot in ligne : 
        ouvrant = mot.count("<")
        nb_balise += ouvrant
    return nb_balise


log =  open("log.txt", "w", encoding='UTF-8')

#verification validité chemin
chemin=os.getcwd()
print(chemin)
os.chdir(chemin)
try : 
    os.makedirs("piaf")
except :
    pass

accentless("piaf/")
#clean_doc("piaf/")

#driver = webdriver.Chrome(chrome_options=chrome_options ,executable_path = "chromedriver.exe")
#driver.get("https://www.oiseaux.net/oiseaux/")

#exploration_site(driver, 0, log)
