from vue.abstractview import AbstractView
from vue.abstractview import AbstractView
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator
from InquirerPy.base.control import Choice
from dao.wishListDAO import WishListDAO
from pyfiglet import Figlet
from dao.userDAO import UserDAO
from dao.wishListDAO import WishListDAO

from vue.session import Session
from business_object.particulier import Particulier

class Wishlist():
    def __init__(self):
          self.ques = inquirer.select(
                        message = 'Favoris'
                        , choices=[
                        Choice('Supprimer une annonce')
                        ,Choice('Retourner au menu')])

    def display_info(self) :  
        import os
        os.system('cls')
        print(Figlet(font='standard').renderText('Mes Favoris').format('100'))
        email = Session().user_email
        id_user = UserDAO().get_id_by_email(email)
        print(WishListDAO().find_wishlist_by_id(id_user))
    def make_choice(self):
        choosed = self.ques.execute()
        #self.ques.execute() : revenir en arrière 
        if choosed == 'Supprimer une annonce' :
            email = Session().user_email
            id_user = UserDAO().get_id_by_email(email)
            ASK_numero=inquirer.text(message = 'Entrez le numéro de l''annonce')
            id = ASK_numero.execute()
            WishListDAO().delete_favorite(id_user, id)
            import os
            os.system('cls')
            from vue.wishlistview import Wishlist
            return Wishlist()
        if choosed == 'Retourner au menu':
            from vue.menu2view import Menu2View
            return Menu2View()
