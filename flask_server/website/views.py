import psycopg2
from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user
from .models import *
from .plan_working import readLessons, readClasses

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


@views.route('/grades/<string:class_name>')
def grades_teacher(class_name):
    clas = Classes.query.get_or_404(class_name)
    classes = readClasses()
    return render_template('grades_teacher.html', user=current_user, clas=clas, classes=classes)


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


@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)
