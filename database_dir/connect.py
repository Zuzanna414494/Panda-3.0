"""c
# !/usr/bin/python
import psycopg2
from config import config


def connect():
    #Connect to the PostgreSQL database server
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')




        cur.execute("SELECT * FROM users where user_type like 'teacher';")






        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
"""

from sqlalchemy import create_engine

# Tworzenie URL'a połączenia na podstawie danych z config.py
db_url = "postgresql+psycopg2://postgres:malibu@localhost/dziennik_db"

# Tworzenie silnika SQLAlchemy
engine = create_engine(db_url)
