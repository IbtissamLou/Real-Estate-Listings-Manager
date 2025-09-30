from vue.abstractview import AbstractView
from vue.abstractview import AbstractView
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator
from InquirerPy.base.control import Choice
from pyfiglet import Figlet
from dao.userDAO import UserDAO
from dao.historicDAO import HistoricDAO

from vue.session import Session
from business_object.particulier import Particulier

class Historic():
    def __init__(self):
          self.ques = inquirer.select(
                        message = 'Historique'
                        , choices=[Choice('Retourner au menu')])

    def display_info(self) :  
        import os
        os.system('cls')
        print(Figlet(font='standard').renderText('Mon historique').format('100'))
        email = Session().user_email
        id_user = UserDAO().get_id_by_email(email)
        print(HistoricDAO().find_historic_by_id(id_user))
    def make_choice(self):
        choosed = self.ques.execute()
        if choosed == 'Retourner au menu':
            from vue.menu2view import Menu2View
            return Menu2View()
