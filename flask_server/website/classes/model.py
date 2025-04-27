from flask_server.website.extensions import db
from flask_login import UserMixin


# model klas (odpowiednik tabeli classes)
class Classes(db.Model, UserMixin):
    class_name = db.Column(db.String(10), primary_key=True)
    homeroom_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=True)
    class_profile = db.Column(db.String(50), nullable=False)
