import geopy.distance
from geopy.geocoders import Nominatim

class Geolocalisation():


     def distance_villes(self,nom_1,nom_2):
            """Calcule la distance entre 2 villes

            parameters
            ----------
            nom1: str
                premièe ville
            nom2: str
                deuxième ville
            
            returns
            -------
            str"""
            loc = Nominatim(user_agent="GetLoc")
            ville_1 = loc.geocode(nom_1)
            ville_1_coord=(ville_1.latitude,ville_1.longitude)
            ville_2=loc.geocode(nom_2)
            ville_2_coord=(ville_2.latitude,ville_2.longitude)
            distance = geopy.distance.geodesic(ville_1_coord, ville_2_coord).km
            return  "La distance entre " + nom_1 + " et " + nom_2  + " est de " + str(round(distance,2)) + " km. "

# print(Geolocalisation().distance_villes("Bruz","Lyon"))

