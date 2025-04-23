from datetime import datetime
from flask import *
from flask_login import login_required, current_user
from flask_server.website.extensions import db
from flask_server.website.classes.service import getClasses
from flask_server.website.models import Students, Subjects, Classes, Grades

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
def grades_teacher(class_name):
    # wyszukanie modelu klasy
    clas = Classes.query.get_or_404(class_name)
    # pobrane nazw wszystkich klas, żeby można było wybrać, do strony z ocenami któej klasy chce się przejść
    classes = getClasses()
    # dla nauczyciela pobranie tych przedmiotów, których uczy w danej klasie
    if current_user.user_type == 'teacher':
        subjects = Subjects.query.filter_by(teacher_id=current_user.user_id, class_name=class_name)
    # dla admina pobranie wszystkich przedmiotów danej klasy
    if current_user.user_type == 'admin':
        subjects = Subjects.query.filter_by(class_name=class_name)
    # pobranie modeli uczniów danej klasy
    students = Students.query.filter_by(class_name=class_name)

    if request.method == "POST":

        # pobranie informacji o nowo dodanej albo zmienionej ocenie
        grade = request.form.get("type")
        weight = request.form.get("weight")
        description = request.form.get("description")

        # jeśli akcja to usuwanie
        if request.form.get("delete"):
            # wyszukanie danej oceny w bazie na podstawie jej id i usunięcie
            Grades.query.filter_by(grade_id=request.form.get("grade_id_delete")).delete()
            db.session.commit()
            # komunikat o poprawnie wykonanej akcji
            flash('Grade deleted!', category='success')

        else:
            # jeśli akcja zmiana zwykłej oceny
            if request.form.get("change"):
                # sprawdzenie, czy poprawnie wprowadzono dane
                if not grade:
                    flash('Empty place!', category='error')
                elif int(grade) > 6 or int(grade) < 1:
                    flash('Wrong grade!', category='error')
                else:
                    # wyszukanie danej oceny w bazie na podstawie jej id i jej edycja
                    grade = Grades.query.filter_by(grade_id=request.form.get("grade_id")).first()
                    grade.type = request.form.get("type")
                    grade.weight = request.form.get("weight")
                    grade.description = request.form.get("description")
                    db.session.commit()
                    flash('Grade changed!', category='success')

            else:
                # dodanie albo zmiana oceny końcowej
                if request.form.get("is_final"):
                    # sprawdzenie, czy poprawnie wprowadzono dane
                    if not grade:
                        flash('Empty place!', category='error')
                    elif int(grade) > 6 or int(grade) < 1:
                        flash('Wrong grade!', category='error')
                    else:

                        # jeśli uczeń nie posiada oceny końcowej z danego przedmiotu to dodanie nowej
                        if int(request.form.get("final_id")) == 0:
                            is_final = True
                            weight = 100
                            description = "Final"
                            new_grade = Grades(
                                subject_id=request.form["subject_id"],
                                type=grade,
                                weight=weight,
                                student_id=request.form["student_id"],
                                description=description,
                                add_date=datetime.now(),
                                is_final=is_final)
                            db.session.add(new_grade)
                            db.session.commit()
                            flash('Grade added!', category='success')

                        # jeśli uczeń posiada, to jej edycja
                        else:
                            grade = Grades.query.filter_by(grade_id=request.form.get("final_id")).first()
                            grade.type = request.form.get("type")
                            grade.add_date = datetime.now()
                            db.session.commit()
                            flash('Grade changed!', category='success')

                # dodanie nowej zwykłej oceny
                else:
                    # sprawdzenie, czy poprawnie wprowadzono dane
                    if not grade or not weight or not description:
                        flash('Empty place!', category='error')
                    elif int(grade) > 6 or int(grade) < 1:
                        flash('Wrong grade!', category='error')
                    else:
                        # wprowadzenie nowej oceny do bazy
                        is_final = False
                        new_grade = Grades(
                            subject_id=request.form["subject_id"],
                            type=grade,
                            weight=weight,
                            student_id=request.form["student_id"],
                            description=description,
                            add_date=datetime.now(),
                            is_final=is_final)
                        db.session.add(new_grade)
                        db.session.commit()
                        flash('Grade added!', category='success')

        # powrót do strony z ocenami danej klasy
        return redirect(url_for('grades.grades_teacher', class_name=class_name))

    return render_template('grades_teacher.html', user=current_user, clas=clas, subjects=subjects,
                           classes=classes, students=students)
