from dao.dbconnection import DBConnection
from outil.singleton import Singleton
from business_object.annonce import Annonce
from typing import List
from service.historic import Historic

class HistoricDAO():
    #def create_historic(self):
     #   request = "CREATE TABLE Historic (id_historic INT PRIMARY KEY , id_user INT , id_recherche INT , date DATE);"
      #  with DBConnection().connection as conn :
       #     with conn.cursor() as cursor :
        #     cursor.execute(request)
         #    res = cursor.fetchone()
        #return res

    def add_historic(self, id_user, id_annonce, date_recherche) :
        request ="INSERT INTO historic(id_annonce,id_user,date_recherche) VALUES (%(id_annonce)s,%(id_user)s,%(date_recherche)s);"
        with DBConnection().connection as conn :
            with conn.cursor() as cursor :
                cursor.execute(request,{ 'id_annonce': id_annonce,'id_user': id_user, 'date_recherche': date_recherche})

    def find_historic_by_id(self, id_user) :
        connection = DBConnection().connection 
        with connection.cursor() as cursor :
            request = f"\nSELECT DISTINCT * FROM annonce LEFT JOIN historic ON annonce.id_annonce = historic.id_annonce "\
                      f" WHERE id_user=%(id_user)s"
            cursor.execute(request, {"id_user": id_user})
            res = cursor.fetchall()
            for i in range(len(res)):
                print("{} : Annonce n°{} : {}".format(res[i][14], res[i][0], res[i][9])+" "+"de {}m² avec {} pièce.s situé à {} ".format(res[i][6],res[i][7],res[i][1])+
                "son prix est de {}€".format(res[i][5])+" se renseigner avec l\'agence {}".format(res[i][8])+" tu peux retrouver l\'image du bien ici : {}".format(res[i][2])+" et le lien du bien là : {}".format(res[i][3])+"\n")

    def list_historic_by_id(self, id_user) :
        connection = DBConnection().connection 
        with connection.cursor() as cursor :
            request = f"\nSELECT DISTINCT * FROM annonce LEFT JOIN historic ON annonce.id_annonce = historic.id_annonce "\
                      f" WHERE id_user=%(id_user)s"
            cursor.execute(request, {"id_user": id_user})
            res = cursor.fetchall()
            liste = []
            for i in range(len(res)):
                annonce = "{} : Annonce n°{} : {}".format(res[i][14], res[i][0], res[i][9])+" "+"de {}m² avec {} pièce.s situé à {} ".format(res[i][6],res[i][7],res[i][1])+\
                "son prix est de {}€".format(res[i][5])+" se renseigner avec l\'agence {}".format(res[i][8])+" tu peux retrouver l\'image du bien ici : {}".format(res[i][2])+" et le lien du bien là : {}".format(res[i][3])
                liste.append(annonce)
            return liste




