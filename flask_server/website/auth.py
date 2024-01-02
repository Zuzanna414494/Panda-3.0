from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user


auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=["GET", "POST"])
@login_required
def sign_up():
    if request.method == "POST":
        user_type = request.form.get("user_type")
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

        elif user_type == "parent":
            new_parent = Parents(parent_id=user_id,
                                 name=request.form.get("name"),
                                 surname=request.form.get("surname"),
                                 student_id=request.form.get("student_id"))
            db.session.add(new_parent)
        elif user_type == "teacher":
            new_teacher = Teachers(teacher_id=user_id,
                                   name=request.form.get("name"),
                                   surname=request.form.get("surname"),
                                   classroom_nr=request.form.get("classroom_nr"),
                                   description=request.form.get("description"))
            db.session.add(new_teacher)

        db.session.commit()
        flash('Account created!', category='success')
        return redirect(url_for('views.profile'))
    return render_template("sign_up.html", user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            login=request.form.get("username")).first()
        if check_password_hash(user.password, request.form.get("password")):
            login_user(user, remember=True)
            flash('Logged in!', category='success')
            return redirect(url_for("views.profile"))
    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
