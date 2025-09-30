from business_object.annonce import Annonce
from vue.session import Session

class RechercheMotClef():
    """
    Permet d'accéder aux éléments utiles pour une recherche par mot clefs

    Arguments:
    --------
    data : list[Annonce] = Session().data
        Ensemble d'annonces d'où l'on veut extraire les mots clefs

    Methods:
    --------
    get_all() : dict
        retourne une liste des mots clefs de la base de données
        Permettra de constituer le completer de Inquirerpy
    filtre_mot_clef()
    """
    def __init__(self, data= Session().data):
        self.data = data

    def get_all(self) -> dict:
        mots_clefs = []
        for i in self.data : #On récupère les élements en liste
            mots_clefs.append(i.city)
            mots_clefs.append(i.agency)
            mots_clefs.extend(str(i.description).split())#On décompose les textes par terme sous forme de liste
            mots_clefs.extend(str(i.title).split())
        mots_clefs = [*set(mots_clefs)]  #On s'assure qu'il n'y est pas de doublons
        #Le format du completer d'inquirerpy exige un dictionnaire lié à None pour chaque terme
        completer = {str(i):None for i in mots_clefs}
        return completer

    def filtre_mot_clef(self, terme):
        """
        Filtre qui permet de récupérer les annonces contenant le mot clef
        Attributes:
        -----------
        terme : str = None
            Terme pour effectuer la recherche et le filtrage des annonces
        """
        filtered=[] #stockage des données après traitement
        for i in self.data:
            if terme.lower() in str(i.city).lower() or terme in str(i.agency).lower() or terme in str(i.description).lower() or terme in str(i.title).lower():
                filtered.append(i)
        return filtered