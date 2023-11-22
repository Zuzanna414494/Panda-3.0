from flask import *
from flask_login import login_user, logout_user
import psycopg2

from StudentsClass import *
from TeachersClass import *
from UsersClass import *
from ParentsClass import *
# from readGrades import *


# Odtąd działa stara wersja# # ################################################################################
# # Tells flask-sqlalchemy what database to connect to
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# # Enter a secret key
# app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
# # Initialize flask-sqlalchemy extension
# db = SQLAlchemy()
#
# # LoginManager is needed for our application
# # to be able to log in and out users
# login_manager = LoginManager()
# login_manager.init_app(app)
#
#
# class Users(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(250), unique=True, nullable=False)
#     password = db.Column(db.String(250), nullable=False)
#     # user_type = db.Column(db.String(250), nullable=False)
#
#
# # Initialize app with extension
# db.init_app(app)
# # Create database within app context
#
# with app.app_context():
#     db.create_all()
#
#
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            login=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['user_type'] = user.user_type
            session['email'] = user.email
            session['phone'] = user.phone_nr

            if user.user_type == 'teacher':
                teacher = Teachers.query.filter_by(teacher_id=user.user_id).first()
                session['name'] = teacher.name
                session['surname'] = teacher.surname
                session['classroom_nr'] = teacher.classroom_nr
                session['description'] = teacher.description

            if user.user_type == 'parent':
                parent = Parents.query.filter_by(parent_id=user.user_id).first()
                session['parent_id'] = parent.parent_id
                session['name'] = parent.name
                session['surname'] = parent.surname

                session['child_id'] = parent.student_id
                child = Students.query.filter_by(student_id=parent.student_id).first()
                session['child_name'] = child.name
                session['child_surname'] = child.surname
                session['child_gradebook_nr'] = child.gradebook_nr
                session['child_class_name'] = child.class_name
                session['child_date_of_birth'] = child.date_of_birth
                session['child_place_of_birth'] = child.place_of_birth
                session['child_address'] = child.address

            if user.user_type == 'student':
                student = Students.query.filter_by(student_id=user.user_id).first()
                session['student_id'] = student.student_id
                session['name'] = student.name
                session['surname'] = student.surname
                session['gradebook_nr'] = student.gradebook_nr
                session['class_name'] = student.class_name
                session['date_of_birth'] = student.date_of_birth
                session['place_of_birth'] = student.place_of_birth
                session['address'] = student.address

            if user.user_type != 'teacher':

                if user.user_type == 'student':
                    id_for_grades = user.user_id
                else:
                    id_for_grades = parent.student_id

                # session['mat_grades'], session['bio_grades'], session['che_grades'], session['phi_grades'] = readGrades(id_for_grades)
                con = psycopg2.connect(database="dziennik_baza",
                                       user="dziennik_baza_user",
                                       password="MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc",
                                       host="dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com",
                                       port="5432")
                cur = con.cursor()
                cur.execute("SELECT g.type, s.subject_name FROM grades g JOIN subjects s ON g.subject_id=s.subject_id AND g.student_id = %(id)s", {'id': id_for_grades})
                grades_data = cur.fetchall()
                cur.close()
                con.close()

                mat = list()
                bio = list()
                che = list()
                phi = list()
                for row in grades_data:
                    if row[1] == 'matematyka':
                        mat.append(row[0])
                    if row[1] == 'biologia':
                        bio.append(row[0])
                    if row[1] == 'chemia':
                        che.append(row[0])
                    if row[1] == 'fizyka':
                        phi.append(row[0])
                session['mat_grades'] = mat
                session['bio_grades'] = bio
                session['che_grades'] = che
                session['phi_grades'] = phi
                if len(mat) != 0:
                    session['mat_ave'] = sum(mat) / len(mat)
                else:
                    session['mat_ave'] = '-'

                if len(bio) != 0:
                    session['bio_ave'] = sum(bio)/len(bio)
                else:
                    session['bio_ave'] = '-'

                if len(che) != 0:
                    session['che_ave'] = sum(che)/len(che)
                else:
                    session['che_ave'] = '-'

                if len(phi) != 0:
                    session['phi_ave'] = sum(phi)/len(phi)
                else:
                    session['phi_ave'] = '-'

            return redirect(url_for("profile"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
def home():
    return redirect("http://127.0.0.1:5000/login")


@app.route('/grades')
def grades():
    return render_template("grades.html")


@app.route('/plan')
def plan():
    return render_template("plan.html")


@app.route('/announces')
def announces():
    return render_template("announces.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


if __name__ == '__main__':
    app.run(debug=True)
