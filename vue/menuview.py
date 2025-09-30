from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy import prompts

from vue.abstractview import AbstractView
from vue.session import Session


#if Session().user_name == None :
msg_user = f'Bonjour, afin d\'accéder à plus de fonctionnalités veuillez vous enregistrer'
#else :
 #   msg_user =f'Bonjour {Session().user_name}'

QUESTIONS = inquirer.select(
            message = msg_user
        , choices=[
            Choice("Se connecter")
            ,Choice("Rechercher une annonce")
            ,Choice("Quitter")])

class MenuView(AbstractView):
    """
    Instancie le menu sur lequel l'utilisateur accèdera aux différentes fonctionnalités

    Methods
    -------
    display_info()
        Gère l'affichage fixe des vues
    make_choice():
        permet à l'utilisateur d'intéragir avec le programme en déclarant des inputs
    """  
    def display_info(self):
        with open('graphical_assets/banner.txt', 'r', encoding="utf-8") as asset:
            print(asset.read())
    
    def make_choice(self):
        choosed = QUESTIONS.execute() 
        if choosed == "Se connecter":
            from vue.inscriptionview import Inscription
            return Inscription()
            
        elif choosed == 'Rechercher une annonce':
            from vue.listannonceview import AnnonceListView
            from scrapping.scrap_pv_immo import Scrapping
            from dao.villeDAO import VilleDAO
            from dao.annonceDAO import AnnonceDAO
            from service.rechercheFiltre import RechercheFiltre
            ville = inquirer.text(
                message ="Autour de quelle ville ?",
                completer = VilleDAO().get_all_cities(),
                multicolumn_complete=True
                ).execute()
            scrap = []
            if VilleDAO().get_insee(ville) != None :
                scrap.extend(Scrapping(ville).list_annonce())
            bdd_annonces = AnnonceDAO().get_all()
            bdd_annonces = RechercheFiltre(bdd_annonces).filtre_str(ville, 'city')
            scrap.extend(bdd_annonces)
            if scrap != []:
                Session().ville_scrap = ville
                Session().data = scrap
                return AnnonceListView()
            else :
                return MenuView()

        elif choosed == 'Quitter':
            pass
        import os
        os.system('cls')