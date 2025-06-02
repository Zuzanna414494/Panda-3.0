from datetime import datetime, date
from flask import *
from flask_login import login_required, current_user
from flask_server.website.extensions import db
from flask_server.website.classes.service import getClasses
from flask_server.website.classes.model import Classes
from flask_server.website.timetable.model import Subjects
from flask_server.website.behavioral_notes.model import BehavioralNotes
from flask_server.website.authorization.model import Students, Users
from flask import request, render_template

behavioral_notes = Blueprint('behavioral_notes',
                             __name__,
                             static_folder='../static',
                             template_folder='templates',
                             url_prefix='/behavioral_notes')


# endpoint wyświetlający stronę z notatkami behawioralnymi
@behavioral_notes.route('/')
@login_required
def getBehavioralNotes():
    # jeśli użytkownik jest nauczycielem albo administratorem, następuje pobranie wszystkich klas,
    # żeby mógł wybrać, której klasy notatki chce zobaczyć
    if current_user.user_type == 'teacher' or current_user.user_type == 'admin':
        classes = getClasses()
        return render_template("behavioral_notes.html", user=current_user, classes=classes)

    child = None
    # jeśli użytkownik jest rodzicem, następuje wyszukanie modelu ucznia jego dziecka
    if current_user.user_type == 'parent':
        child = Students.query.filter_by(student_id=current_user.parent[0].student_id).first()
    # jeśli użytkownik jest uczniem, od razu przypisanie do 'child' jego modelu ucznia
    elif current_user.user_type == 'student':
        child = current_user.student[0]

    # pobranie notatek behawioralnych dla ucznia
    notes = BehavioralNotes.query.filter_by(student_id=child.student_id).order_by(BehavioralNotes.add_date.desc()).all()

    # pobranie przedmiotów klasy, do której jest przypisany uczeń (albo dziecko)
    subjects = Subjects.query.filter_by(class_name=child.class_name)

    return render_template("behavioral_notes.html", user=current_user, child=child, notes=notes, subjects=subjects)


# endpoint wyświetlający notatki behawioralne danej klasy (dla nauczyciela albo admina)
@behavioral_notes.route('<string:class_name>', methods=["GET", "POST"])
@login_required
def behavioral_notes_teacher(class_name):
    # Obsługa POST - dodawanie, edycja i usuwanie notatek
    if request.method == "POST":
        # Dodawanie nowej notatki
        if 'add_note' in request.form:
            new_note = BehavioralNotes(
                student_id=request.form.get('student_id'),
                teacher_id=current_user.user_id,
                subject_id=request.form.get('subject_id') if request.form.get('subject_id') else None,
                behavior_type=request.form.get('behavior_type'),
                category=request.form.get('category'),
                title=request.form.get('title'),
                description=request.form.get('description'),
                behavior_score=request.form.get('behavior_score'),
                incident_date=datetime.strptime(request.form.get('incident_date'),
                                                '%Y-%m-%d').date() if request.form.get(
                    'incident_date') else date.today(),
                requires_followup=True if request.form.get('requires_followup') == 'on' else False
            )
            db.session.add(new_note)
            db.session.commit()
            flash('Notatka została dodana pomyślnie!', 'success')

        # Edycja notatki
        elif 'edit_note' in request.form:
            note_id = request.form.get('note_id')
            note = BehavioralNotes.query.get(note_id)
            if note:
                note.behavior_type = request.form.get('behavior_type')
                note.category = request.form.get('category')
                note.title = request.form.get('title')
                note.description = request.form.get('description')
                note.behavior_score = request.form.get('behavior_score')
                note.incident_date = datetime.strptime(request.form.get('incident_date'), '%Y-%m-%d').date()
                note.requires_followup = True if request.form.get('requires_followup') == 'on' else False
                db.session.commit()
                flash('Notatka została zaktualizowana!', 'success')

        # Usuwanie notatki
        elif 'delete_note' in request.form:
            note_id = request.form.get('note_id_delete')
            note = BehavioralNotes.query.get(note_id)
            if note:
                db.session.delete(note)
                db.session.commit()
                flash('Notatka została usunięta!', 'success')

        # Oznaczanie rodzica jako powiadomionego
        elif 'notify_parent' in request.form:
            note_id = request.form.get('note_id')
            note = BehavioralNotes.query.get(note_id)
            if note:
                note.parent_notified = True
                note.parent_notification_date = datetime.now()
                db.session.commit()
                flash('Rodzic został oznaczony jako powiadomiony!', 'success')

        # Oznaczanie follow-up jako zakończony
        elif 'complete_followup' in request.form:
            note_id = request.form.get('note_id')
            note = BehavioralNotes.query.get(note_id)
            if note:
                note.followup_completed = True
                note.followup_date = datetime.now()
                note.followup_notes = request.form.get('followup_notes')
                db.session.commit()
                flash('Działania następcze zostały oznaczone jako zakończone!', 'success')

    # Pobierz klasę
    clas = Classes.query.filter_by(class_name=class_name).first()

    # Pobierz przedmioty nauczane w tej klasie (dla nauczyciela lub admina)
    if current_user.user_type == 'teacher':
        subjects = Subjects.query.filter_by(teacher_id=current_user.user_id, class_name=class_name).all()
    else:  # admin
        subjects = Subjects.query.filter_by(class_name=class_name).all()

    # Pobierz wszystkie klasy do wyboru (np. dla dropdowna)
    classes = Classes.query.all()

    # Pobierz uczniów w klasie
    students = Students.query.filter_by(class_name=class_name).all()

    # Pobierz wszystkie notatki behawioralne dla tej klasy
    student_ids = [student.student_id for student in students]
    notes = BehavioralNotes.query.filter(BehavioralNotes.student_id.in_(student_ids)).order_by(
        BehavioralNotes.add_date.desc()).all()

    # Pobierz parametr sortowania z URL (domyślnie malejąco - najnowsze pierwsze)
    sort_order = request.args.get('sort', 'desc')

    # Sortuj notatki
    if sort_order == 'asc':
        notes = sorted(notes, key=lambda x: x.add_date)
    else:
        notes = sorted(notes, key=lambda x: x.add_date, reverse=True)

    return render_template(
        'behavioral_notes_teacher.html',
        user=current_user,
        clas=clas,
        subjects=subjects,
        classes=classes,
        students=students,
        notes=notes,
        sort_order=sort_order
    )