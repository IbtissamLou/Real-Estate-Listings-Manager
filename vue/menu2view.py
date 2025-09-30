from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy import prompts
from pyfiglet import Figlet

from vue.abstractview import AbstractView
from vue.session import Session

from dao.wishListDAO import WishListDAO
from dao.userDAO import UserDAO
from dao.historicDAO import HistoricDAO
from vue.historicView import Historic

from service.impexp import ImpExp

qstt = inquirer.select(
                        message = f'Veillez choisir la page'
                        , choices=[
            Choice("Rechercher une annonce")
            ,Choice("Accéder à l'historique")
            ,Choice("Mon compte") #differents profils qui s'affichent selon l'utilisateur
            ,Choice("Accéder à wishlist") 
            ,Choice('Exporter les recherches')
            ,Choice('Quitter')])

class Menu2View(AbstractView):
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
        text = Session().user_prenom
        print(Figlet(font='standard').renderText('Bonjour'+" "+ text).format('100'))
        #with open('graphical_assets/banner.txt', 'r', encoding="utf-8") as asset:
         #   print(asset.read())
    def make_choice(self):
            choix = qstt.execute()
            if choix == "Rechercher une annonce" :
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
                    from scrapping.scrap_pv_immo import Scrapping
                    scrap.extend(Scrapping(ville).list_annonce())
                bdd_annonces = AnnonceDAO().get_all()
                bdd_annonces = RechercheFiltre(bdd_annonces).filtre_str(ville, 'city')
                scrap.extend(bdd_annonces)
                if scrap != []:
                    from vue.listannonceview import AnnonceListView
                    Session().ville_scrap = ville
                    Session().data = scrap
                    return AnnonceListView()
                else :
                    from vue.menu2view import Menu2View
                    return Menu2View()
            elif choix == "Accéder à wishlist" :
                from vue.wishlistview import Wishlist
                return Wishlist()
            elif choix == "Mon compte":
                from vue.profilview import Profilview
                return Profilview()
            elif choix == "Accéder à l'historique":
                return Historic()
                pass
            elif choix == "Exporter les recherches":
                question = inquirer.select(
                            message = f'Que voulez vous faire ?'
                            , choices=[
                            Choice('Exporter votre historique')
                            ,Choice('Exporter votre liste d\'envies')
                            ,Choice('Retour')])
                choosed = question.execute()
                if choosed == 'Exporter votre historique':
                    id = UserDAO().get_id_by_email(Session().user_email)
                    hist = HistoricDAO().list_historic_by_id(id)
                    ASK_path=inquirer.text(message = 'Le chemin ou vous voulez exporter le fichier (Ne pas mettre le double backslash au debut !) ?')
                    ASK_name=inquirer.text(message = 'Le nom que vous voulez donner au fichier ?')
                    path=ASK_path.execute()
                    name=ASK_name.execute()
                    ImpExp(str(path), str(name), '.txt').envoyer_donnees_hist(hist)
                    print('Export effectué ! ')
                    import os
                    os.system('cls')
                    from vue.menu2view import Menu2View
                    return Menu2View()
                if choosed == 'Exporter votre liste d\'envies':
                    id = UserDAO().get_id_by_email(Session().user_email)
                    wishlist = WishListDAO().find_wishlist_by_id_list(id)
                    ASK_path=inquirer.text(message = 'Le chemin ou vous voulez exporter le fichier (Ne pas mettre le double backslash au debut !) ?')
                    ASK_name=inquirer.text(message = 'Le nom que vous voulez donner au fichier ?')
                    path=ASK_path.execute()
                    name=ASK_name.execute()
                    ImpExp(str(path), str(name), '.txt').envoyer_donnees(wishlist)
                    print('Export effectué ! ')
                    import os
                    os.system('cls')
                    from vue.menu2view import Menu2View
                    return Menu2View()
                if choosed == 'Exporter votre liste d\'envies':
                    from vue.menu2view import Menu2View
                    return Menu2View()
            elif choix == "Quitter":
                pass