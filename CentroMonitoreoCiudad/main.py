import psycopg2
def main():
    try:
        connectionLegalProblems = psycopg2.connect("dbname='cmcdatabase' user='postgres' host='localhost' password='postgres'")
    except:
        print ("I am unable to connect to the database")
        #crear base de datos si no existen
        #crear indice flann si no existe
        #servidor rabbit
if __name__ == '__main__':
    main()
