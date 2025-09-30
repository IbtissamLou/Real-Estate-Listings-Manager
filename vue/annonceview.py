from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from vue.abstractview import AbstractView
from vue.session import Session
from dao.userDAO import UserDAO
from dao.annonceDAO import AnnonceDAO
from business_object.annonce import Annonce
from dao.wishListDAO import WishListDAO

from service.rechercheFiltre import RechercheFiltre

if Session().user_email is not None:
    CHOIX = inquirer.select(message = f'Voici l\'annonce qui t`\'intéresse'
                , choices=[
                Choice('L\'exporter')
                ,Choice('La géolocaliser')
                ,Choice('Retourner aux annonces')])
else :
    CHOIX = inquirer.select(message = f'Voici l\'annonce qui t`\'intéresse'
                , choices=[
                Choice('L\'ajouter à ma liste d\'envies')
                ,Choice('L\'exporter')
                ,Choice('La géolocaliser')
                ,Choice('Retourner aux annonces')])
    
ASK_city = inquirer.text(message = 'La ville ou vous vous trouvez ?')
ASK_path=inquirer.text(message = 'Le chemin ou vous voulez exporter le fichier (Ne pas mettre le double backslash au debut !) ?')
ASK_name=inquirer.text(message = 'Le nom que vous voulez donner au fichier ?')

class AnnonceView(AbstractView):
    def __init__(self, id_annonce):
        self.id_annonce = int(id_annonce)
        self.annonce = RechercheFiltre(Session().data).filtre_by_id(int(self.id_annonce))
    
    def display_info(self):
        with open('graphical_assets/banner.txt', 'r', encoding="utf-8") as asset:
            print(asset.read())
        if self.annonce.agency != 'Indisponible':
            print("Annonce n°{} : {}]".format(self.annonce.id_annonce, self.annonce.title)+"\n")
            print("Super {} de {}m² avec {} pièce.s situé à {}\n\n{}\n ".format(self.annonce.kind,self.annonce.surface,self.annonce.room,self.annonce.city, self.annonce.description)+"\n")
            print("Son prix est de {}€".format(self.annonce.price)+"\n")
            print("Se renseigner avec l\'agence {}".format(self.annonce.agency)+"\n")
            print("Tu peux retrouver l\'image du bien ici : {}".format(self.annonce.url_image)+"\n")
            print("Et le lien du bien là : {}".format(self.annonce.source)+"\n")
        else:
            print("Annonce n°{}".format(self.annonce.id_annonce)+"\n")
            print("Super {} de {}m² avec {} pièce.s situé à {} ".format(self.annonce.kind,self.annonce.surface,self.annonce.room,self.annonce.city)+"\n")
            print("Son prix est de {}€".format(self.annonce.price)+"\n")
            print("Tu peux retrouver l\'image du bien ici : {}".format(self.annonce.url_image)+"\n")
            print("Et le lien du bien là : {}".format(self.annonce.source)+"\n")
        
    def make_choice(self):
        choosed = CHOIX.execute()
        if choosed == 'L\'ajouter à ma liste d\'envies':
            id_user = UserDAO().get_id_by_email(Session().user_email)
            id_annonce = Session().id_annonce
            id_wish = AnnonceDAO().post_annonce(self.annonce.city, self.annonce.url_image, self.annonce.source, self.annonce.price, self.annonce.kind, self.annonce.surface, self.annonce.room, self.annonce.agency, self.annonce.description, self.annonce.title)
            WishListDAO().add_favorite(id_user, id_wish)
            import os
            os.system('cls')
            from vue.menu2view import Menu2View  #revenir au menu 
            return Menu2View()
        elif choosed == 'L\'exporter':
            path=ASK_path.execute()
            name=ASK_name.execute()
            from service.impexp import ImpExp
            ImpExp(str(path), str(name), '.json').envoyer_donnees( [self.annonce] )
            from vue.listannonceview import AnnonceListView
            print('Export effectué ! ')
            import os
            os.system('cls')
            return AnnonceListView()
        
        elif choosed == 'La géolocaliser':
            ville = ASK_city.execute()
            id_annonce = Session().id_annonce
            ville_annonce=self.annonce.city.split(' ', 1)[0]
            from service.geoloc import Geolocalisation
            geoloc=Geolocalisation().distance_villes(str(ville), str(ville_annonce))
            print(geoloc)
            CHOIX2 = inquirer.select(message = f'Voici la géolocalisation qui t`\'intéresse'
                , choices=[Choice('Retourner à l\'annonce')])
            choisi = CHOIX2.execute()
            if choisi == 'Retourner à l\'annonce':
                return AnnonceView(id_annonce)

        elif choosed == 'Retourner aux annonces': #Comment revenir
            from vue.listannonceview import AnnonceListView
            return AnnonceListView()