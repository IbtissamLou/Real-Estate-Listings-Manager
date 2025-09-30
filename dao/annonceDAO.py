from dao.dbconnection import DBConnection
from outil.singleton import Singleton
from business_object.annonce import Annonce
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np

class AnnonceDAO(metaclass=Singleton):
    """
    Permet d'accéder aux annonces stockées sur la BDD en respectant les exigences CRUD

    Methods:
    --------
    get_all() : list[Annonce]
        retourne les annonces de la base de données
    find_annonce_by_id(id) : Annonce
        retourne une annonce à partir de son id
    post_annonce(city,url_image,source,price,kind,surface,room,agency,description,title,sell=False): id
        permet d'ajouter une annonce dans la BDD, l'attribut sell si True signifie que l'annonce est public et donc le bien à vendre. Retourne l'id de l'annonce si elle existe
        déjà ou bien l'id de l'annonce créée.
    delete_annonce(id):
        Retire une annonce de la BDD à partir de son id
    """
    @staticmethod
    def get_all() -> List[Annonce]:
        sql =   f"SELECT * FROM Annonce LEFT JOIN categorie ON Annonce.id_cat = categorie.id_cat WHERE sell = 'TRUE'"

        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(sql)
                res = cursor.fetchall()

        annonces = []
        for row in res:
            annonce = Annonce(
                id_annonce = row[0]
                , city=row[1]
                , url_image=row[2]
                , source=row[3]
                , price=row[5]
                , surface=row[6]
                , room=row[7]
                , agency=row[8]
                , title=row[9]
                , kind=row[13]
                ,description=row[10])
            annonces.append(annonce)
        return annonces

    @staticmethod
    def find_annonce_by_id() -> Annonce:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor :
                    cursor.execute("SELECT * FROM Annonce LEFT JOIN categorie ON Annonce.id_cat = categorie.id_cat WHERE id_annonce=%(id)s", {"id": id})
                    res = cursor.fetchone()
                annonce = Annonce(
                    id_annonce = res[0]
                    , city=res[1]
                    , url_image=res[2]
                    , source=res[3]
                    , price=res[5]
                    , surface=res[6]
                    , room=res[7]
                    , agency=res[8]
                    , title = res[9]
                    , kind=res[13])
            return annonce
    
    @staticmethod
    def post_annonce(city,url_image,source,price,kind,surface,room,agency,description,title,sell=False):
        NaN = 'Indisponible'
        connection = DBConnection().connection
        dic_attr=  {"city" :city
                                , "url_image" :url_image
                                , "source" :source
                                , "price" :price
                                ,"kind" :kind
                                , "surface" :surface
                                , "room" :room
                                , "agency" :agency
                                , "description" :description
                                , "title":title
                                ,"sell":sell
                }
        try :
            sql_test_exist = "SELECT id_annonce from Annonce Where city=%(city)s AND url_image=%(url_image)s AND source=%(source)s AND price=%(price)s AND  surface=%(surface)s AND room=%(room)s AND agency=%(agency)s AND description =%(description)s AND title=%(title)s;"
            with connection.cursor() as cursor:
                cursor.execute(sql_test_exist,dic_attr)
                res = cursor.fetchall()
                return(res[0][0])
        except IndexError:
            if sell==False:
                sql = "INSERT INTO Annonce(city,url_image, source,id_cat,price,surface,room,agency,description,title) VALUES (%(city)s, %(url_image)s, %(source)s,(SELECT id_cat FROM categorie WHERE label = %(kind)s), %(price)s,  %(surface)s, %(room)s, %(agency)s,%(description)s, %(title)s)"
            else:
                sql = "INSERT INTO Annonce(city,url_image, source,id_cat,price,surface,room,agency,description,title,sell) VALUES (%(city)s, %(url_image)s, %(source)s,(SELECT id_cat FROM categorie WHERE label = %(kind)s), %(price)s,  %(surface)s, %(room)s, %(agency)s,%(description)s, %(title)s,%(sell)s)"

            sql2 = "INSERT INTO categorie (label) SELECT %(kind)s WHERE NOT EXISTS (SELECT * FROM categorie WHERE label = %(kind)s);"
            with connection.cursor() as cursor:
                cursor.execute(sql2,{"kind":kind})
                cursor.execute(sql,dic_attr)
                connection.commit()
                cursor.close()
            sql =   "SELECT MAX(id_annonce) FROM Annonce"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor :
                    cursor.execute(sql)
                    res = cursor.fetchall()
            sql =   "SELECT MAX(id_annonce) FROM Annonce"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor :
                    cursor.execute(sql)
                    res = cursor.fetchall()
            return res[0][0]
            

    @staticmethod
    def delete_annonce(id):
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM wishlist WHERE id_annonce=%(id)s ;DELETE FROM historic WHERE id_annonce=%(id)s ;DELETE FROM annonce WHERE id_annonce=%(id)s;", {"id": id})
            connection.commit()
            cursor.close()
