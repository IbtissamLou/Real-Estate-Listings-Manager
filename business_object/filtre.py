
class Filtre:
    """
    Instancie un filtre dans le but de faciliter le stockage des
    filtres actifs pour les modifier durant la session ou les
    afficher lors de la recherche.

    Attributes :
    ------------
    label : str
        nom du filtre
    values : list = None
        valeur.s du filtre, par défaut None
    """
    def __init__(self,label : str,values:list = None):
        #Constructeur de la classe
        self.label = label 
        self.values = values 

    def __str__(self):
        if self.label == 'kind':
            return "Catégorie.s : {}".format(self.values[0])
        elif self.label == 'city':
            return "Ville.s : {}".format(self.values[0])
        else :
            return "{} : {} à {}".format(self.label, self.values[0], self.values[1])