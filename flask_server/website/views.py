from datetime import datetime
from flask import *
from flask_login import login_required, current_user
from .models import *
from .plan_working import *

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return redirect(url_for("auth.login"))


@views.route('/grades')
@login_required
def grades():
    if current_user.user_type == 'teacher':
        classes = readClasses()
        return render_template("grades.html", user=current_user, classes=classes)

    child = None
    if current_user.user_type == 'parent':
        child = Students.query.filter_by(student_id=current_user.parent[0].student_id).first()
    elif current_user.user_type == 'student':
        child = current_user.student[0]
    return render_template("grades.html", user=current_user, child=child)


@views.route('/grades/<string:class_name>', methods=["GET", "POST"])
def grades_teacher(class_name):
    clas = Classes.query.get_or_404(class_name)
    classes = readClasses()
    subjects = Subjects.query.filter_by(teacher_id=current_user.user_id, class_name=class_name)
    students = Students.query.filter_by(class_name=class_name)

    if request.method == "POST":
        grade = request.form.get("type")
        if int(grade) > 6 or int(grade) < 1:
            flash('Wrong grade!', category='error')
        else:
            new_grade = Grades(
                subject_id=request.form["subject_id"],
                type=grade,
                weight=request.form.get("weight"),
                student_id=request.form["student_id"],
                description=request.form.get("description"),
                add_date=datetime.now(),
                is_final=False)
            db.session.add(new_grade)
            db.session.commit()
            flash('Grade added!', category='success')
        return redirect(url_for('views.grades_teacher', class_name=class_name))
    return render_template('grades_teacher.html', user=current_user, clas=clas, subjects=subjects,
                           classes=classes, students=students)


@views.route('/plan')
@login_required
def plan():
    if current_user.user_type == 'parent':
        child = Students.query.filter_by(student_id=current_user.parent[0].student_id).first()
        zajecia = readLessons(child.student_id)
    else:
        zajecia = readLessons(current_user.user_id)
    return render_template("plan.html", user=current_user, zajecia=zajecia)


@views.route('/announcements')
@login_required
def announcements():
    filtered_announcements = Announcements.query.filter(Announcements.in_archive == False).order_by(
        Announcements.add_date.desc()).all()
    return render_template("announcements.html", user=current_user, filtered_announcements=filtered_announcements)


@views.route('/announcement/<int:announcement_id>')
def announcement_details(announcement_id):
    announcement = Announcements.query.get_or_404(announcement_id)
    return render_template('announcement_details.html', user=current_user, announcement=announcement)


@views.route('/add-announcement', methods=["GET", "POST"])
@login_required
def add_announcement():
    if request.method == "POST":
        new_announcement = Announcements(
                     description=request.form.get("description"),
                     add_date=datetime.now(),
                     in_archive=False,
                     teacher_id=current_user.user_id)
        db.session.add(new_announcement)
        db.session.commit()
        announcement_id = new_announcement.announcement_id

    return render_template("add_announcement.html", user=current_user)


@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)
