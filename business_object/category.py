class Category():
    """
    Instancie une catégorie

    Attributes :
    ------------
    id_cat : int
        id de la catégorie permettant de l'identifier et lier les tables
    label : str
        nom de la catégorie
    """
    def __init__(self,id_cat:int, label:str):
        self.id_cat = id_cat
        self.label = label
    
    def __str__(self) -> str:
        return self.label