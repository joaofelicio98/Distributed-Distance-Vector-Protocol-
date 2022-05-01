import mysql.connector as connector
from datetime import datetime

class DB_API():

    def __init__(self, config):
    #    self.config = {
    #        "user":"joao",
    #        "password":"password",
    #        "port":"3306",
    #        #"host":"localhost",
    #        "host":"192.168.1.158",
    #        "database":"my_DB"
    #    }

        self.config = config
        self.db = connector.connect(**self.config)
        self.mycursor = self.db.cursor()

    def insert_entries(self, **kwargs):
        if len(kwargs) == 7:
            topo = kwargs['topo']
            Try = kwargs['Try']
            seq_no = kwargs['seq_no']
            node = kwargs['node']
            converge_time = kwargs['converge_time']
            count = kwargs['count']
            valid = kwargs['valid']

            self.mycursor.execute("INSERT INTO stats_table (topo, try, seq_no, node,"
                                " converge_time, count, valid) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                (topo, Try, seq_no, node, converge_time, count, valid))
            self.db.commit()

        else:
            raise AssertionError("Invalid parameters")

    def do_query(self, query, values=None):
        # No values to insert on the query
        if values == None:
            self.mycursor.execute(query)
        else:
            self.mycursor.execute(query, values)

        aux = []
        for x in self.mycursor:
            aux.append(x)
        return aux

    # Deletes all entries with valid == False
    def clean_up_DB(self):
        self.mycursor.execute("SELECT ID FROM stats_table WHERE valid=False")
        aux = self.mycursor
        for id in aux:
            ID = str(id[0])
            sql = "DELETE FROM stats_table WHERE ID=%s"
            values = (ID,)
            self.mycursor.execute(sql,values)
        self.db.commit()

    def close_connection(self):
        print("Closing connection...")
        self.db.close()

if __name__ == "__main__":
    config = {
        "user":"joao",
        "password":"password",
        "port":"3306",
        "host":"192.168.100.249",
        "database":"my_DB"
    }
    api = DB_API(config)

    now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")
    #api.insert_entries(topo='Test', Try=1, seq_no=1, node='s1', converge_time=current_time, count='22', valid=False)
    api.clean_up_DB()
    query = 'SELECT * FROM stats_table'
    print(api.do_query(query))

    api.close_connection()
