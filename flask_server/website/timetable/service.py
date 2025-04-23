import psycopg2
from flask import current_app
from flask_server.website.timetable.model import Lessons
from flask_server.website.authorization.model import Teachers


def getLessons(user_id_l, user_type):
    con = psycopg2.connect(database=current_app.config["DATABASE_NAME"],
                           user=current_app.config["DATABASE_USER"],
                           password=current_app.config["DATABASE_PASSWORD"],
                           host=current_app.config["DATABASE_HOST"],
                           port=current_app.config["DATABASE_PORT"])
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
        line_str = ', '.join(map(str, line))
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

def getTeacherLessons(teacher_id):
    teacher = Teachers.query.get(teacher_id)

    subjects = teacher.subjects

    lesson_info_list = []

    for subject in subjects:
        lessons = Lessons.query.filter_by(subject_id=subject.subject_id).all()
        for lesson in lessons:
            if lesson.test==None:
                lesson.test=" "
            lesson_info = {
                "subject": subject.subject_name,
                "day_of_week": lesson.day_of_week,
                "start_time": lesson.start_time.strftime('%H:%M'),
                "end_time": lesson.end_time.strftime('%H:%M'),
                "building":lesson.building,
                "test": lesson.test
            }
            lesson_info_list.append(lesson_info)

    return lesson_info_list

