import mysql.connector

#connection = {
 #    'host' : "sgbd-eleves.domensai.ecole",
  #   'database' : "id1927",
   #  'user' : "id1927",
    # 'password' : "id1927",
#}
#class DBConnection():
 #   def __init__(self):
  #      pass 
   # def connection(self):
conn = mysql.connector.connect(host = "sgbd-eleves.domensai.ecole",
port='5432',
database = "id1927",
user = "id1927",
password = "id1927") 
cursor = conn.cursor()
request ="INSERT INTO Historic(id_historic,id_user,id_annonce) VALUES ('20','18','17');"\
            "RETURNING id_historic;"
cursor.execute(request)
conn.commit()




