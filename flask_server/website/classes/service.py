import psycopg2
from flask import current_app

# funkcja, która pobiera nazwę i profil każdej klasy w bazie danych
def getClasses():
    # połączenie z bazą danych
    con = psycopg2.connect(database=current_app.config["DATABASE_NAME"],
                           user=current_app.config["DATABASE_USER"],
                           password=current_app.config["DATABASE_PASSWORD"],
                           host=current_app.config["DATABASE_HOST"],
                           port=current_app.config["DATABASE_PORT"])
    # stworzenie kursora
    cur = con.cursor()
    # wykonanie zapytania w bazie za pomocą kursora
    cur.execute(
        "SELECT class_name, class_profile "
        "FROM classes"
    )
    # pobranie wyszukanych danych
    classes_data = cur.fetchall()
    # zamknięcie kursora i połączenia
    cur.close()
    con.close()

    # formatowanie pobranych danych na listę składającą się ze słowników, każdy ma dwa atrybuty: nazwa i profil
    classes = []
    for line in classes_data:
        line_str = ', '.join(map(str, line))
        class_name, class_profile = line_str.split(", ")
        x = {
            "class_name": class_name,
            "class_profile": class_profile,
        }
        classes.append(x)
    # sortowanie nazw klas alfabetycznie
    classes.sort(key=lambda d: d['class_name'])
    # zwrócenie sformatowanych danych
    return classes