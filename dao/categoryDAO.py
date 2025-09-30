from dao.dbconnection import DBConnection
from outil.singleton import Singleton
from business_object.category import Category
import psycopg2

class CategoryDAO():
    """
    Permet d'accéder aux catégories stockées sur la BDD

    Methods:
    --------
    get_all() : list[str]
        retourne une liste des catégories de la base de données
    """
    def get_all(self) -> list[str]:
        sql =   f"SELECT label FROM categorie"

        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(sql)
                res = cursor.fetchall()
        categories = []
        for row in res:
            categories.append(row[0])
        return categories