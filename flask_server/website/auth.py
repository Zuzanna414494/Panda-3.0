from flask import *
from flask_login import login_user, logout_user, login_required
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user


auth = Blueprint('auth', __name__)


# endpoint służący do rejestrowania nowych użytkowników
@auth.route('/sign-up', methods=["GET", "POST"])
# żeby dostać się na stronę, trzeba być zalogowanym użytkownikiem
@login_required
def sign_up():
    if request.method == "POST":
        # pobranie rodzaju użytkownika
        user_type = request.form.get("user_type")

        # stworzenie modelu nowego użytkownika i dodanie go do bazy danych
        new_user = Users(login=request.form.get("login"),
                     password=generate_password_hash(request.form.get("password")),
                     user_type=user_type,
                     email=request.form.get("email"),
                     phone_nr=request.form.get("phone_nr"),
                     photo=f'{request.form.get("login")}.jpg',
                     logged_in=False)
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.user_id

        # jeśli użytkownik jest uczniem, to stworzenie modelu nowego ucznia i dodanie go do bazy danych
        if user_type == "student":
            new_student = Students(student_id=user_id,
                                   name=request.form.get("name"),
                                   surname=request.form.get("surname"),
                                   gradebook_nr=request.form.get("gradebook_nr"),
                                   class_name=request.form.get("class_name"),
                                   date_of_birth=request.form.get("date_of_birth"),
                                   place_of_birth=request.form.get("place_of_birth"),
                                   address=request.form.get("address"))
            db.session.add(new_student)

        # jeśli użytkownik jest rodzicem, to stworzenie modelu nowego rodzica i dodanie go do bazy danych
        elif user_type == "parent":
            new_parent = Parents(parent_id=user_id,
                                 name=request.form.get("name"),
                                 surname=request.form.get("surname"),
                                 student_id=request.form.get("student_id"))
            db.session.add(new_parent)

        # jeśli użytkownik jest nauczycielem, to stworzenie modelu nowego nauczyciela i dodanie go do bazy danych
        elif user_type == "teacher":
            new_teacher = Teachers(teacher_id=user_id,
                                   name=request.form.get("name"),
                                   surname=request.form.get("surname"),
                                   classroom_nr=request.form.get("classroom_nr"),
                                   description=request.form.get("description"))
            db.session.add(new_teacher)

        db.session.commit()
        # wyświetlenie komunikatu o poprawnym dodaniu nowego użytkownika
        flash('Account created!', category='success')

        # powrót na stronę profilową aktualnego użytkownika
        return redirect(url_for('views.profile'))

    # uruchomienie strony do rejestracji
    return render_template("sign_up.html", user=current_user)


# endpoint służący do logowania do aplikacji
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # wyszukiwanie użytkownika o danym loginie
        user = Users.query.filter_by(
            login=request.form.get("username")).first()

        # jeśli nie znalezniono takiego użytkownika w bazie, pokazuje się alert o błędzie
        if not user:
            flash('User not found!', category='error')
            return redirect(url_for("auth.login"))

        # jeśli użytkownik o danym loginie istnieje i wpisane hasło jest poprawne (odhaszowywanie)
        elif check_password_hash(user.password, request.form.get("password")):
            # zalogowanie i zapamiętanie użytkownika
            login_user(user, remember=True)
            # alert o poprawnym zalogowaniu
            flash('Logged in!', category='success')
            # przekierowanie na stronę profilową użytkownika
            return redirect(url_for("views.profile"))

        # jeśli wpisane hasło dla istniejącego użytkownika jest niepoprawne
        else:
            # alert o błędzie
            flash('Incorrect password!', category='error')
            # powrót na stronę logowania
            return redirect(url_for("auth.login"))

    # uruchomienie strony do logowania
    return render_template("login.html")


# endpoint służący do wylogowywania
@auth.route("/logout")
@login_required
def logout():
    # wylogowanie użytkownika
    logout_user()
    # przekierowanie na stronę do logowania
    return redirect(url_for("auth.login"))
