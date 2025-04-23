from flask_login import UserMixin
from flask_server.website.extensions import db


# model użytkownika (odpowiednik tabeli users)
class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_nr = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(80), nullable=True)
    logged_in = db.Column(db.Boolean, nullable=True)

    # relacje zdefiniowane na tabeli users
    student = db.relationship('Students')
    teacher = db.relationship('Teachers')
    parent = db.relationship('Parents')

    # funkcja zwracająca id użytkownika
    def get_id(self):
        return self.user_id


# model ucznia (odpowiednik tabeli students)
class Students(db.Model, UserMixin):
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    gradebook_nr = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    place_of_birth = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)

    # relacje zdefiniowane na tabeli students
    # parent = db.relationship('Parents')
    grades = db.relationship('Grades')


# model nauczyciela (odpowiednik tabeli teachers)
class Teachers(db.Model, UserMixin):
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    classroom_nr = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(80), nullable=False)

    # relacje zdefiniowane na tabeli teachers
    announcement = db.relationship('Announcements')
    subjects = db.relationship('Subjects')


# model rodzica (odpowiednik tabeli parents)
class Parents(db.Model, UserMixin):
    parent_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))

    # relacje zdefiniowane na tabeli parents
    child = db.relationship('Students')