from flask import *
from flask_login import login_required, current_user
from flask_server.website.authorization.model import Students
from flask_server.website.profile.service import getTeacher, getTeachers
from flask_server.website.timetable.service import getTeacherLessons, getLessons
from flask_server.website.classes.service import getClasses

timetable = Blueprint('timetable',
                          __name__,
                          static_folder='../static',
                          template_folder='templates',
                          url_prefix='/timetable')


# endpoint wyświetlający plan zajęć
@timetable.route('/')
@login_required
def plan():
    # jeśli użytkownik to rodzic, to pobranie modelu jego dziecka i wczytanie jego zajęć
    if current_user.user_type == 'parent':
        child = Students.query.filter_by(student_id=current_user.parent[0].student_id).first()
        zajecia = getLessons(child.student_id, current_user.user_type)

    # jeśli użytkownik to admin, to wczytanie wszystkich klas - będzie mógł wybrać której klasy plan chce zobaczyć
    elif current_user.user_type == 'admin':
        classes = getClasses()
        teachers = getTeachers()
        return render_template("plan.html", user=current_user, classes=classes, teachers=teachers)

    # jeśli użytkownik to nauczyciel, to wczytanie wszystkich klas - będzie mógł wybrać której klasy plan chce zobaczyć
    # - oraz wczytanie jego własnych zajęć (na początku zobaczy też swój plan)
    elif current_user.user_type == 'teacher':
        classes = getClasses()
        zajecia = getLessons(current_user.user_id, current_user.user_type)
        return render_template("plan.html", user=current_user, zajecia=zajecia, classes=classes)

    # jeśli użytkownik to uczeń, to wczytanie jego zajęć
    else:
        zajecia = getLessons(current_user.user_id, current_user.user_type)

    return render_template("plan.html", user=current_user, zajecia=zajecia)


# endpoint wyświetlający plan zajęć danej klasy dla nauczyciela
@timetable.route('/<string:class_name>', methods=["GET", "POST"])
@login_required
def plan_teacher(class_name):
    # wczytanie wszystkich klas, aby można było którąś wybrać
    classes = getClasses()
    # wczytanie zajęć uczniów z danej klasy
    child = Students.query.filter_by(class_name=class_name).first()
    zajecia = getLessons(child.student_id, 'admin')

    return render_template("plan_teacher.html", user=current_user, class_name=class_name, zajecia=zajecia,
                           classes=classes)


# endpoint wyświetlający plan zajęć danej klasy dla admina
@timetable.route('/<string:class_name>a', methods=["GET", "POST"])
@login_required
def plan_for_admin_classes(class_name):
    if current_user.user_type == 'admin':
        classes = getClasses()
        child = Students.query.filter_by(class_name=class_name).first()
        zajecia = getLessons(child.student_id, 'admin')
        teachers = getTeachers()
        want_teacher = False
        return render_template("plan_admin.html", user=current_user, zajecia=zajecia, classes=classes,
                               class_name=class_name, teachers=teachers, want_teacher=want_teacher)


# endpoint wyświetlający plan zajęć danenego nauczyciela klasy dla admina
@timetable.route('/<int:teacher_id>', methods=["GET", "POST"])
@login_required
def plan_for_admin_teachers(teacher_id):
    if current_user.user_type == 'admin':
        zajecia = getTeacherLessons(teacher_id)
        teachers = getTeachers()
        classes = getClasses()
        teacher = getTeacher(teacher_id)
        want_teacher = True
        return render_template("plan_admin.html", user=current_user, zajecia=zajecia, teachers=teachers,
                               teacher=teacher, classes=classes, want_teacher=want_teacher)

