from sqlalchemy.orm import sessionmaker
from connect import engine  # Zaimportuj stworzony wcześniej engine
from sqlalchemy import text


Session = sessionmaker(bind=engine)
session = Session()

def get_user_info():
    query = text("SELECT * FROM users;")
    result = session.execute(query)
    for row in result:
        print(row)

def get_teacher_info():
    query = text("SELECT * FROM teachers;")
    result = session.execute(query)
    for row in result:
        print(row)
get_user_info()
print("next")
get_teacher_info()
