import unittest
from unittest import TestCase
from service.geoloc import Geolocalisation

class TestGeolocalisation(TestCase):
    def test_geolocalisation(self):
        # GIVEN
        distance_hyp="La distance entre Bruz et Metz est de 596.98 km. "
        test_g=Geolocalisation()
        ville1 = 'Bruz'
        ville2 = 'Metz'

        # WHEN
        distance_app = test_g.distance_villes(ville1, ville2)
        # THEN
        self.assertEqual(distance_hyp, distance_app)

if __name__ == '__main__':
    unittest.main()