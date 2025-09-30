from vue.listannonceview import AnnonceListView
from vue.menuview import MenuView
from vue.abstractview import AbstractView
if __name__ == '__main__':
    import os
    os.system('cls')
    vue = MenuView()
    while vue:
        # Display the info of the view
        vue.display_info()
        # ask user for a choice
        vue = vue.make_choice()
