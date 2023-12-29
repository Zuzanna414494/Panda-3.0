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

    student = db.relationship('Students')
    teacher = db.relationship('Teachers')
    parent = db.relationship('Parents')

    def get_id(self):
        return self.user_id


class Students(db.Model, UserMixin):
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    gradebook_nr = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    place_of_birth = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)

    parent = db.relationship('Parents')
    grades = db.relationship('Grades')


class Teachers(db.Model, UserMixin):
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    classroom_nr = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(80), nullable=False)

    announcement = db.relationship('Announcements')
    subjects = db.relationship('Subjects')


class Parents(db.Model, UserMixin):
    parent_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))

    child = db.relationship('Students')


class Announcements(db.Model, UserMixin):
    announcement_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    add_date = db.Column(db.DateTime(timezone=True), default=func.now())
    in_archive = db.Column(db.Boolean)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))

    def teacher_name(self):
        # Tutaj pobierz nazwę nauczyciela na podstawie teacher_id
        teacher = Teachers.query.filter_by(teacher_id=self.teacher_id).first()
        full_name=teacher.name+" "+teacher.surname
        return full_name if teacher else None
    def title(self):
        return self.description.split('.', 1)[0]


class Grades(db.Model, UserMixin):
    grade_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    add_date = db.Column(db.DateTime(timezone=True), default=func.now())

    subject = db.relationship('Subjects')


class Subjects(db.Model, UserMixin):
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(80), nullable=False)
    class_name = db.Column(db.String(80), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=False)

    grades = db.relationship('Grades')


class Lessons(db.Model, UserMixin):
    lesson_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    day_of_week = db.Column(db.String(15), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    test = db.Column(db.String(80), nullable=True)


class Classes(db.Model, UserMixin):
    class_name = db.Column(db.String(10), primary_key=True)
    homeroom_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=True)
    class_profile = db.Column(db.String(50), nullable=False)
