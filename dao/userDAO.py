from cgitb import reset
import psycopg2
from business_object.particulier import Particulier
from dao.dbconnection import DBConnection
from outil.singleton import Singleton
from psycopg2.extras import RealDictCursor

class UserDAO(): 
    """
    Permet d'accéder aux utilisateurs stockées sur la BDD en respectant les exigences CRUD

    Methods:
    --------
    add_user(user)
        ajoute un utilisateur dans la BDD 
    find_all_user(limit: int = 50, offset: int = 0)
        retourne les 50 premiers utilisateurs de la BDD
    find_user_by_id(id)
        retourne les informations de l'utilisateur avec un id donné
    get_type_by_id(id)
        retourne le type (0: administrateur, 1: particulier, 2: professionnel) de l'utilisateur 
    delete_user(user)
        supprime un utilisateur de la BDD
    change_type(user)
        modifie le type de l'utilisateur (seulement professionnel en particulier et particulier en professionnel)
    """

    def add_user(self, user) -> bool:
        request = "INSERT INTO utilisateur ( nom, prenom, email, birth_date, zip_code, password, type,tel,adresse,date_inscription ) VALUES (%(nom)s,%(prenom)s,%(email)s,%(birth_date)s,\
        %(zip_code)s,%(password)s,%(type)s,%(tel)s,%(adresse)s,%(date_inscr)s)"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(request,{ "nom" :user.nom , "prenom":user.prenom
                                  , "email":user.email
                                  , "birth_date":user.birth_date
                                  , "zip_code":user.zip_code
                                  , "password":user._password
                                  , "type": user.type
                                  , "tel":user._tel
                                  , "adresse":user._adresse
                                  , "date_inscr":user.date_inscription
                })
          

    def find_all_user(self, limit: int = 50, offset: int = 0) -> list[Particulier]: #a enlevé 
        sql = f"SELECT * FROM utilisateur LIMIT {max(limit, 0)} OFFSET {max(offset, 0)}"
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        return res
        
    def find_user_by_id(self, id) -> Particulier:
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM utilisateur WHERE id_user=%(id)s", {"id": id})
            res = cursor.fetchone()
            return res

    def get_type_by_email(self,email) -> int:
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT type FROM utilisateur WHERE email=%(email)s", {"email": email})
            res = cursor.fetchone()
            return res[0]

    def delete_user_by_mail(self, email):
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM utilisateur WHERE email=%(email)s", {"email": email})
            connection.commit()
            cursor.close()

    def find_user_by_email(self,email) -> Particulier : 
        connection = DBConnection().connection
        with connection.cursor() as cursor:   
            cursor.execute('SELECT * FROM utilisateur WHERE email=%(email)s',{"email": email})
            res = cursor.fetchone()
            return res
        


    def update_user(self,email,birth_date,zip_code,tel,adresse,date_inscription):
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            sql = "INSERT INTO utilisateur(birth_date,zip_code,tel,adresse,date_inscription) VALUES (%(birth_date)s,\
           %(zip_code)s,%(tel)s,%(adresse)s,%(date_inscription)s) WHERE email=%(email)s"   
            cursor.execute(sql, {"email" : email
                                ,"birth_date": birth_date
                                ,"zip_code":zip_code   
                                 , "tel": tel
                                 , "adresse": adresse
                                 , "date_inscription": date_inscription})

    def get_id_by_email(self,email) : 
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_user FROM utilisateur WHERE email=%(email)s", {"email": email})
            res = cursor.fetchone()
            return res[0]            

    def get_password_by_email(self,email) : 
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM utilisateur WHERE email=%(email)s", {"email": email})
            res = cursor.fetchone()
            return res[0]
    
    def get_prenom_by_email(self,email):
         connection = DBConnection().connection
         with connection.cursor() as cursor:
            cursor.execute("SELECT prenom FROM utilisateur WHERE email=%(email)s", {"email": email})
            res = cursor.fetchone()
            return res[0]
    
    def get_prenom_by_id(self,id_user):
         connection = DBConnection().connection
         with connection.cursor() as cursor:
            cursor.execute("SELECT prenom FROM utilisateur WHERE id_user=%(id_user)s", {"id_user": id_user})
            res = cursor.fetchone()
            return res[0]



    def change_type(self,user): #enlever 
        if UserDAO().get_type_by_id(user._id_user) == 1:
            new_type = 2
        else:
            new_type = 1
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute("UPDATE utilisateur SET type=%(type)s WHERE id_user=%(id)s", {"id":user._id_user,"type":new_type})
            connection.commit()
            cursor.close()

    def completer_info(self,email, tel, adresse, birth_date, zip_code):
        request = "UPDATE utilisateur SET tel = %(tel)s, adresse=%(adresse)s, birth_date = %(birth_date)s,zip_code=%(zip_code)s\
           WHERE email=%(email)s"
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute(request,{"email":email,"birth_date":birth_date,"zip_code":zip_code,"tel":tel,"adresse":adresse})
            connection.commit()
            cursor.close()
        
    def modifier_mdp(self, email, new_mdp):
        request = "UPDATE utilisateur SET password=%(new_mdp)s WHERE email=%(email)s"
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute(request,{"new_mdp":new_mdp,"email":email})
            connection.commit()
            cursor.close() 

