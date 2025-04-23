from flask_server.website.extensions import db
from flask_login import UserMixin

# model przedmiotów (odpowiednik tabeli subjects)
class Subjects(db.Model, UserMixin):
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(80), nullable=False)
    class_name = db.Column(db.String(80), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)

    # relacje zdefiniowane na tabeli subjects
    # grades = db.relationship('Grades')


# model zajęć (odpowiednik tabeli lessons)
class Lessons(db.Model, UserMixin):
    lesson_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    day_of_week = db.Column(db.String(15), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    building=db.Column(db.String(20),nullable=True)
    test = db.Column(db.String(80), nullable=True)