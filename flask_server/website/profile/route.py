from flask import *
from flask_login import login_required, current_user
from flask_server.website.authorization.model import Users
from flask_server.website.authorization.model import Students
from flask_server.website.extensions import db
from .service import search

profile = Blueprint('profile',
                    __name__,
                    static_folder='../static',
                    template_folder='templates',
                    url_prefix='/profile')


# endpoint służący do wyświetlania strony profilowej użytkownika oraz do wyszukiwania innych użytkowników
@profile.route('/', methods=['GET', 'POST'])
@login_required
def getProfile():
    # wyszukiwanie innych użytkowników
    if request.method == "POST":
        searched = request.form.get("search")
        print(searched)
        users = search(searched)
        return render_template("profile.html", user=current_user, searched=searched, users=users)

    return render_template("profile.html", user=current_user)


# endpoint służący do wyświetlania strony profilowej wyszukanego użytkownika
@profile.route('/<int:user_id>', methods=['GET', 'POST'])
@login_required
def searched_profile(user_id):
    searched_user = Users.query.filter_by(user_id=user_id).first()

    # if request.method == "POST":
    #     if request.form.get("delete"):
    #         Students.query.filter_by(student_id=request.form.get("user_id_delete")).delete()
    #         # Users.query.filter_by(user_id=request.form.get("user_id_delete")).delete()
    #         db.session.commit()
    #         flash('User deleted!', category='success')
    #         return redirect(url_for('views.profile'))

    return render_template("searched_profile.html", user=current_user, searched_user=searched_user)


# Edycja adresu zamieszkania studenta
@profile.route('/edit_address', methods=['POST'])
@login_required
def edit_address():
    new_address = request.form.get('new_address')
    if not new_address:
        flash('Address cannot be empty!', category='error')
        return redirect(url_for('profile.getProfile'))

    student = Students.query.filter_by(student_id=current_user.user_id).first()
    if student:
        student.address = new_address
        db.session.commit()
        flash('Address updated successfully!', category='success')
    else:
        flash('Student not found.', category='error')
    return redirect(url_for('profile.getProfile'))


# Edycja numeru telefonu użytkownika
@profile.route('/edit_phone', methods=['POST'])
@login_required
def edit_phone():
    new_phone = request.form.get('new_phone')
    if not new_phone or not new_phone.isdigit() or len(new_phone) != 9:
        flash('Phone number must have exactly 9 digits!', category='error')
        return redirect(url_for('profile.getProfile'))

    user = Users.query.get(current_user.user_id)
    if user:
        user.phone_nr = int(new_phone)
        db.session.commit()
        flash('Phone number updated successfully!', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('profile.getProfile'))
