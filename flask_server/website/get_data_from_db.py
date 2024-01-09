import psycopg2


def get_plan():
    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []

    days_of_week = [monday, tuesday, wednesday, thursday, friday]

    for x in range(1, 9):
        monday.append("null")
        tuesday.append("null")
        wednesday.append("null")
        thursday.append("null")
        friday.append("null")

    print(days_of_week)


def readLessons(user_id_l, user_type):
    con = psycopg2.connect(database="dziennik_baza",
                           user="dziennik_baza_user",
                           password="MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc",
                           host="dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com",
                           port="5432")
    cur = con.cursor()
    if user_type == 'student' or user_type == 'admin':
        cur.execute(
            "SELECT su.subject_name, l.day_of_week, l.start_time, l.end_time, l.building, l.test "
            "FROM lessons l "
            "JOIN subjects su USING(subject_id) "
            "JOIN classes c USING(class_name) "
            "JOIN students st USING(class_name) "
            "WHERE st.student_id = %(user_id_l)s",
            {'user_id_l': user_id_l}
        )
    elif user_type == 'teacher':
        cur.execute(
            "SELECT su.subject_name, l.day_of_week, l.start_time, l.end_time, l.building, l.test "
            "FROM lessons l "
            "JOIN subjects su USING(subject_id) "
            "JOIN teachers t USING(teacher_id) "
            "WHERE t.teacher_id = %(user_id_l)s",
            {'user_id_l': user_id_l}
        )
    else:
        """
        child = None
        child = Students.query.filter_by(student_id=current_user.parent[0].student_id).first()
        user_id_l=child.student_id
        """
        cur.execute(
            "SELECT su.subject_name, l.day_of_week, l.start_time, l.end_time, l.building, l.test "
            "FROM lessons l "
            "JOIN subjects su USING(subject_id) "
            "JOIN classes c USING(class_name) "
            "JOIN students st USING(class_name) "
            "WHERE st.student_id = %(user_id_l)s",
            {'user_id_l': user_id_l}
        )

    lessons_data = cur.fetchall()
    cur.close()
    con.close()

    zajecia = []

    for line in lessons_data:
        # Konwertuj każdą krotkę na łańcuch, łącząc jej elementy za pomocą przecinków
        line_str = ', '.join(map(str, line))
        # Teraz możemy podzielić łańcuch na poszczególne części
        subject, day_of_week, start_time, end_time, building, test = line_str.split(", ")
        lesson = {
            "subject": subject,
            "day_of_week": day_of_week,
            "start_time": start_time[:-3],
            "end_time": end_time[:-3],
            "building": building,
            "test": test
        }
        zajecia.append(lesson)
    return zajecia


def readClasses():
    con = psycopg2.connect(database="dziennik_baza",
                           user="dziennik_baza_user",
                           password="MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc",
                           host="dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com",
                           port="5432")
    cur = con.cursor()
    cur.execute(
        "SELECT class_name, class_profile "
        "FROM classes"
    )
    classes_data = cur.fetchall()
    cur.close()
    con.close()
    classes = []
    for line in classes_data:
        line_str = ', '.join(map(str, line))
        class_name, class_profile = line_str.split(", ")
        x = {
            "class_name": class_name,
            "class_profile": class_profile,
        }
        classes.append(x)
    classes.sort(key=lambda d: d['class_name'])
    return classes


def search(searched):
    con = psycopg2.connect(database="dziennik_baza",
                           user="dziennik_baza_user",
                           password="MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc",
                           host="dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com",
                           port="5432")
    cur = con.cursor()
    cur.execute(
        "SELECT name, surname "
        "FROM students "
        "WHERE name ilike %(searched)s or surname ilike %(searched)s ",
        {'searched': '%' + searched + '%'}
    )
    students_data = cur.fetchall()
    cur.close()
    users = []
    for line in students_data:
        line_str = ', '.join(map(str, line))
        name, surname = line_str.split(", ")
        x = {
            "name": name,
            "surname": surname,
        }
        users.append(x)

    cur = con.cursor()
    cur.execute(
        "SELECT name, surname "
        "FROM teachers "
        "WHERE name ilike %(searched)s or surname ilike %(searched)s ",
        {'searched': '%' + searched + '%'}
    )
    teachers_data = cur.fetchall()
    cur.close()
    for line in teachers_data:
        line_str = ', '.join(map(str, line))
        name, surname = line_str.split(", ")
        x = {
            "name": name,
            "surname": surname,
        }
        users.append(x)

    cur = con.cursor()
    cur.execute(
        "SELECT name, surname "
        "FROM parents "
        "WHERE name ilike %(searched)s or surname ilike %(searched)s ",
        {'searched': '%' + searched + '%'}
    )
    parents_data = cur.fetchall()
    cur.close()
    con.close()
    for line in parents_data:
        line_str = ', '.join(map(str, line))
        name, surname = line_str.split(", ")
        x = {
            "name": name,
            "surname": surname,
        }
        users.append(x)

    users.sort(key=lambda d: d['surname'])
    return users
