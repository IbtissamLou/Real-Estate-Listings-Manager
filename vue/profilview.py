from vue.abstractview import AbstractView
from vue.abstractview import AbstractView
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator
from InquirerPy.base.control import Choice
from dao.userDAO import UserDAO
from termcolor import colored
from pyfiglet import Figlet

from dao.annonceDAO import AnnonceDAO
from dao.userDAO import UserDAO

from vue.session import Session
from vue.menu2view import Menu2View
from business_object.particulier import Particulier

import os

ASK_tel=inquirer.text(message = 'Entrez votre numéro de télephone')
ASK_adresse=inquirer.text(message = 'Entrez votre adresse')
ASK_birth_date=inquirer.text(message = 'Entrez votre date de naissance yyyy-mm-dd')
ASK_zip_code=inquirer.text(message = 'Entrez votre code postal')
ASK_new_mdp=inquirer.text(message = 'Entrez votre nouveau mot de passe')
class Profilview(AbstractView):
    def __init__(self):
        self.qst1 = inquirer.select(
                        message = f'Gérer mon compte : '
                        , choices=[
                         Choice('Mes informations') #fonction pour changer les valeurs des atts 
                        ,Choice('Modifier le mot de passe') #fonction pour modifier mot de passe
                        ,Choice('Supprimer son compte')
                        ,Choice('Retourner au menu')])
        self.qst2 = inquirer.select(
                        message = f'Veillez choisir la page'
                        , choices=[
                        #Choice('Mes annonces déposées')
                         Choice('Mes informations')
                        ,Choice('Modifier le mot de passe') 
                        ,Choice('Ajouter un article')
                        ,Choice('Envoyer un message') #fonction pour envoyer un message 
                        ,Choice('Supprimer son compte')
                        ,Choice('Retourner au menu')])
        self.qst3 = inquirer.select(
                        message = f'Veillez choisir la page'
                        , choices=[
                         Choice('Gérer les utilisateurs') #actions sur les utilisateurs
                        ,Choice('Gérer les articles')
                        ,Choice('Ma messagerie')
                        ,Choice('Retourner au menu') ]  )      

    def display_info(self) : 
        import os
        os.system('cls')
        print(colored(Figlet(font='cybermedium').renderText('Mes informations personnelles').format('100'),'red'))
    def make_choice(self):
        email = Session().user_email
        from dao.userDAO import UserDAO
        if UserDAO().get_type_by_email(email) == 1 :
            choosed = self.qst1.execute()
            if choosed == 'Mes informations' :
                tel = ASK_tel.execute()
                adresse = ASK_adresse.execute()
                birth_date = ASK_birth_date.execute()
                zip_code = ASK_zip_code.execute()
                UserDAO().completer_info(email, tel, adresse, birth_date, zip_code)
                import os
                os.system('cls')
                from vue.menu2view import Menu2View
                return Menu2View()
            if choosed == 'Modifier le mot de passe':
                new_mdp = ASK_new_mdp.execute()
                from werkzeug import security
                password = security.generate_password_hash(new_mdp)
                UserDAO().modifier_mdp(email, password)
                import os
                os.system('cls')
                from vue.menu2view import Menu2View
                return Menu2View()
            if choosed == 'Supprimer son compte':
                email = Session().user_email
                UserDAO().delete_user_by_mail(email)
                from vue.menuview import MenuView
                return MenuView()
            if choosed == 'Retourner au menu':
                from vue.menu2view import Menu2View
                return Menu2View()
        from dao.userDAO import UserDAO    
        if UserDAO().get_type_by_email(email) == 2 :
            choosed = self.qst2.execute()
            if choosed == 'Mes informations' :
                tel = ASK_tel.execute()
                adresse = ASK_adresse.execute()
                birth_date = ASK_birth_date.execute()
                zip_code = ASK_zip_code.execute()
                UserDAO().completer_info(email, tel, adresse, birth_date, zip_code)
                import os
                os.system('cls')
                from vue.menu2view import Menu2View
                return Menu2View()
            if choosed == 'Modifier le mot de passe':
                new_mdp = ASK_new_mdp.execute()
                from werkzeug import security
                password = security.generate_password_hash(new_mdp)
                UserDAO().modifier_mdp(email, password)
                import os
                os.system('cls')
                from vue.menu2view import Menu2View
                return Menu2View()
            if choosed == 'Ajouter un article':
                ASK_city=inquirer.text(message = 'Entrez la ville')
                ASK_url_image=inquirer.text(message = 'Entrez l\'url de l\'image')
                ASK_source=inquirer.text(message = 'Entrez la source')
                ASK_price=inquirer.text(message = 'Entrez le prix')
                ASK_kind=inquirer.text(message = 'Entrez le type de bien')
                ASK_surface=inquirer.text(message = 'Entrez la surface')
                ASK_room=inquirer.text(message = 'Entrez le nombre de pièce')
                ASK_agency=inquirer.text(message = 'Entrez l\'agence')
                ASK_title=inquirer.text(message = 'Entrez le titre')
                ASK_description=inquirer.text(message = 'Entrez la description')
                city = ASK_city.execute()
                url_image = ASK_url_image.execute()
                source = ASK_source.execute()
                price = ASK_price.execute()
                kind = ASK_kind.execute()
                surface = ASK_surface.execute()
                room = ASK_room.execute()
                agency = ASK_agency.execute()
                description = ASK_description.execute()
                title = ASK_title.execute()
                AnnonceDAO().post_annonce(city, url_image, source, price, kind, surface, room, agency, description, title, sell=True)
                import os
                os.system('cls')
                from vue.menu2view import Menu2View
                return Menu2View()
            if choosed == 'Supprimer son compte':
                email = Session().user_email
                UserDAO().delete_user_by_mail(email)
                from vue.menuview import MenuView
                return MenuView()
            if choosed == 'Envoyer un message':
                email = Session().user_email
                id_user = UserDAO().get_id_by_email(email)
                ASK_message = inquirer.text(message = 'Taper votre message :')
                message = ASK_message.execute()
                from dao.MessageDao import MessageDao
                MessageDao().add_message(message,id_user)
                import os
                os.system('cls')
                from vue.menu2view import Menu2View
                return Menu2View()
            if choosed == 'Retourner au menu':
                from vue.menu2view import Menu2View
                return Menu2View()

        if UserDAO().get_type_by_email(email) == 3 :
            choosed = self.qst3.execute()
            if choosed == 'Gérer les utilisateurs':
                question = inquirer.select(
                            message = f'Que voulez vous faire ?'
                            , choices=[
                            Choice('Ajouter un utilisateur')
                            ,Choice('Supprimer un utilisateur')])
                choosedbis = question.execute()
                if choosedbis == 'Ajouter un utilisateur':
                    ASK_nom=inquirer.text(message = 'Entrez le nom')
                    ASK_prenom=inquirer.text(message = 'Entrez le prénom')
                    ASK_emailbis=inquirer.text(message = 'Entrez le mail')
                    ASK_type=inquirer.text(message = 'Entrez le type (1:Particulier, 2:Professionnel)')
                    ASK_password=inquirer.secret(message = 'Entrez le mot de passe',
                    transformer=lambda _: "[hidden]",)
                    ASK_telbis=inquirer.text(message = 'Entrez votre numéro de télephone')
                    ASK_adressebis=inquirer.text(message = 'Entrez l\'adresse')
                    ASK_birth_datebis=inquirer.text(message = 'Entrez la date de naissance')
                    ASK_zip_codebis=inquirer.text(message = 'Entrez le code postal')
                    nom = ASK_nom.execute()
                    prenom = ASK_prenom.execute()
                    emailbis = ASK_emailbis.execute()
                    typebis = ASK_type.execute()
                    passe = ASK_password.execute()
                    from werkzeug import security
                    password = security.generate_password_hash(passe)
                    telbis = ASK_telbis.execute()
                    adressebis = ASK_adressebis.execute()
                    birth_date_bis = ASK_birth_datebis.execute()
                    zip_codebis = ASK_zip_codebis.execute()
                    user = Particulier(nom, prenom, emailbis, birth_date_bis, zip_codebis, password, typebis, telbis, adressebis, date_inscription=None)
                    UserDAO().add_user(user)
                    import os
                    os.system('cls')
                    from vue.menu2view import Menu2View
                    return Menu2View()
                if choosedbis == 'Supprimer un utilisateur':
                    ASK_utilisateur=inquirer.text(message = 'Quel son email ?')
                    user_a_supprimer = ASK_utilisateur.execute()
                    UserDAO().delete_user_by_mail(user_a_supprimer)
                    import os
                    os.system('cls')
                    from vue.menu2view import Menu2View
                    return Menu2View()
            if choosed == 'Gérer les articles':
                question = inquirer.select(
                            message = f'Que voulez vous faire ?'
                            , choices=[
                            Choice('Ajouter un article')
                            ,Choice('Supprimer un article')])
                choosedbis = question.execute()
                if choosedbis == 'Ajouter un article':
                    ASK_city=inquirer.text(message = 'Entrez la ville')
                    ASK_url_image=inquirer.text(message = 'Entrez l\'url de l\'image')
                    ASK_source=inquirer.text(message = 'Entrez la source')
                    ASK_price=inquirer.text(message = 'Entrez le prix')
                    ASK_kind=inquirer.text(message = 'Entrez le type de bien')
                    ASK_surface=inquirer.text(message = 'Entrez la surface')
                    ASK_room=inquirer.text(message = 'Entrez le nombre de pièce')
                    ASK_agency=inquirer.text(message = 'Entrez l\'agence')
                    ASK_title=inquirer.text(message = 'Entrez le titre')
                    ASK_description=inquirer.text(message = 'Entrez la description')
                    city = ASK_city.execute()
                    url_image = ASK_url_image.execute()
                    source = ASK_source.execute()
                    price = ASK_price.execute()
                    kind = ASK_kind.execute()
                    surface = ASK_surface.execute()
                    room = ASK_room.execute()
                    agency = ASK_agency.execute()
                    description = ASK_description.execute()
                    title = ASK_title.execute()
                    AnnonceDAO().post_annonce(city, url_image, source, price, kind, surface, room, agency, description, title)
                    import os
                    os.system('cls')
                    from vue.menu2view import Menu2View
                    return Menu2View()
                if choosedbis == 'Supprimer un article':
                    ASK_id = inquirer.text(message = 'Quel id d\'annonce supprimer')
                    id_a_supprimer = ASK_id.execute()
                    AnnonceDAO().delete_annonce(id_a_supprimer)
                    import os
                    os.system('cls')
                    from vue.menu2view import Menu2View
                    return Menu2View()
            if choosed == 'Ma messagerie' :
                from vue.vuemessage import Messagevue
                return Messagevue()
            if choosed == 'Retourner au menu':
                from vue.menu2view import Menu2View
                return Menu2View()




        


        


    

