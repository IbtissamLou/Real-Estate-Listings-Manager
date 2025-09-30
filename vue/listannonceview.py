from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator
from InquirerPy.validator import NumberValidator

from vue.abstractview import AbstractView
from vue.session import Session
from vue.annonceview import AnnonceView

from dao.annonceDAO import AnnonceDAO
from business_object.annonce import Annonce

from datetime import datetime

from service.rechercheFiltre import RechercheFiltre
from dao.historicDAO import HistoricDAO
from dao.userDAO import UserDAO

class AnnonceListView(AbstractView):
    """
    Implémente la vue sur les annonces listées.

    Attributes
    ----------
    page : int =0
        numéro de la page affichée
    elem_by_page : int = 10 
        Nombre d'annonces par page
    data : list[Annonce]
        Liste des annonces correspondant aux critères retournée par le fetchall 
    max_page : int
        page maximale explorable
    EXPLORATEUR : inquirer.select()
        Ensemble des choix que l'utilisateur peut réaliser sur la vue
    """
    def __init__(self, page : int = 0, elem_by_page: int =10):
        #Constructeur de la classe
        self.page = page
        self.elem_by_page = elem_by_page
        self.data = Session().data
        self.max_page = len(self.data)//self.elem_by_page
        if page == self.max_page :
            self.EXPLORATEUR = inquirer.select(
                    message = f'Voici nos magnifiques et mirobolantes annonces'
                    , choices=[
                    Choice('Une annonce m\'intéresse')
                    ,Choice('Rechercher un terme')
                    ,Choice('Page précédente') #enlever
                    ,Choice('Filtrer les annonces') #enlever 
                    ,Choice('Retourner au menu')])
        if self.page == 0 :
            self.EXPLORATEUR = inquirer.select(
                    message = f'Voici nos magnifiques et mirobolantes annonces'
                    , choices=[
                    Choice('Une annonce m\'intéresse')
                    ,Choice('Rechercher un terme')
                    ,Choice('Page suivante')
                    ,Choice('Filtrer les annonces')
                    ,Choice('Retourner au menu')])
        else :
            self.EXPLORATEUR = inquirer.select(
                    message = f'Voici nos magnifiques et mirobolantes annonces'
                    , choices=[
                    Choice('Une annonce m\'intéresse')
                    ,Choice('Rechercher un terme')
                    ,Choice('Page précédente')
                    ,Choice('Page suivante')
                    ,Choice('Filtrer les annonces')
                    ,Choice('Retourner au menu')])

    def display_info(self):
        #Informations fixes sur la page
        with open('graphical_assets/banner.txt', 'r', encoding="utf-8") as asset:
            print(asset.read())
        for i in range(self.page*self.elem_by_page, min(len(self.data),self.page*self.elem_by_page + self.elem_by_page)):
            print("{}\n\nAnnonce n°{}".format(self.data[i].title, self.data[i].id_annonce)+"\n"+str(self.data[i]))
            print('»»————-　★　————-««')
    
    def make_choice(self):
        #Choix sur la page
        choosed = self.EXPLORATEUR.execute()
        if choosed == 'Une annonce m\'intéresse':
            id_to_see = inquirer.number(
                message='Quel numéro d\'annonce ?'
                ,min_allowed=0
                ,validate=EmptyInputValidator('L\'entrée est vide') and NumberValidator(message='Doit être un entier')
            )
            id_choosen = id_to_see.execute()
            annonce = RechercheFiltre(Session().data).filtre_by_id(int(id_choosen))
            Session().id_annonce = id_choosen
            if Session().user_email is not None:
                id_historic = AnnonceDAO().post_annonce(annonce.city, annonce.url_image, annonce.source, annonce.price, annonce.kind, annonce.surface, annonce.room, annonce.agency, annonce.description, annonce.title)
                date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                id = UserDAO().get_id_by_email(Session().user_email)
                HistoricDAO().add_historic(id, id_historic, date_and_time)
            import os
            os.system('cls')
            return AnnonceView(id_choosen)

        elif choosed == 'Page suivante': 
            return AnnonceListView(page=self.page + 1) 

        elif choosed == 'Page précédente':
            return AnnonceListView(page=self.page - 1) 
        elif choosed == 'Retourner au menu':
            if Session().user_email is not None:
                from vue.menu2view import Menu2View
                return Menu2View()
            else:
                from vue.menuview import MenuView
                return MenuView()
        
        elif choosed == 'Filtrer les annonces': 
            from vue.filterview import FilterView
            return FilterView()
        
        elif choosed == 'Rechercher un terme' :
            from service.rechercheMotClef import RechercheMotClef
            terme = inquirer.text(
                message ="Que recherchez vous ?",
                completer = RechercheMotClef().get_all(),
                multicolumn_complete=True
                ).execute()
            Session().data = RechercheMotClef().filtre_mot_clef(terme)
            import os
            os.system('cls')
            return AnnonceListView()

