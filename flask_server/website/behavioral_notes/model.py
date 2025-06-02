from flask_server.website.extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# model notatek behawioralnych (odpowiednik tabeli behavioral_notes)
class BehavioralNotes(db.Model, UserMixin):
    note_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=True)

    # Typ zachowania: positive, negative, neutral
    behavior_type = db.Column(db.String(20), nullable=False)

    # Kategoria: discipline, participation, homework, social_behavior, academic_performance, attendance, other
    category = db.Column(db.String(30), nullable=False)

    # Treść notatki
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    # Ocena zachowania (1-5, gdzie 5 = bardzo dobre)
    behavior_score = db.Column(db.Integer, nullable=True, default=3)

    # Daty
    incident_date = db.Column(db.Date, nullable=False, default=func.current_date())
    add_date = db.Column(db.DateTime(timezone=True), default=func.now())

    # Czy rodzic został powiadomiony
    parent_notified = db.Column(db.Boolean, default=False)
    parent_notification_date = db.Column(db.DateTime(timezone=True), nullable=True)

    # Czy wymaga działań następczych
    requires_followup = db.Column(db.Boolean, default=False)
    followup_completed = db.Column(db.Boolean, default=False)
    followup_date = db.Column(db.DateTime(timezone=True), nullable=True)
    followup_notes = db.Column(db.String(300), nullable=True)

    # relacje zdefiniowane na tabeli behavioral_notes
    subject = db.relationship('Subjects')
    student = db.relationship('Students')
    teacher = db.relationship('Users')