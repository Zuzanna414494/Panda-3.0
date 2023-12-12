from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_nr = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(80), nullable=False)
    logged_in = db.Column(db.Boolean, nullable=False)

    def get_id(self):
        return self.user_id


class Students(db.Model, UserMixin):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    gradebook_nr = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    place_of_birth = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)


class Teachers(db.Model, UserMixin):
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    classroom_nr = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(80), nullable=False)


class Parents(db.Model, UserMixin):
    parent_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    student_id = db.Column(db.Integer, primary_key=True)


class Announcements(db.Model, UserMixin):
    announcement_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    add_date = db.Column(db.DateTime(timezone=True), default=func.now())
    in_archive = db.Column(db.Boolean)
    teacher_id = db.Column(db.Integer)
