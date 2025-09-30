from business_object.particulier import Particulier

class Professionnel(Particulier):
    def __init__(self, nom, prenom, mail, id_user, tel, mdp, adresse,zip_code, date_inscp, birth_date):
        super().__init__(nom, prenom, mail, id_user, tel, mdp, adresse, zip_code, date_inscp, birth_date)
        