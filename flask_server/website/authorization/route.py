from flask import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_server.website.extensions import db

authorization = Blueprint('authorization',
                          __name__,
                          static_folder='../static',
                          template_folder='templates',
                          url_prefix='/')


@authorization.route("/")
def home_redirect():
    return redirect(url_for("authorization.login"))


# endpoint służący do rejestrowania nowych użytkowników
@authorization.route('/sign-up', methods=["GET", "POST"])
# żeby dostać się na stronę, trzeba być zalogowanym użytkownikiem
@login_required
def sign_up():
    from flask_server.website.authorization.model import Users, Students, Teachers, Parents

    # do sprawdzania, czy był błąd podczas rejestracji
    error = False

    if request.method == "POST":
        # pobranie danych o użytkowniku
        user_type = request.form.get("user_type")
        login_ = request.form.get("login")
        password = request.form.get("password")
        email = request.form.get("email")
        phone_nr = request.form.get("phone_nr")

        # sprawdzenie, czy wprowadzono dane do modelu User
        if not (user_type and login_ and password and email and phone_nr) or user_type not in ('student', 'teacher', 'parent'):
            # jeśli nie, to komunikat i przekierowanie na stronę do rejestracji
            flash('Error!', category='error')
            error = True
            return redirect(url_for('authorization.sign_up'))

        else:
            # stworzenie modelu nowego użytkownika i dodanie go do bazy danych
            new_user = Users(login=login_,
                         password=generate_password_hash(password),
                         user_type=user_type,
                         email=email,
                         phone_nr=phone_nr,
                         photo=f'{request.form.get("login")}.jpg',
                         logged_in=False)
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.user_id

            # jeśli użytkownik jest uczniem, to po sprowdzeniu, czy wprowadzono wszystkie dane stworzenie modelu nowego
            # ucznia i dodanie go do bazy danych
            if user_type == "student":

                name = request.form.get("name")
                surname = request.form.get("surname")
                gradebook_nr = request.form.get("gradebook_nr")
                class_name = request.form.get("class_name")
                date_of_birth = request.form.get("date_of_birth")
                place_of_birth = request.form.get("place_of_birth")
                address = request.form.get("address")

                if not (name and surname and gradebook_nr and class_name and date_of_birth and place_of_birth and address):
                    flash('Empty place!', category='error')
                    error = True
                    return redirect(url_for('authorization.sign_up'))

                else:
                    new_student = Students(student_id=user_id,
                                           name=name,
                                           surname=surname,
                                           gradebook_nr=gradebook_nr,
                                           class_name=class_name,
                                           date_of_birth=date_of_birth,
                                           place_of_birth=place_of_birth,
                                           address=address)
                    db.session.add(new_student)

            # jeśli użytkownik jest rodzicem, to po sprawdzeniu, czy wprowadzono dane, stworzenie modelu nowego rodzica
            # i dodanie go do bazy danych
            elif user_type == "parent":

                name = request.form.get("name")
                surname = request.form.get("surname")
                student_id = request.form.get("student_id")

                if not (name and surname and student_id):
                    flash('Empty place!', category='error')
                    error = True
                    return redirect(url_for('authorization.sign_up'))

                else:
                    new_parent = Parents(parent_id=user_id,
                                         name=name,
                                         surname=surname,
                                         student_id=student_id)
                    db.session.add(new_parent)

            # jeśli użytkownik jest nauczycielem, to po sprawdzeniu, czy wprowadzono dane, stworzenie modelu nowego
            # nauczyciela i dodanie go do bazy danych
            elif user_type == "teacher":

                name = request.form.get("name")
                surname = request.form.get("surname")
                classroom_nr = request.form.get("classroom_nr")
                description = request.form.get("description")

                if not (name and surname and classroom_nr and description):
                    flash('Empty place!', category='error')
                    error = True
                    return redirect(url_for('authorization.sign_up'))

                else:
                    new_teacher = Teachers(teacher_id=user_id,
                                           name=name,
                                           surname=surname,
                                           classroom_nr=classroom_nr,
                                           description=description)
                    db.session.add(new_teacher)

            if not error:
                db.session.commit()
                # wyświetlenie komunikatu o poprawnym dodaniu nowego użytkownika
                flash('Account created!', category='success')

            # powrót na stronę profilową aktualnego użytkownika
            return redirect(url_for('profile.getProfile'))

    # uruchomienie strony do rejestracji
    return render_template("sign_up.html", user=current_user)


# endpoint służący do logowania do aplikacji
@authorization.route("/login", methods=["GET", "POST"])
def login():
    from flask_server.website.authorization.model import Users
    if request.method == "POST":

        # wyszukiwanie użytkownika o danym loginie
        user = Users.query.filter_by(
            login=request.form.get("username")).first()

        # jeśli nie znalezniono takiego użytkownika w bazie, pokazuje się alert o błędzie
        if not user:
            flash('User not found!', category='error')
            return redirect(url_for("authorization.login"))

        # jeśli użytkownik o danym loginie istnieje i wpisane hasło jest poprawne (odhaszowywanie)
        elif check_password_hash(user.password, request.form.get("password")):
            # zalogowanie i zapamiętanie użytkownika
            login_user(user, remember=True)
            # alert o poprawnym zalogowaniu
            flash('Logged in!', category='success')
            # przekierowanie na stronę profilową użytkownika
            return redirect(url_for("profile.getProfile"))

        # jeśli wpisane hasło dla istniejącego użytkownika jest niepoprawne
        else:
            # alert o błędzie
            flash('Incorrect password!', category='error')
            # powrót na stronę logowania
            return redirect(url_for("authorization.login"))

    # uruchomienie strony do logowania
    return render_template("login.html")


# endpoint służący do wylogowywania
@authorization.route("/logout")
@login_required
def logout():
    # wylogowanie użytkownika
    logout_user()
    # przekierowanie na stronę do logowania
    return redirect(url_for("authorization.login"))
