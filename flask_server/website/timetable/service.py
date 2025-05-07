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

    query = """
        SELECT l.lesson_id, su.subject_name, l.day_of_week, l.start_time, l.end_time, l.building, l.test
        FROM lessons l
        JOIN subjects su ON l.subject_id = su.subject_id
        JOIN students st ON st.class_name = su.class_name
        WHERE st.student_id = %(user_id)s
    """

    if user_type == 'teacher':
        query = """
            SELECT l.lesson_id, su.subject_name, l.day_of_week, l.start_time, l.end_time, l.building, l.test
            FROM lessons l
            JOIN subjects su ON l.subject_id = su.subject_id
            WHERE su.teacher_id = %(user_id)s
        """

    cur.execute(query, {'user_id': user_id_l})
    lessons_data = cur.fetchall()
    cur.close()
    con.close()

    zajecia = []
    for row in lessons_data:
        lesson = {
            "lesson_id": row[0],
            "subject": row[1],
            "day_of_week": row[2],
            "start_time": row[3].strftime('%H:%M'),
            "end_time": row[4].strftime('%H:%M'),
            "building": row[5],
            "test": row[6]
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

def getTeacherLessons(teacher_id):
    con = psycopg2.connect(database=current_app.config["DATABASE_NAME"],
                           user=current_app.config["DATABASE_USER"],
                           password=current_app.config["DATABASE_PASSWORD"],
                           host=current_app.config["DATABASE_HOST"],
                           port=current_app.config["DATABASE_PORT"])
    cur = con.cursor()

    query = """
        SELECT l.lesson_id, su.subject_name, l.day_of_week, l.start_time, l.end_time, l.building, l.test
        FROM lessons l
        JOIN subjects su ON l.subject_id = su.subject_id
        WHERE su.teacher_id = %(teacher_id)s
    """

    cur.execute(query, {'teacher_id': teacher_id})
    lessons_data = cur.fetchall()
    cur.close()
    con.close()

    lesson_info_list = []
    for row in lessons_data:
        lesson_info = {
            "lesson_id": row[0],
            "subject": row[1],
            "day_of_week": row[2],
            "start_time": row[3].strftime('%H:%M'),
            "end_time": row[4].strftime('%H:%M'),
            "building": row[5],
            "test": row[6]
        }
        lesson_info_list.append(lesson_info)

    return lesson_info_list
