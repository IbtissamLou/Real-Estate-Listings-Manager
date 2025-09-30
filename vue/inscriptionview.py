from vue.abstractview import AbstractView
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator
from InquirerPy.base.control import Choice
from dao.userDAO import UserDAO
from datetime import date
from pyfiglet import Figlet


from vue.session import Session
from business_object.particulier import Particulier

#Les questions à poser sur l'utilisateur lors de l'inscription
#ASK_id = inquirer.text(message = "id ?")
ASK_nom = inquirer.text(message = 'Nom ?')
ASK_prenom = inquirer.text(message = 'Prénom ?')
ASK_email = inquirer.text(message = 'Renseignez votre adresse email ?')
ASK_password=inquirer.secret(message='Votre mot de passe ?',
        transformer=lambda _: "[hidden]",)


class Inscription(AbstractView):

    def __init__(self):
        self.question = inquirer.select(
                        message = 'Veillez se connecter ou créer un compte pour bénéficier de plus de fonctionnalités'
                        , choices=[
                         Choice('Se connecter')
                        ,Choice('Creer un compte')
                        ,Choice('Quitter')]  )
        
    def display_info(self) : 
        import os
        os.system('cls')
        print(Figlet(font='standard').renderText('Connexion').format('100'))
        
    def make_choice(self):
        choosed = self.question.execute()
        if choosed == 'Creer un compte':
            self.qst = inquirer.select(    
            message = 'veillez préciser votre type'
            , choices=[
                Choice('Particulier'),
                Choice('Professionnel')
            ])
            choose = self.qst.execute()
            if choose == 'Particulier' : 
                type = 1
                prenom = ASK_prenom.execute()
                nom = ASK_nom.execute()
                email = ASK_email.execute()
                passe = ASK_password.execute()
                from werkzeug import security
                password = security.generate_password_hash(passe)
                from datetime import datetime
                date_inscription = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if choose == 'Professionnel' :
                type = 2
                #id = ASK_id.execute()
                #Session().user_id = id
                prenom = ASK_prenom.execute()
                nom = ASK_nom.execute()
                email = ASK_email.execute()
                passe = ASK_password.execute()
                from werkzeug import security
                password = security.generate_password_hash(passe)
                from datetime import datetime
                date_inscription = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            user = Particulier(nom = nom , prenom = prenom, email = email , birth_date = '2000-12-10', zip_code = '123', password=password , type = type , tel = '123' , adresse = 'cc' , date_inscription = date_inscription)
            UserDAO().add_user(user) #Ajouter l'utilisateur dans la base de données
            Session().user_email = email
            Session().user_prenom = prenom
            Session().is_connected = True
            import os
            os.system('cls')
            from vue.menu2view import Menu2View
            return Menu2View()
        if choosed == 'Se connecter':
            email = ASK_email.execute()
            Session().selected_user = UserDAO().find_user_by_email(email)
            if Session().selected_user != None:
                 Session().user_email = email
                 Session().user_prenom = UserDAO().get_prenom_by_email(email)
                 password = ASK_password.execute()
                 pwhash = UserDAO().get_password_by_email(email)
                 from werkzeug import security
                 if  security.check_password_hash(pwhash, password):
                     Session().is_connected = True
                     print("Connexion réussie")
                     import os
                     os.system('cls')
                     from vue.menu2view import Menu2View
                     return Menu2View()
                 else : 
                     print("Mot de passe incorrect")
                     import os
                     os.system('cls')
                     from vue.menuview import MenuView
                     return MenuView()
            else : 
                print("Cet identifiant n'existe pas, veuillez réessayer")
                import os
                os.system('cls')
                from vue.menuview import MenuView
                return MenuView()
        if choosed == 'Quitter':
            import os
            os.system('cls')
            from vue.menuview import MenuView
            return MenuView()
           
    


          
    