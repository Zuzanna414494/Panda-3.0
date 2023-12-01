import psycopg2


def average(grades):
    if len(grades) != 0:
        return sum(grades) / len(grades)
    else:
        return '-'


def readGrades(id_for_grades):
    con = psycopg2.connect(database="dziennik_baza",
                           user="dziennik_baza_user",
                           password="MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc",
                           host="dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com",
                           port="5432")
    cur = con.cursor()
    cur.execute(
        "SELECT g.type, s.subject_name FROM grades g JOIN subjects s ON g.subject_id=s.subject_id AND g.student_id = %(id)s",
        {'id': id_for_grades})
    grades_data = cur.fetchall()
    cur.close()
    con.close()

    mat = list()
    bio = list()
    che = list()
    phi = list()
    for row in grades_data:
        if row[1] == 'matematyka':
            mat.append(row[0])
        if row[1] == 'biologia':
            bio.append(row[0])
        if row[1] == 'chemia':
            che.append(row[0])
        if row[1] == 'fizyka':
            phi.append(row[0])

    # mat = average(mat)
    # bio = average(bio)
    # che = average(che)
    # phi = average(phi)

    return [mat, bio, che, phi, average(mat), average(bio), average(che), average(phi)]
