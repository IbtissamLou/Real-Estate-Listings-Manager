class Singleton(type):
    """Classe singletons qui servira à garantir l'unicité de l'instance qu'elle générera.Ainsi il ne pourra n'y avoir qu'un utilisateur d'enregistré à la fois.

    Args:
        type (_type_)
    """  
    #Stockage des singletons créé
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """_summary_

        Returns:
            cls: _description_
            *args: _description_
            **kwargs: _description_
        """        
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
