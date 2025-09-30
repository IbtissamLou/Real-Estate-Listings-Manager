from dao.dbconnection import DBConnection
import psycopg2
import json

class Export_data():
    """
    Permet l'export des données scrappés vers la base de données, suit une logique DAO

    Attributes:
    -----------
    data : dict
        dictionnaire résultant du scrapping
    
    Methods
    -------
    __init__ :
        Constructeur de la classe

    exp_data(self, data : dict)
        Permet l'export des données
    """

    def __init__(self, data : dict):
        null = 'Indisponible'
        NaN = 'Indisponible'
        dump = json.dumps(data)
        self.data = json.loads(dump)

    def exp_data(self):
        """
        Permet l'export des données scrappés vers la base de données, suit une logique DAO
        """
        with  DBConnection().connection as connection :
            with connection.cursor() as cur :
                for line in self.data :
                    sql = "INSERT INTO categorie (label) SELECT %(type)s WHERE NOT EXISTS (SELECT * FROM categorie WHERE label = %(type)s);"
                    cur.execute(sql,self.data[line])
                    sql = "INSERT INTO Annonce(surface, city, id_cat, price, room,  source, agency, url_image,title) VALUES (%(surface)s, %(city)s, (SELECT id_cat FROM categorie WHERE label = %(type)s), %(price)s, %(room)s, %(source)s, %(agency)s, %(url_image)s, %(title)s);"
                    cur.execute(sql,self.data[line])
