from flask_server.website.extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Messages(db.Model, UserMixin):
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(5000), nullable=False)
    send_date = db.Column(db.DateTime(timezone=True), default=func.now())
    forwarded = db.Column(db.Boolean, default=False)

    def sender_name(self):
        from flask_server.website.authorization.model import Users
        sender = Users.query.get(self.sender_id)
        return f"{sender.login}" if sender else "Unknown"

    def receiver_name(self):
        from flask_server.website.authorization.model import Users
        receiver = Users.query.get(self.receiver_id)
        return f"{receiver.login}" if receiver else "Unknown"
