import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user="root",
        passwd="MHCA2407",
        database="dogodb"
    )