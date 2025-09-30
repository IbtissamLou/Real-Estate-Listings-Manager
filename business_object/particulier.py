from datetime import date


class Particulier():
    def __init__(self, nom, prenom, email,  birth_date, zip_code, password, type, tel,  adresse, date_inscription):
            self.nom = nom
            self.prenom = prenom
            self.email = email
            #self.id_user = id_user
            self._tel = tel
            self._password = password
            self._adresse = adresse
            self.zip_code = zip_code
            self.date_inscription = date_inscription
            self.birth_date = birth_date
            self.type = type

#alice = Particulier('ibt', 'lou', 'ibtt', None, None, 'sqd', '1', None, None, None)
#print(alice.id_user)
#bob = Particulier('hjb', None, None, 'birth_date', 'zip_code', 'password', 'type', 'tel', 'adresse', 'date_inscription')
#print(bob.id_user)
#sa =  Particulier('hjb', None, None, 'birth_date', 'zip_code', 'password', 'type', 'tel', 'adresse', 'date_inscription')
#print(sa.id_user)
#ma = Particulier('hjb', None, None, 'birth_date', 'zip_code', 'password', 'type', 'tel', 'adresse', 'date_inscription')
#print(ma.id_user)
#today = date().today()
#d1 = today.strftime("%d/%m/%Y")
#print(d1)