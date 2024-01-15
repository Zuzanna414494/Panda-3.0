from datetime import datetime
from flask import *
from flask_login import login_required, current_user
from .models import *
from .get_data_from_db import *

views = Blueprint('views', __name__)


# endpoint domyślny - strona logowania
@views.route("/")
def home():
    return redirect(url_for("auth.login"))


# endpoint wyświetlający stronę z ocenami
@views.route('/grades')
@login_required
def grades():
    # jeśli użytkownik jest nauczycielem albo administratorem, następuje pobranie wszystkich klas,
    # żeby mógł wybrać, której klasy oceny chce zobaczyć
    if current_user.user_type == 'teacher' or current_user.user_type == 'admin':
        classes = readClasses()
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
@views.route('/grades/<string:class_name>', methods=["GET", "POST"])
def grades_teacher(class_name):
    # wyszukanie modelu klasy
    clas = Classes.query.get_or_404(class_name)
    # pobrane nazw wszystkich klas, żeby można było wybrać, do strony z ocenami któej klasy chce się przejść
    classes = readClasses()
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
        return redirect(url_for('views.grades_teacher', class_name=class_name))

    return render_template('grades_teacher.html', user=current_user, clas=clas, subjects=subjects,
                           classes=classes, students=students)


# endpoint wyświetlający plan zajęć
@views.route('/plan')
@login_required
def plan():

    # jeśli użytkownik to rodzic, to pobranie modelu jego dziecka i wczytanie jego zajęć
    if current_user.user_type == 'parent':
        child = Students.query.filter_by(student_id=current_user.parent[0].student_id).first()
        zajecia = readLessons(child.student_id, current_user.user_type)

    # jeśli użytkownik to admin, to wczytanie wszystkich klas - będzie mógł wybrać której klasy plan chce zobaczyć
    elif current_user.user_type == 'admin':
        classes = readClasses()
        teachers = read_teachers()
        return render_template("plan.html", user=current_user, classes=classes,teachers=teachers)

    # jeśli użytkownik to nauczyciel, to wczytanie wszystkich klas - będzie mógł wybrać której klasy plan chce zobaczyć
    # - oraz wczytanie jego własnych zajęć (na początku zobaczy też swój plan)
    elif current_user.user_type == 'teacher':
        classes = readClasses()
        zajecia = readLessons(current_user.user_id, current_user.user_type)
        return render_template("plan.html", user=current_user, zajecia=zajecia, classes=classes)

    # jeśli użytkownik to uczeń, to wczytanie jego zajęć
    else:
        zajecia = readLessons(current_user.user_id, current_user.user_type)

    return render_template("plan.html", user=current_user, zajecia=zajecia)


# endpoint wyświetlający plan zajęć danej klasy dla nauczyciela
@views.route('/plan/<string:class_name>', methods=["GET", "POST"])
@login_required
def plan_teacher(class_name):

    # wczytanie wszystkich klas, aby można było którąś wybrać
    classes = readClasses()
    # wczytanie zajęć uczniów z danej klasy
    child = Students.query.filter_by(class_name=class_name).first()
    zajecia = readLessons(child.student_id, 'admin')

    return render_template("plan_teacher.html", user=current_user, class_name=class_name, zajecia=zajecia,
                           classes=classes)

# endpoint wyświetlający plan zajęć danej klasy dla admina
@views.route('/plan/<string:class_name>a', methods=["GET", "POST"])
@login_required
def plan_for_admin_classes(class_name):
    if current_user.user_type == 'admin':
        classes = readClasses()
        child = Students.query.filter_by(class_name=class_name).first()
        zajecia = readLessons(child.student_id, 'admin')
        teachers = read_teachers()
        want_teacher=False
        return render_template("plan_admin.html", user=current_user, zajecia=zajecia,classes=classes,
                               class_name=class_name, teachers=teachers,want_teacher=want_teacher)

