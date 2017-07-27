import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
def main():
    try:
        #conn = psycopg2.connect("dbname='legalproblemsdatabase' user='postgres' host='localhost' password='postgres'")
        con = psycopg2.connect("dbname='postgres' user='postgres' host = 'localhost' password='postgres'")
        dbname = "legalproblemsdatabase"
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('CREATE DATABASE ' + dbname)
        cur.close()
        con.close()
    except:
        print ("I am unable to connect to the database")
        #crear base de datos si no existen
        #crear indice flann si no existe
        #servidor rabbit
if __name__ == '__main__':
    main()
