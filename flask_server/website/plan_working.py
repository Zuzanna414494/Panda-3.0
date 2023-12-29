import psycopg2
from .models import *
from flask_login import current_user


def get_plan():
    days_of_week = []

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


# get_plan()

def readLessons(user_id_l):
    con = psycopg2.connect(database="dziennik_baza",
                           user="dziennik_baza_user",
                           password="MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc",
                           host="dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com",
                           port="5432")
    cur = con.cursor()
    if current_user.user_type == 'student':
        cur.execute(
            "SELECT su.subject_name, l.day_of_week, l.start_time, l.end_time, l.building, l.test "
            "FROM lessons l "
            "JOIN subjects su USING(subject_id) "
            "JOIN classes c USING(class_name) "
            "JOIN students st USING(class_name) "
            "WHERE st.student_id = %(user_id_l)s",
            {'user_id_l': user_id_l}
        )
    elif current_user.user_type == 'teacher':
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
