from dao.dbconnection import DBConnection
from outil.singleton import Singleton

import csv
from csv import DictReader

import psycopg2

class VilleDAO():
    """
    Permet la gestion de la table des villes et leur code INSEE dans la BDD

    Methods:
    --------
    export(url:str) 
        exporte une liste INSEE sur la BDD à partir d'un fichier
        ne sera utilisé qu'une unique fois
    get_insee(ville:str):str
        retourne le code INSEE associé à une ville dans la BDD
    get_all_cities():dict
        retourne une liste de toutes les villes possibles dans un dictionnaire pour
        suggérer à l'utilisateur les possibilités
    """
    def __init__(self):
        pass

    @staticmethod
    def export(url:str):  
        with open(url, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile) 
            with  DBConnection().connection as connection :
                with connection.cursor() as cur : 
                    sql = "CREATE TABLE Ville(city text, insee text);"
                    cur.execute(sql)
                    for line in reader :
                        insee = str(line["COM"])
                        city = str(line["LIBELLE"])
                        sql = "INSERT INTO Ville(city,insee) VALUES ((%s), (%s));"
                        cur.execute(sql,(city, insee))
    
    @staticmethod
    def get_all_cities() -> dict :
        sql =   "SELECT city FROM Ville"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor :
                cursor.execute(sql)
                res = cursor.fetchall()
        villes = []
        for row in res:
            villes.append(row[0])
        completer = {str(i[0]):None for i in res}
        return completer
    
    @staticmethod
    def get_insee(ville : str) -> str:
        try :
            sql = "SELECT insee FROM Ville Where LOWER((%(ville)s)) = LOWER(city)"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor :
                    cursor.execute(sql, {"ville": ville})
                    return cursor.fetchall()[0][0]
        except :
            return None

#Commande qui aura servit à la création de la table ville
#VilleDAO().export(url='//filer-eleves2\id1927\Downloads\commune2021-csv\commune2021.csv')