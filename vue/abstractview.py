from abc import ABC, abstractmethod

class AbstractView(ABC):
    """
    Classe abstraite formatant les vues filles

    Methods
    -------
    display_info()
        Gère l'affichage fixe des vues
    make_choice():
        permet à l'utilisateur d'intéragir avec le programme en déclarant des inputs
    """    
    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def make_choice(self):
        pass