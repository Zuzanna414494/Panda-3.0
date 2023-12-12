from flask import Blueprint, redirect, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return redirect("http://127.0.0.1:5000/login")


@views.route('/grades')
@login_required
def grades():
    return render_template("grades.html")


@views.route('/plan')
@login_required
def plan():
    return render_template("plan.html")


@views.route('/announcements')
@login_required
def announcements():
    return render_template("announcements.html")


@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html")
