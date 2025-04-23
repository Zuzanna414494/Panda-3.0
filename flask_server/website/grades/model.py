from flask_server.website.extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# model ocen (odpowiednik tabeli grades)
class Grades(db.Model, UserMixin):
    grade_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    add_date = db.Column(db.DateTime(timezone=True), default=func.now())
    is_final = db.Column(db.Boolean, nullable=False)

    # relacje zdefiniowane na tabeli grades
    subject = db.relationship('Subjects')