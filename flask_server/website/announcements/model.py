from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_server.website.extensions import db

# model ogłoszeń (odpowiednik tabeli announcements)
class Announcements(db.Model, UserMixin):
    announcement_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    add_date = db.Column(db.DateTime(timezone=True), default=func.now())
    in_archive = db.Column(db.Boolean)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))

    def teacher_name(self):
        from flask_server.website.authorization.model import Teachers
        # Tutaj pobierz nazwę nauczyciela na podstawie teacher_id
        teacher = Teachers.query.filter_by(teacher_id=self.teacher_id).first()
        full_name = teacher.name + " " + teacher.surname
        return full_name if teacher else None

    def title(self):
        return self.description.split('.', 1)[0]