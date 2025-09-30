from dao.annonceDAO import AnnonceDAO

from outil.singleton import Singleton

from business_object.filtre import Filtre
from business_object.particulier import Particulier

class Session(metaclass=Singleton):
    """
    Permet de stocker les données d'une session, instancié sous forme de singleton pour garantir l'unicité

    ...

    Attributes
    ----------
    user : particulier or admin or professionnel
        profil utilisateur connecté
    data : list[Annonce] = AnnonceDAO().get_all()
        annonces filtrés par l'utilisateur lors de sa session, par défaut toutes
    filtres_actifs : list[Filtre] = []
        filtres actifs durant la session, par défaut aucun
    """  
    def __init__(self):
        """
        Constructeur de la classe
        """   
        self.selected_user = None
        self.user_id = None
        self.user_name = None
        self.user_prenom = None
        self.user_email = None
        self.id_annonce = None
        self.data = None
        self.filtres_actifs = []
        self.ville_scrap = None
        self.is_connected = False