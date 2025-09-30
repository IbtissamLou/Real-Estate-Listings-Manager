from business_object.annonce import Annonce
from dao.annonceDAO import AnnonceDAO
from scrapping.scrap_pv_immo import Scrapping
import requests

class RechercheFiltre():
    """
    Classe de l'ensemble des méthodes permettant de filtrer les données scrappés sur les sites d'annonce
    Attributs:
    --------
    data : list(Annonce)
        Annonces sur lesquels sera appliqué les filtres
    Methods:
    --------
    __init__(data:list)
        constructeur de la classe

    filtre_str(discrim:str, attribute : stre):list[Annonce]
        A partir d'une variable text spécifiée, retourne uniquement les annonces ayant la même valeur que discrim.

    filtre_categorie(category:str):list[Annonce]
        A partir d'une catégorie spécifiée, retourne uniquement les annonces relatives à cette dernière.
    
    localiser_ann(self,id): str
        Retourne la ville d'une annonce à partir de son identifiant

    filtre_by_id(id_annonce : int):Annonce
        A partir d'un id spécifié, retourne uniquement l'annonce relative
    
    filtres(var:list(str),values:list(list)): list(Annonce)
        Filtre sur les variables spécifiée dans la liste var et selon l'encadrement de valeurs de values.
    
    list_category():list(str)
        Retourne une liste des catégories représentées dans les annonces

    list_ville():list(str)
        Retourne une liste des catégories représentées dans les annonces
    """
    def __init__(self,data):
        self.data=data

    def filtre_str(self, discrim:str, attribute:str):
        """
        Filtre qui permet de choisir de filtrer selon un texte
        Attributes:
        -----------
        discrim:str
            Terme qui permettra de discriminer les éléments
        attribute : str
            Attributs sur lequel portera le filtre
        """
        data2=[a.__dict__ for a in self.data] #Retourne une liste de dictionnaire des données
        filtered= list(filter(lambda x: x[attribute].lower() == discrim.lower(), data2)) #Liste de dictionnaires qui vérifient la catégorie donnée
        list_object=[Annonce(elem["id_annonce"],
                            elem["city"], 
                            elem["url_image"],
                            elem["source"],
                            elem["price"],
                            elem["kind"],
                            elem["surface"],
                            elem["room"],
                            elem["agency"],
                            elem["description"],
                            elem["title"]) for elem in filtered]
        #Elem est un dictionnaire, on recupère les valeurs de chaque clés (variables) 
        # Ainsi, chaque element de la liste est une instance d'annonce
        return list_object
    
    def filtre_by_id(self,id_annonce:int):
        """Filtre qui permet de choisir une annonce avec son id
        Attributes:
        -----------
        id:int()
            l'id choisit
        """
        data2=[a.__dict__ for a in self.data] #Retourne une liste de dictionnaire des données
        filtered= list(filter(lambda x: x['id_annonce'] == id_annonce, data2)) #Liste de dictionnaires qui vérifient l'id donné
        list_object=[Annonce(elem["id_annonce"],
                            elem["city"], 
                            elem["url_image"],
                            elem["source"],
                            elem["price"],
                            elem["kind"],
                            elem["surface"],
                            elem["room"],
                            elem["agency"],
                            elem["description"],
                            elem["title"]) for elem in filtered]
        
        #Elem est un dictionnaire, on recupère les valeurs de chaque clés (variables) 
        # Ainsi, chaque element de la liste est une instance d'annonce
        return list_object[0]

    def filtres(self,var:list(str()),values:list(list())):
        """
        Filtres les annonces selon une variable et des valeurs
        La fonction permet in fine d'obtenir les annonces qui pour chaque variable dans la liste var, ont des valeurs 
        qui verifient les conditions définies par les sous-listes de la liste values

        Attributes :
        -----------
        var:list(str)
            Liste de variables sur lesquels nous appliqueront les filtres
        values:list(list) 
            Liste de liste. Les sous-listes  sont associés aux valeurs min et max qui vont encadrer les variables choisies
        """
        data2=[a.__dict__ for a in self.data] #Retourne une liste de dictionnaire des données
        filtered=data2
        for i in range(len(var)):
            #Filtres de varibles numériques
            if var[i] in ['price','surface','room']:
                filtered= list(filter(lambda x: values[i][0]<= int(x[var[i]])<=values[i][1], filtered)) 
            #Filtres de variables nominales
            else:
                filtered= list(filter(lambda x: x[var[i]] in values[i], filtered)) #Liste qui contient les dictionnaires qui verifient que la valeur i de value est une valeur de la clé var
        list_object=[Annonce(elem["id_annonce"],
                            elem["city"], 
                            elem["url_image"],
                            elem["source"],
                            elem["price"],
                            elem["kind"],
                            elem["surface"],
                            elem["room"],
                            elem["agency"],
                            elem["description"],
                            elem["title"]) for elem in filtered] 
        return list_object
        

    def localiser_ann(self,id):
        """
        Localise l'annonce de l'id donnée
        
        Attributes:
        -----------
        id : int
            id de l'annonce à chercher
        """
        data2=[a.__dict__ for a in self.data] #Retourne une liste de dictionnaire des données
        filtered=list(filter(lambda x: x['id_annonce'] == id , data2)) #Liste de dictionnaires qui vérifient l'id de l'annonce (unique) 
        new_dict = {i: d for i, d in enumerate(filtered)} #Conversion au format original( dictionnaire de dictionnaire)
        return new_dict[0]['city']

    def list_category(self):
        """
        Retourne l'ensemble des catégories présentent au sein des données 
        """
        all_category=[]
        for elem in self.data:
            if elem.kind not in all_category :
                all_category.append(elem.kind)
        return all_category
    
    def list_ville(self):
        """
        Retourne l'ensemble des villes représentées au sein des données 
        """
        all_cities=[]
        for elem in self.data:
            if elem.city not in all_cities :
                all_cities.append(elem.city)
        return all_cities