from business_object.professionnel import Professionnel
from dao.userDAO import UserDAO

class Administrateur(Professionnel):
    def __init__(self, nom, prenom, mail, id_user, tel, mdp,zip_code, adresse, date_inscp, birth_date):
        super().__init__(nom, prenom, mail, id_user, tel, mdp,zip_code, adresse, date_inscp, birth_date)



ad1=Administrateur(nom='Sam',prenom='prenom',mail='mail',id_user=2,tel='tel',zip_code='zip',mdp='mdp',adresse='adresse',date_inscp='date_inscp',birth_date='date_anniv') 
# b=ad1.supprimer_utilisateur(2)
ad2=Administrateur(nom='Sam',prenom='prenom',mail='mail',id_user=2,tel='tel',zip_code='zip',mdp='mdp',adresse='adresse',date_inscp='date_inscp',birth_date='date_anniv') 

# print(b)

