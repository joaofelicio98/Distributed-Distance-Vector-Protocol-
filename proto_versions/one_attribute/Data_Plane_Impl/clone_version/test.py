import sys
import os.path as path

sys.path.append('../../DB_API')
from DB_API import DB_API

api = DB_API()
query = 'SELECT * FROM stats_table'
print(api.do_query(query))
api.close_connection()
