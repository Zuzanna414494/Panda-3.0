from flask import *
from flask_login import login_required, current_user
from datetime import datetime
from flask_server.website.extensions import db
from flask_server.website.timetable.model import Lessons, Subjects
from flask_server.website.authorization.model import Students
from flask_server.website.profile.service import getTeacher, getTeachers
from flask_server.website.timetable.service import getTeacherLessons, getLessons
from flask_server.website.classes.service import getClasses


timetable = Blueprint('timetable',
                      __name__,
                      static_folder='../static',
                      template_folder='templates',
                      url_prefix='/timetable')

# ---------- PLAN WYŚWIETLANIE ----------

@timetable.route('/')
@login_required
def plan():
    if current_user.user_type == 'parent':
        child = Students.query.filter_by(student_id=current_user.parent[0].student_id).first()
        zajecia = getLessons(child.student_id, current_user.user_type)
        return render_template("plan.html", user=current_user, zajecia=zajecia)

    elif current_user.user_type == 'admin':
        classes = getClasses()
        teachers = getTeachers()
        return render_template("plan.html", user=current_user, classes=classes, teachers=teachers)

    elif current_user.user_type == 'teacher':
        classes = getClasses()
        zajecia = getLessons(current_user.user_id, current_user.user_type)
        return render_template("plan.html", user=current_user, zajecia=zajecia, classes=classes)

    else:  # student
        zajecia = getLessons(current_user.user_id, current_user.user_type)
        return render_template("plan.html", user=current_user, zajecia=zajecia)


# Plan klasy dla nauczyciela
@timetable.route('/class/<string:class_name>', methods=["GET"])
@login_required
def plan_teacher(class_name):
    classes = getClasses()
    child = Students.query.filter_by(class_name=class_name).first()
    zajecia = getLessons(child.student_id, 'admin')
    return render_template("plan_teacher.html", user=current_user, class_name=class_name, zajecia=zajecia, classes=classes)


# Plan klasy dla admina
@timetable.route('/admin/class/<string:class_name>', methods=["GET"])
@login_required
def plan_for_admin_classes(class_name):
    if current_user.user_type == 'admin':
        classes = getClasses()
        child = Students.query.filter_by(class_name=class_name).first()
        zajecia = getLessons(child.student_id, 'admin')
        teachers = getTeachers()
        subjects = Subjects.query.filter_by(class_name=class_name).all()

        return render_template("plan_admin.html", user=current_user, zajecia=zajecia, classes=classes,
                               class_name=class_name, teachers=teachers, want_teacher=False,
                               subjects=subjects)


# Plan nauczyciela dla admina
@timetable.route('/admin/teacher/<int:teacher_id>', methods=["GET"])
@login_required
def plan_for_admin_teachers(teacher_id):
    if current_user.user_type == 'admin':
        zajecia = getTeacherLessons(teacher_id)
        teachers = getTeachers()
        classes = getClasses()
        teacher = getTeacher(teacher_id)
        return render_template("plan_admin.html", user=current_user, zajecia=zajecia,
                               teachers=teachers, teacher=teacher, classes=classes, want_teacher=True)


# ---------- OPERACJE NA LEKCJACH (tylko admin) ----------

@timetable.route('/add_lesson', methods=["POST"])
@login_required
def add_lesson():
    if current_user.user_type != 'admin':
        return "Unauthorized", 403

    try:
        subject_id = int(request.form['subject_id'])
        day_of_week = request.form['day_of_week']
        time_slot = request.form['time_slot']
        building = request.form['building']
        test = request.form['test'] if request.form['test'] else None

        start_time_str, end_time_str = time_slot.split('-')

        dummy_date = "1900-01-01"
        start_time = datetime.strptime(f"{dummy_date} {start_time_str}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{dummy_date} {end_time_str}", "%Y-%m-%d %H:%M")

        if start_time >= end_time:
            flash("Start time must be before end time.", category="error")
            return redirect(request.referrer)

        new_lesson = Lessons(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            building=building,
            test=test
        )
        db.session.add(new_lesson)
        db.session.commit()
        flash("Lesson added successfully.", category="success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding lesson: {str(e)}", category="error")

    return redirect(request.referrer)


@timetable.route('/edit_lesson/<int:lesson_id>', methods=["POST"])
@login_required
def edit_lesson(lesson_id):
    if current_user.user_type != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    lesson = Lessons.query.get_or_404(lesson_id)
    data = request.form
    try:
        lesson.building = data.get('building')
        lesson.test = data.get('test') or None
        db.session.commit()
        flash("Lesson updated successfully", category="success")
        return redirect(request.referrer)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@timetable.route('/delete_lesson/<int:lesson_id>', methods=["POST"])
@login_required
def delete_lesson(lesson_id):
    if current_user.user_type != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    lesson = Lessons.query.get_or_404(lesson_id)
    try:
        db.session.delete(lesson)
        db.session.commit()
        flash("Lesson deleted successfully", category="success")
        return redirect(request.referrer)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@timetable.route('/add_substitute', methods=["POST"])
@login_required
def add_substitute():
    if current_user.user_type != 'admin':
        return "Unauthorized", 403

    try:
        subject_id = int(request.form['subject_id'])
        day_of_week = request.form['day_of_week']
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']
        building = request.form['building']
        test_note = request.form['test']  # tu wpisujemy np. "Zastępstwo za ..."

        dummy_date = "1900-01-01"
        start_time = datetime.strptime(f"{dummy_date} {start_time_str}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{dummy_date} {end_time_str}", "%Y-%m-%d %H:%M")

        lesson = Lessons(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            building=building,
            test=test_note
        )

        db.session.add(lesson)
        db.session.commit()
        flash("Zastępstwo dodane pomyślnie.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Błąd przy dodawaniu zastępstwa: {str(e)}", "error")

    return redirect(request.referrer)

@timetable.route('/edit_test/<int:lesson_id>', methods=["POST"])
@login_required
def edit_test(lesson_id):
    if current_user.user_type != 'teacher':
        return "Unauthorized", 403

    lesson = Lessons.query.get_or_404(lesson_id)

    # zabezpieczenie: czy to jego lekcja
    subject = Subjects.query.get(lesson.subject_id)
    if subject.teacher_id != current_user.user_id:
        return "Unauthorized", 403

    new_test = request.form.get("test") or None

    try:
        lesson.test = new_test
        db.session.commit()
        flash("Test/zastępstwo zaktualizowane.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Błąd: {str(e)}", "error")

    return redirect(request.referrer)
