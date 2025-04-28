from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_server.website.extensions import db
from flask_server.website.authorization.model import Users, Students
from flask_server.website.messages.model import Messages

messages = Blueprint('messages',
    __name__,
    static_folder='../static',
    template_folder='templates',
    url_prefix='/messages'
)

@messages.route('/')
@login_required
def getMessages():
    received_messages = Messages.query.filter_by(receiver_id=current_user.user_id).order_by(Messages.send_date.desc()).all()
    sent_messages = Messages.query.filter_by(sender_id=current_user.user_id).order_by(Messages.send_date.desc()).all()
    return render_template("messages.html", user=current_user, received_messages=received_messages, sent_messages=sent_messages)

@messages.route('/delete/<int:message_id>', methods=["POST"])
@login_required
def deleteMessage(message_id):
    message = Messages.query.get_or_404(message_id)
    if message.sender_id == current_user.user_id or message.receiver_id == current_user.user_id:
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted!', category='success')
    else:
        flash('You do not have permission to delete this message.', category='error')
    return redirect(url_for('messages.getMessages'))

@messages.route('/send', methods=["GET", "POST"])
@login_required
def sendMessage():
    if request.method == "POST":
        receiver_email = request.form.get("receiver_email")
        class_name = request.form.get("class_name")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if receiver_email:
            user = Users.query.filter_by(email=receiver_email).first()
            if not user:
                flash('No user found with that email.', category='error')
                return redirect(url_for('messages.sendMessage'))
            new_message = Messages(
                sender_id=current_user.user_id,
                receiver_id=user.user_id,
                subject=subject,
                body=body
            )
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent!', category='success')

        elif class_name:
            students = Students.query.filter_by(class_name=class_name).all()
            if not students:
                flash('No students found in the selected class.', category='error')
                return redirect(url_for('messages.sendMessage'))
            for student in students:
                new_message = Messages(
                    sender_id=current_user.user_id,
                    receiver_id=student.student_id,
                    subject=subject,
                    body=body
                )
                db.session.add(new_message)
            db.session.commit()
            flash(f'Message sent to class {class_name}!', category='success')

        else:
            flash('Please provide a receiver email or select a class.', category='error')

        return redirect(url_for('messages.getMessages'))

    classes = Students.query.with_entities(Students.class_name).distinct().all()
    return render_template("send_message.html", user=current_user, classes=classes)

# FORWARD MESSAGE
@messages.route('/forward/<int:message_id>', methods=["GET", "POST"])
@login_required
def forwardMessage(message_id):
    original_message = Messages.query.get_or_404(message_id)

    if request.method == "POST":
        receiver_email = request.form.get("receiver_email")
        if receiver_email:
            user = Users.query.filter_by(email=receiver_email).first()
            if not user:
                flash('No user found with that email.', category='error')
                return redirect(url_for('messages.forwardMessage', message_id=message_id))

            new_message = Messages(
                sender_id=current_user.user_id,
                receiver_id=user.user_id,
                subject=original_message.subject,
                body=original_message.body,
                forwarded=True
            )
            db.session.add(new_message)
            db.session.commit()
            flash('Message forwarded!', category='success')
            return redirect(url_for('messages.getMessages'))
        else:
            flash('Please provide receiver email.', category='error')

    return render_template('forward_message.html', user=current_user, original_message=original_message)
