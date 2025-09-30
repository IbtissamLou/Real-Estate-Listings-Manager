import unittest
from unittest import TestCase

from service.rechercheFiltre import RechercheFiltre
from scrapping.scrap_pv_immo import Scrapping

class TestRecherche(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.scrap = Scrapping('Annecy').list_annonce()

    def test_FiltreCategory(self):
        filtre_cat = RechercheFiltre(self.scrap).filtre_str("Appartement", "kind")
        types= RechercheFiltre(filtre_cat).list_category()
        test = all(x=="Appartement" for x in types)
        self.assertTrue(test)
    
    def test_FiltreVille(self):
        filtre_ville = RechercheFiltre(self.scrap).filtre_str("Seynod (74600)", "city") #Seynod est une ville accolée à Annecy, on s'attend à la voir dans les annonces
        villes = RechercheFiltre(filtre_ville).list_ville()

        test = len(villes) == 1 and villes[0] == 'Seynod (74600)'
        self.assertTrue(test)

    def test_FiltreCatPrix(self):
        filtre_ville = RechercheFiltre(self.scrap).filtres(['kind','price'],[['Appartement'],[0,200000]])
        test1 = all((x.kind=="Appartement" and 0<=int(x.price)<=200000) for x in filtre_ville)
        test2 = all((x.kind=="Appartement" and 0<=int(x.price)<=200000) for x in self.scrap)
        self.assertTrue(test1)
        self.assertFalse(test2)

    def test_id(self):
        filtre_id = RechercheFiltre(self.scrap).filtre_by_id(47)
        self.assertEqual(filtre_id.id_annonce, 47)

if __name__ == '__main__':
    unittest.main()