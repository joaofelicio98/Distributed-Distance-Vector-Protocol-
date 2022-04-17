#mySQL root pass = password
# DB name -> my_DB
# user to insert on tables: user: joao | pass: password
# table name ->
import mysql.connector as connector
from datetime import datetime

config = {
    "user":"joao",
    "password":"password",
    "port":"3306",
    "host":"localhost",
    "database":"my_DB"
}

db = connector.connect(**config)
mycursor = db.cursor()

#now = datetime.now()
#current_time = now.strftime("%H:%M:%S")
#print ("current_time = ",current_time)

#mycursor.execute("CREATE TABLE stats_table (topo VARCHAR(50), try INT NOT NULL, seq_no INT NOT NULL, node VARCHAR(10), converge_time TIME, count INT NOT NULL, valid BOOLEAN, ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY)")

#topo = 'test'
#Try = 1
#seq_no = 1
#node = 's1'
#converge_time = current_time
#count = 2
#valid = False

#mycursor.execute("INSERT INTO stats_table (topo, try, seq_no, node, converge_time, count, valid) VALUES (%s,%s,%s,%s,%s,%s,%s)",(topo, Try, seq_no, node, converge_time, count, valid))
#db.commit()

#mycursor.execute("SELECT * FROM stats_table")
#for x in mycursor:
#    print(x[4])


db.close()
