import psycopg2
from config import postgres

try:
    print('[+] Connecting to the database...\n')
    DB = psycopg2.connect(host=postgres["ENDPOINT"],
                          port=postgres["PORT"],
                          user=postgres["USR"],
                          dbname=postgres["DBNAME"],
                          password=postgres["PASSWORD"])
except Exception as e:
    ERROR = e
    print('\n[-] Error while connecting to the database:\n', e)

cur = DB.cursor()
cur.execute("create table images (name varchar(50), url varchar(200) not null, primary key (name));")
cur.close()
DB.commit()
