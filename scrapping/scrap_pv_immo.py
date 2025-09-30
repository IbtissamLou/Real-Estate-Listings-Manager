import re
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
from business_object.annonce import Annonce
from dao.villeDAO import VilleDAO
class Scrapping():

    def __init__(self,ville,count=3):
        self.count=count
        self.ville=ville

    def clean_price(self,tag):
        """ Enlève le symbole euros et les textes d'une chaine de caractère contenant un prix"""
        text=tag.text.strip()
        n_prix=text.split("€",1)[0]    #enleve tout après la 1e occurence de euros. on avait  21 300 €\nà débattre avant on passe à 21 300 €
        price = n_prix.replace("€", "").replace(" ", "") #enleve le symbole €
        price=re.sub('\D', '', price) #Dans le cas ou la valeur est "à partir de X" (euros), on enlève les lettres afin d'avoir  X, le prix numérique
        return price

    def parse_page(self,page):
        """Crée un dataframe avec les informations pertinentes d'une annonce du  site"""
        a=pd.DataFrame()
        soup=BeautifulSoup(page,"html.parser")
        #Dans la classe donnée, on a les odnnées en format [nb_pièce, surface, city, nb_pieces, surface , city....]
        a["Cara"]= [tag.text.strip() for tag in soup.find_all('span',attrs={"class":"px-2 text-black whitespace-nowrap"})]
        len_a= a.shape[0] #Donne le nombre de ligne de a
        #On definit un dataframe dff qui decoupe bien les données de "a " de facon "périodique"
        try :
            dff=pd.DataFrame({"Nombre_piece": [a["Cara"][i] for i in  range(0,len_a,3)],
                            "surface":[a["Cara"][i+1] for i in  range(0,len_a,3)],
                            "city":[a["Cara"][i+2] for i in  range(0,len_a,3)] })
            dff['surface'] = dff['surface'].map(lambda x: x.lstrip('+-').rstrip('m²m2'))
            dff["type"]=[elem.split()[0] for elem in dff["Nombre_piece"] ]   #Premier mot du nom de l'article en général
            dff["price"]= [Scrapping(self.ville).clean_price(tag) for tag in soup.find_all(attrs={"class":"flex justify-center items-center w-full gap-4 text-lg sm:text-base text-red font-medium border-1 border-red p-1 mb-2 sm:my-2"})]

            dff["room"]=[elem.split()[1] for elem in dff["Nombre_piece"] ]   #Deuxième mot du nom de l'article en général
            
            #Lien URL
            rrr=soup.find_all('a',class_="h-10 text-sm bg-red text-white hover:text-white hover:bg-red-dark block px-2.5 w-max leading-10",href=re.compile("^/immobilier/"))
            liste_lien= ["https://www.paruvendu.fr"+ link.get('href') for link in rrr]   #Liste de lien
            dff["source"]=pd.Series(liste_lien,dtype='object')
            
            liste_lien_parse=[str(elem).split('/') if elem is not None else None for elem in liste_lien]    # Dataframe de liste parsés
            # dff["title"]=pd.Series([elem[6] if elem is not None else None for elem in liste_lien_parse ])
            list_title=[elem[6] if elem is not None else None for elem in liste_lien_parse ]
            dff["title"]=pd.Series([str(s).replace("-", " ") for s in list_title ],dtype='object')
            
            dff["agency"]=pd.Series([tag.text.strip() for tag in soup.find_all('span',attrs={"class":"text-black line-clamp-1 max-w-64 float-none h-5 block"})],dtype='object')
            dff=dff.drop("Nombre_piece",axis=1) # Variable qui regroupe Type de structure et nombre de pièces
            
            #Lien image
            r_img=soup.find_all('img',class_="w-full object-cover h-50")
            dff["url_image"]=pd.Series([link.get('original') for link in r_img],dtype='object')

            dff['description']=[child.find(class_="text-sm text-justify").get_text().replace('\r\n',"") for child in soup.find_all(class_="flex flex-col my-2 gap-1")]
            #.capitalize() si besoin

            dff['description']=[child.find(class_="text-sm text-justify").get_text().replace('\r\n',"") for child in soup.find_all(class_="flex flex-col my-2 gap-1")]
        #.capitalize() si besoin
        except KeyError:
            print("Ville indisponible.")
            dff = None
        return dff

    def parse_pages(self):
        """Applique parse_page pour les differentes pages du site d'annonce
        
        
        Parameters
        -----------
        count: int
            Nombre de page du site que l'utilisateur veut
        
        Returns
        --------
        pd.DataFrame
        """
        results=pd.DataFrame()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        insee=VilleDAO().get_insee(self.ville)
        for i in range(1,self.count+1):
            url=f"https://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbApp=1&tbDup=1&tbChb=1&tbLof=1&tbAtl=1&tbPla=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&at=1&nbp0=99&pa=FR&lol=5&ray=50&codeINSEE={insee},&p={i}"
            page = requests.get(url,headers=headers).text
            result=Scrapping(self.ville,self.count).parse_page(page)
            #On ajoute le dataframe obtenu au dataframe initialisé, on obtient à la fin un dataframe contenant les informations de plusieurs pages
            results=pd.concat([results,result])
        #Pour avoir des indices croissants  
        results=results.reset_index(drop=True)
        #Ajout de la variable id_annonce
        results.insert(0,'id_annonce',[i for i in range(1,len(results)+1) ])
        return results

    def list_annonce(self):
        """Convertit le dataframe obtenu precedemment en liste d'objet Annonce
        Parameters
        -----------
        count: int =2
            Nombre de page du site que l'utilisateur veut

            
        Returns
        -------
        list(Annonce())
        """
        pages=Scrapping(self.ville,self.count).parse_pages()
        data=[Annonce(row.at["id_annonce"],
                        row.at["city"], 
                            row.at["url_image"],
                            row.at["source"],
                            row.at["price"],
                            row.at["type"],
                            row.at["surface"],
                            row.at["room"],
                            row.at["agency"],
                            row.at["description"],
                            row.at['title']) for index, row in pages.iterrows()]
        return data

# changer le departement: https://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?nbp=0&tt=1&tbApp=1&tbDup=1&tbChb=1&tbLof=1&tbAtl=1&tbPla=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&at=1&nbp0=99&pa=FR&lo={num_departement}&ddlFiltres=nofilter&codeINSEE=,
