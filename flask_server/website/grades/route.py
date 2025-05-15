from datetime import datetime
from flask import *
from flask_login import login_required, current_user
from flask_server.website.extensions import db
from flask_server.website.classes.service import getClasses
from flask_server.website.classes.model import Classes
from flask_server.website.timetable.model import Subjects
from flask_server.website.grades.model import Grades
from flask_server.website.authorization.model import Students
from flask import request, render_template

grades = Blueprint('grades',
                          __name__,
                          static_folder='../static',
                          template_folder='templates',
                          url_prefix='/grades')

# endpoint wyświetlający stronę z ocenami
@grades.route('/')
@login_required
def getGrades():
    # jeśli użytkownik jest nauczycielem albo administratorem, następuje pobranie wszystkich klas,
    # żeby mógł wybrać, której klasy oceny chce zobaczyć
    if current_user.user_type == 'teacher' or current_user.user_type == 'admin':
        classes = getClasses()
        return render_template("grades.html", user=current_user, classes=classes)

    child = None
    # jeśli użytkownik jest rodzicem, następuje wyszukanie modelu ucznia jego dziecka
    if current_user.user_type == 'parent':
        child = Students.query.filter_by(student_id=current_user.parent[0].student_id).first()
    # jeśli użytkownik jest uczniem, od razu przypisanie do 'child' jego modelu ucznia
    elif current_user.user_type == 'student':
        child = current_user.student[0]
    # pobranie przedmiotów klasy, do której jezt przypisany uczeń (albo dziecko)
    subjects = Subjects.query.filter_by(class_name=child.class_name)

    return render_template("grades.html", user=current_user, child=child, subjects=subjects)


# endpoint wyświetlający oceny danej klasy (dla nauczyciela albo admina), pobiera nazwę danej klasy

@grades.route('<string:class_name>', methods=["GET", "POST"])
@login_required
def grades_teacher(class_name):
    # Pobierz klasę (przykładowo, dostosuj do swojej logiki)
    clas = Classes.query.filter_by(class_name=class_name).first()

    # Pobierz przedmioty nauczane w tej klasie (dla nauczyciela lub admina)
    if current_user.user_type == 'teacher':
        subjects = Subjects.query.filter_by(teacher_id=current_user.user_id, class_name=class_name).all()
    else:  # admin
        subjects = Subjects.query.filter_by(class_name=class_name).all()

    # Pobierz wszystkie klasy do wyboru (np. dla dropdowna)
    classes = Classes.query.all()

    # Pobierz uczniów w klasie
    students = Students.query.filter_by(class_name=class_name).all()

    # Funkcja do obliczenia średniej ocen ucznia dla tej klasy (i nauczyciela jeśli dotyczy)
    def student_average(student):
        relevant_grades = []
        for grade in student.grades:
            # Sprawdzamy czy ocena jest z przedmiotu tej klasy
            if grade.subject.class_name == class_name:
                # Jeśli nauczyciel, to tylko jego przedmioty
                if current_user.user_type == 'teacher':
                    if grade.subject.teacher_id != current_user.user_id:
                        continue
                # Pomijamy oceny końcowe
                if not grade.is_final:
                    relevant_grades.append((grade.type, grade.weight))
        if not relevant_grades:
            return 0
        weighted_sum = sum(g * w for g, w in relevant_grades)
        weight_sum = sum(w for _, w in relevant_grades)
        if weight_sum == 0:
            return 0
        return weighted_sum / weight_sum

    # Pobierz parametr sortowania z URL (domyślnie rosnąco)
    sort_order = request.args.get('sort', 'asc')

    # Sortuj uczniów po średniej ocen
    students = list(students)
    students.sort(key=student_average, reverse=(sort_order == 'desc'))

    return render_template(
        'grades_teacher.html',
        user=current_user,
        clas=clas,
        subjects=subjects,
        classes=classes,
        students=students,
        sort_order=sort_order,
        student_average=student_average
    )

