#import os
#import dotenv
import psycopg2
#from psycopg2.extras import RealDictCursor


class DBConnection():
    """
    Technical class to open only one connection to the DB.
    """
    def __init__(self):
        #dotenv.load_dotenv(override=True)
        # Open the connection. 
        self.__connection =psycopg2.connect(
            host='sgbd-eleves.domensai.ecole',
            port='5432',
            database='id1927',
            user='id1927',
            password='id1927',)

    @property
    def connection(self):
        #if self.__connection.is_connected():
         #       db_Info = self.__connection.get_server_info()
          #      print('Connected to MySQL database', db_Info)
        #else:
         #   print("Error while connected to database")
        return self.__connection
       
        
    