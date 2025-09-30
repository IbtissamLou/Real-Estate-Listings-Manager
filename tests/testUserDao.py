from unittest import TestCase
import unittest

from dao.userDAO import UserDAO
from business_object.particulier import Particulier

class TestUserDAO(TestCase):
  @classmethod
  def setup(self):
    pass

  def test_id(self):
    id = UserDAO().get_id_by_email("et@com")
    self.assertEqual(id, 22)

  def test_prenom(self):
    prenom = UserDAO().get_prenom_by_email("et@com")
    self.assertEqual(prenom, 'Elysabeth')

  def test_prenom_id(self):
    prenom_id = UserDAO().get_prenom_by_id(22)
    self.assertEqual(prenom_id, 'Elysabeth')

  def test_add_get_name_delete(self):
    Dilane=Particulier(nom='Dilane', prenom='Keubou',email= 'emailpourtest', tel=1505050514,password= 'Tentative', adresse='adresse', zip_code='35170',date_inscription= '2020-01-01', birth_date="2020-01-01", type=1)
    UserDAO().add_user(Dilane)
    test1 = UserDAO().get_prenom_by_email("emailpourtest")
    UserDAO().delete_user_by_mail("emailpourtest")
    self.assertTrue(test1)

if __name__ == '__main__':
    unittest.main()