from click import open_file
#from bases import Base
import json
import gzip
from click import open_file
from dao.historicDAO import HistoricDAO

class ImpExp ():
    def __init__(self,emplacement,nom_fichier,extension):
        self.emplacement = emplacement
        self.nom_fichier = nom_fichier
        self.extension=extension

    def charger_donnees(self):
        """
        Permet de charger les données
        Arguments:
        -------
        emplacement : str .
        Il correspond à l'emplacement du fichier
        nom_fichier : str. 
        Il correspond au nom du fichier
        Returns : 
        ------
        None 
        """
        folder=self.emplacement
        filename=self.nom_fichier
        lien='\\\\'+ folder+'\\'+ filename + self.extension
        lien=str(r'{}').format(lien)
        try :
            with gzip.open(lien,mode="r", encoding='utf8') as gzfile:
                data=json.load(gzfile)
            self.donnees=data
        except:
            with open_file(lien,mode="r", encoding='utf8') as f:
                data=json.load(f)
            self.donnees=data
        return self.donnees

    def envoyer_donnees(self,liste_art_rech):
        liste=[a.__dict__ for a in liste_art_rech]
        liste2 = {i: d for i, d in enumerate(liste) } #Conversion au format original( dictionnaire de dictionnaire)
        folder=self.emplacement
        filename=self.nom_fichier
        lien='\\\\'+ folder+'\\'+ filename + self.extension
        chemin_f=str(r'{}').format(lien)
        json_object=json.dumps(liste2,ensure_ascii=False)
        with open(chemin_f, "w", encoding='utf8') as outfile:
            outfile.write(json_object)
        
    def envoyer_donnees_hist(self, liste):
        folder=self.emplacement
        filename=self.nom_fichier
        lien='\\\\'+ folder+'\\'+ filename + self.extension
        chemin_f=str(r'{}').format(lien)
        with open(chemin_f, "w", encoding='utf8') as outfile:
            for line in liste: 
                outfile.write(line)
                outfile.write('\n')

