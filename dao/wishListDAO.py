
from service.wishList import WishList 
from dao.dbconnection import DBConnection
from outil.singleton import Singleton
from business_object.annonce import Annonce
#LEFT JOIN utilisateur ON utilisateur.id_user = wishlist.id_user
class WishListDAO(metaclass = Singleton):

    def find_wishlist_by_id(self, id_user) :
        connection = DBConnection().connection 
        with connection.cursor() as cursor :
            request = f"\nSELECT DISTINCT * FROM annonce LEFT JOIN wishlist ON annonce.id_annonce = wishlist.id_annonce "\
                      f" WHERE id_user=%(id_user)s"
            cursor.execute(request, {"id_user": id_user})
            res = cursor.fetchall()
            for i in range(len(res)):
                print("Annonce n°{} : {}".format(res[i][0], res[i][9])+" "+"de {}m² avec {} pièce.s situé à {} ".format(res[i][6],res[i][7],res[i][1])+
                "son prix est de {}€".format(res[i][5])+" se renseigner avec l\'agence {}".format(res[i][8])+" tu peux retrouver l\'image du bien ici : {}".format(res[i][2])+" et le lien du bien là : {}".format(res[i][3])+"\n")

    def find_wishlist_by_id_list(self, id_user):
        connection = DBConnection().connection 
        with connection.cursor() as cursor :
            request = f"\nSELECT DISTINCT * FROM annonce LEFT JOIN wishlist ON annonce.id_annonce = wishlist.id_annonce "\
                      f" WHERE id_user=%(id_user)s"
            cursor.execute(request, {"id_user": id_user})
            res = cursor.fetchall()
            wish = []
            for i in range(len(res)):
                annonce = Annonce(id_annonce=res[i][0],city=res[i][1],url_image=res[i][2],source=res[i][3],price=res[i][5],kind=res[i][4],surface=res[i][6],room=res[i][7],agency=res[i][8]
                ,description=res[i][10],title=res[i][9])
                wish.append(annonce)
            return wish

    def add_favorite(self, user_id, annonce_id):
        request = 'INSERT INTO wishlist (id_user, id_annonce) VALUES (%(id_u)s,%(id_a)s)'
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(request, {'id_u': user_id, 'id_a': annonce_id})


    def delete_favorite(self, id_user, id_annonce):
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM wishlist WHERE id_user=%(id_user)s AND id_annonce=%(id_annonce)s", {"id_user":id_user, "id_annonce":id_annonce})
            connection.commit()
            cursor.close()
    