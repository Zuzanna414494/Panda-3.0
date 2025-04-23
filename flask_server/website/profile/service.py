import psycopg2
from flask import current_app
from flask_server.website.authorization.model import Teachers
import random
import datetime


# generating lucky number that stays the same during the day and changes the next day
def generateLuckyNumber(current_date=None):
    if current_date is None:
        current_date = datetime.date.today()
    seed_date = current_date.toordinal()
    random.seed(seed_date)
    lucky_number = random.randint(1, 20)
    return lucky_number

# funkcja zwracająca wyniki wyszukiwania użytkowników
def search(searched):
    # deklaracja listy z wynikami wyszukiwania
    users = []
    # połączenie z bazą danych
    con = psycopg2.connect(database=current_app.config["DATABASE_NAME"],
                           user=current_app.config["DATABASE_USER"],
                           password=current_app.config["DATABASE_PASSWORD"],
                           host=current_app.config["DATABASE_HOST"],
                           port=current_app.config["DATABASE_PORT"])
    # stworzenie kursora
    cur = con.cursor()
    # wykonanie zapytania w bazie za pomocą kursora - wyszukiwanie uczniów
    cur.execute(
        "SELECT name, surname, student_id, user_type "
        "FROM students "
        "JOIN users on user_id=student_id "
        "WHERE name ilike %(searched)s or surname ilike %(searched)s ",
        {'searched': '%' + searched + '%'}
    )
    # pobranie wyszukanych danych
    students_data = cur.fetchall()
    # zamknięcie kursora i połączenia
    cur.close()
    # dodanie uczniów do zwracanego słownika
    addNamesToDict(users, students_data)

    # wykonanie zapytania w bazie za pomocą kursora - wyszukiwanie nauczycieli
    cur = con.cursor()
    cur.execute(
        "SELECT name, surname, teacher_id, user_type "
        "FROM teachers "
        "JOIN users on user_id=teacher_id "
        "WHERE name ilike %(searched)s or surname ilike %(searched)s ",
        {'searched': '%' + searched + '%'}
    )
    teachers_data = cur.fetchall()
    cur.close()
    # dodanie nauczycieli do zwracanego słownika
    addNamesToDict(users, teachers_data)

    # wykonanie zapytania w bazie za pomocą kursora - wyszukiwanie rodziców
    cur = con.cursor()
    cur.execute(
        "SELECT name, surname, parent_id, user_type "
        "FROM parents "
        "JOIN users on user_id=parent_id "
        "WHERE name ilike %(searched)s or surname ilike %(searched)s ",
        {'searched': '%' + searched + '%'}
    )
    parents_data = cur.fetchall()
    cur.close()
    con.close()
    # dodanie rodziców do zwracanego słownika
    addNamesToDict(users, parents_data)

    # sortowanie wyników alfabetycznie
    users.sort(key=lambda d: d['surname'])
    # zwrócenie wyników wyszukiwania
    return users


# funkcja przekształcająca pobrane wyniki wyszukiwania użytkowników z bazy danych
def addNamesToDict(users, data):
    # formatowanie pobranych danych na słowniki (każdy ma dwa atrybuty: nazwa i nazwisko) i dodanie ich do listy z wynikami
    for line in data:
        line_str = ', '.join(map(str, line))
        name, surname, user_id, user_type = line_str.split(", ")
        x = {
            "name": name,
            "surname": surname,
            "user_id": user_id,
            "user_type": user_type
        }
        users.append(x)


def getTeachers():
    teachers_list=Teachers.query.all()
    teachers_info = []
    for teacher in teachers_list:
        teacher_info = {
            'teacher_id': teacher.teacher_id,
            'name': teacher.name,
            'surname': teacher.surname,
            'full_name':teacher.name+" "+teacher.surname
        }
        teachers_info.append(teacher_info)
    return teachers_info

def getTeacher(teacher_id):
    teacher=Teachers.query.get(teacher_id)
    teacher_info = {
        'teacher_id': teacher.teacher_id,
        'name': teacher.name,
        'surname': teacher.surname,
        'full_name':teacher.name+" "+teacher.surname
    }
    return teacher_info