# endpoint wyświetlający plan zajęć danenego nauczyciela klasy dla admina
@views.route('/plan/<int:teacher_id>', methods=["GET", "POST"])
@login_required
def plan_for_admin_teachers(teacher_id):
    if current_user.user_type == 'admin':
        zajecia = read_lessons(teacher_id)
        teachers=read_teachers()
        classes = readClasses()
        teacher=read_teacher(teacher_id)
        want_teacher=True
        return render_template("plan_admin.html", user=current_user, zajecia=zajecia,teachers=teachers,
                               teacher=teacher,classes=classes,want_teacher=want_teacher)

# endpoint wyświetlający ogłoszenia
@views.route('/announcements')
@login_required
def announcements():
    filtered_announcements = Announcements.query.filter(Announcements.in_archive == False).order_by(
        Announcements.add_date.desc()).all()
    return render_template("announcements.html", user=current_user, filtered_announcements=filtered_announcements,
                           user_id=current_user.user_id)

# endpoint wyświetlający szczegóły ogłoszenia
@views.route('/announcement/<int:announcement_id>', methods=["GET", "POST"])
def announcement_details(announcement_id):
    announcement = Announcements.query.get_or_404(announcement_id)
    if request.method == "POST":
        Announcements.query.filter_by(announcement_id=request.form.get("announcement_id")).delete()
        db.session.commit()
        flash('Announcement deleted!', category='success')
        filtered_announcements = Announcements.query.filter(Announcements.in_archive == False).order_by(
            Announcements.add_date.desc()).all()
        return render_template("announcements.html", user=current_user, filtered_announcements=filtered_announcements)
    return render_template('announcement_details.html', user=current_user, announcement=announcement)

# endpoint służący do edytowania ogłoszeń
@views.route('/edit_announcement/<int:announcement_id>', methods=["GET","POST"])
@login_required
def edit_announcement(announcement_id):
    announcement = Announcements.query.get_or_404(announcement_id)
    if request.method=="POST":
        data = request.json
        announcement_id = data.get("announcement_id")
        new_description = data.get("description")
        # Znajdujemy ogłoszenie o podanym announcement_id
        announcement = Announcements.query.filter_by(announcement_id=announcement_id).first()
        if announcement is not None:
            try:
                announcement.description = new_description
                db.session.commit()
                return redirect(url_for('views.announcements'))
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": "Failed to update description", "details": str(e)}), 500
        else:
            return jsonify({"error": "Announcement not found"}), 404

    return render_template("edit_announcement.html",user=current_user,announcement_id=announcement_id,announcement=announcement)

# endpoint służący do dodawania nowych ogłoszeń
@views.route('/add-announcement', methods=["GET", "POST"])
@login_required
def add_announcement():

    if request.method == "POST":

        # sprawdzenie, czy poprawnie wprowadzono dane
        if not request.form.get("description"):
            flash('Empty place!', category='error')

        # dodanie nowego ogłoszenia do bazy
        else:
            new_announcement = Announcements(
                description=request.form.get("description"),
                add_date=datetime.now(),
                in_archive=False,
                teacher_id=current_user.user_id)
            db.session.add(new_announcement)
            db.session.commit()
            announcement_id = new_announcement.announcement_id

    return render_template("add_announcement.html", user=current_user)


# endpoint służący do wyświetlania strony profilowej użytkownika oraz do wyszukiwania innych użytkowników
@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    # wyszukiwanie innych użytkowników
    if request.method == "POST":
        searched = request.form.get("search")
        users = search(searched)
        return render_template("profile.html", user=current_user, searched=searched, users=users)

    return render_template("profile.html", user=current_user)


# endpoint służący do wyświetlania strony profilowej wyszukanego użytkownika
@views.route('/profile/<int:user_id>')
@login_required
def searched_profile(user_id):
    searched_user = Users.query.filter_by(user_id=user_id).first()

    return render_template("searched_profile.html", user=current_user, searched_user=searched_user)
