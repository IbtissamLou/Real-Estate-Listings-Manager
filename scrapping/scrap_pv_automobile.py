import re
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
from business_object.annonce import Annonce
from dao.villeDAO import VilleDAO
class Scrapping_automobile():

    def __init__(self,ville,count=2):
        self.ville=ville
        self.count=count

    def list_category(self,data):
        all_category=[]
        for elem in data:
            if elem.kind not in all_category :
                all_category.append(elem.kind)
        return all_category

    def list_ville(self,data):
        all_cities=[]
        for elem in data:
            if elem.city not in all_cities :
                all_cities.append(elem.city)
        return all_citie
    
    def parse_pages(self):
        """Applique parse_page pour les differentes pages du site d'annonce, puis conversion du dataframe en json/dictionnaire"""
        #Dossier ou se trouve les pages html sauvegardé localement
        results=pd.DataFrame()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        insee=VilleDAO().get_insee(self.ville)
        for i in range(1,self.count+1):
            url=f'https://www.paruvendu.fr/auto-moto/listefo/default/default?origine=affinage&tri=indiceQualite&ord=desc&np=&r=VO&trub=&ty=&r2=&codeINSEE={insee},&lo=&pa=&ray=15&px0=&px1=&nrj=&co2=&critair=&a0=&a1=&km0=&km1=&npo=&tr=&fulltext=&codPro=&pf0=&pf1=&p={i}'
            page = requests.get(url,headers=headers).text
            result=Scrapping_automobile(self.ville,self.count).parse_page(page)
            #On ajoute le dataframe obtenu au dataframe initialisé, on obtient à la fin un dataframe contenant les informations de plusieurs pages
            results=pd.concat([results,result])
        #Pour avoir des indices croissants  
        results=results.reset_index(drop=True)
        #Ajout de la variable id_annonce
        results.insert(0,'id_annonce',[i for i in range(1,len(results)+1) ])
        return results


    def parse_page(self,page):
        result=pd.DataFrame()
        soup=BeautifulSoup(page,"html.parser")
        
        #Les variables concernant l'article
        rr=soup.find_all("div",class_="ergov3-txtannonce ergov3-txtannonce-auto")
        a=[elem.find('h3') for elem in rr]
        result["name of the article"]=[item.text.strip() for sublist in a for item in sublist]
        result["brand"]=[elem.split()[0] for elem in result["name of the article"] ]   #Premier mot du nom de l'article en général
        result["energy"]= pd.Series([tag.text.strip() for tag in soup.find_all('span',attrs={"class":"nrj"})])
        result["price"]= [Scrapping_automobile(self.ville,self.count).clean_price(tag) for tag in soup.find_all(attrs={"class":"ergov3-priceannonce-auto"})]
        result["city"]= [Scrapping_automobile(self.ville,self.count).clean_city(tag) for tag in soup.find_all(attrs={"class":"infos-mea-auto infos-loc"})]
        result["release date of the article"]= [Scrapping_automobile(self.ville,self.count).clean_year(tag) for tag in soup.find_all(attrs={"class":"annee"})]
        result["mileage"]= pd.Series([Scrapping_automobile(self.ville,self.count).clean_km(tag) for tag in soup.find_all(attrs={"class":"km"})])

        #Lien URL
        rrrr=soup.find_all('a',class_="voirann",href=re.compile("^https://www.paruvendu.fr"))

        #Lien image
        r_img=soup.find_all(class_="img ergov3-imgannonce")
        ab=[elem.find('img') for elem in r_img]
        result["url_image"]=pd.Series([link.get('original') for link in ab])
        result["source"]=[link.get('href') for link in rrrr ]
        return result

        
    def clean_city(self,tag):
        text=tag.text.strip()
        n_ville = text.replace("\t", "")
        return n_ville

    def clean_price(self,tag):
        text=tag.text.strip()
        n_prix=text.split("€",1)[0]    #enleve tout après la 1e occurence de euros. on avait  21 300 €\nà débattre avant on passe à 21 300 €
        price = n_prix.replace("€", "").replace(" ", "") #enleve le symbole €
        price=re.sub('\D', '', price)
        return price

    def clean_year(self,tag):
        text = tag.text.strip()
        return text.replace("Année", "")

    def clean_km(self,tag):
        text = tag.text.strip()
        return text.replace("km", "")

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

result2=Scrapping_automobile('Aubervilliers',2).parse_pages()
print(result2)


