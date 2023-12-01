import psycopg2
from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
# from readGrades import readGrades


auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        flash('Account created!', category='success')

        return redirect(url_for("login"))
    return render_template("sign_up.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            login=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user, remember=True)
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['user_type'] = user.user_type
            session['email'] = user.email
            session['phone'] = user.phone_nr

            flash('Logged in!', category='success')

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

                # session['mat_grades'], session['bio_grades'], session['che_grades'], session['phi_grades'], session[
                #     'mat_ave'], session['bio_ave'], session['che_ave'], session['phi_ave'] = readGrades(id_for_grades)
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

            return redirect(url_for("views.profile"))
    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
