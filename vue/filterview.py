from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator
from InquirerPy.validator import NumberValidator

from vue.abstractview import AbstractView
from vue.session import Session

from dao.categoryDAO import CategoryDAO
from dao.annonceDAO import AnnonceDAO
from dao.villeDAO import VilleDAO

from service.rechercheFiltre import RechercheFiltre
from scrapping.scrap_pv_immo import Scrapping
from business_object.filtre import Filtre

class FilterView(AbstractView):
    """
    Implémente la vue sur les pour sélectionner les filtres
    """

    def display_info(self):
        #Informations fixes sur la page
        with open('graphical_assets/banner.txt', 'r', encoding="utf-8") as asset:
            print(asset.read())
        if Session().filtres_actifs != []: 
            print ("--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.")
            for i in Session().filtres_actifs :
                print(i)
            print("--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.")
    
    def make_choice(self):
        #Choix sur la page
        action = inquirer.select(
                message = f'Par quel critère souhaitez-vous filtrer vos annonces ?'
                , choices=[
                Choice(value='kind', name='Type de bien')
                ,Choice(value='price', name='Prix')
                ,Choice(value='city', name='Localité')
                ,Choice(value='surface', name='Surface')
                ,Choice(value='room', name='Nombre de pièces')
                ,Choice('Réinitialiser les filtres')
                ,Choice('Appliquer les filtres')
                ]).execute()

        if action == 'kind':
            cat = inquirer.select(
                message='Quel type de bien ?',
                choices = RechercheFiltre(Session().data).list_category()
            ).execute()
            Session().data = RechercheFiltre(Session().data).filtre_str(cat,action)
            Session().filtres_actifs.append(Filtre(action,[cat]))
            return FilterView()
        
        if action == 'city':
            ville = inquirer.select(
                message='Localité du bien ?',
                choices = RechercheFiltre(Session().data).list_ville()
            ).execute()
            Session().data = RechercheFiltre(Session().data).filtre_str(ville, action)
            Session().filtres_actifs.append(Filtre(action,[ville]))
            return FilterView()

        elif action in ['price', 'room', 'surface']:
            min = inquirer.number(
                message = f'{action} minimum:'.format(action),
                min_allowed= 0,
                validate = EmptyInputValidator() and NumberValidator()
            ).execute()
            max = inquirer.number(
                message = f'{action} maximum:'.format(action),
                validate = EmptyInputValidator() and NumberValidator()
            ).execute()
            Session().data = RechercheFiltre(Session().data).filtres([action], [[float(min),float(max)]])
            Session().filtres_actifs.append(Filtre(action,[min,max]))
            return FilterView()

        elif action == 'Réinitialiser les filtres':
            scrap = []
            ville = Session().ville_scrap
            if VilleDAO().get_insee(ville) != None :
                scrap.extend(Scrapping(ville).list_annonce())
                bdd_annonces = AnnonceDAO().get_all()
            bdd_annonces = RechercheFiltre(bdd_annonces).filtre_str(ville, 'city')
            scrap.extend(bdd_annonces)
            from vue.listannonceview import AnnonceListView
            Session().filtres_actifs = []
            Session().data = scrap
            return FilterView()

        else:
            from vue.listannonceview import AnnonceListView
            return AnnonceListView()
