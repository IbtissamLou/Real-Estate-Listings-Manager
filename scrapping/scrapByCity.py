from scrapping.scrap_pv_immo import list_annonce
from dao.dbconnection import DBConnection
from dao.villeDAO import VilleDAO

class ScrapByCity():
    """
    Classe implémentant le scrapping selon une ville choisie par l'utilisateur, fait le lien avec  les codes INSEE


    """
    def __init__(self, ville:str):
        self.ville = ville
    
    def annoncesByCity(self) -> list:
        code_insee = VilleDAO().get_insee(self.ville)
        return(list_annonce(count=3,insee= code_insee))

    