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


# # edycja adresu studenta
# @profile.route('/edit_address/<int:student_id>', methods=['GET', 'POST'])
# @login_required
# def edit_address(student_id):
#     if request.method == 'POST':
#         data = request.get_json()
#         new_address = data.get('address')
#         student = Students.query.get(student_id)
#         if student:
#             student.address = new_address
#             db.session.commit()
#             flash('Address updated successfully!', category='success')
#             return redirect(url_for('profile.getProfile'))
#         else:
#             return {"error": "Student not found"}, 404
#     return render_template('edit_address.html', student_id=student_id)
#
#
# # edycja numeru telefonu
# @profile.route('/edit_phone/<int:user_id>', methods=['GET', 'POST'])
# @login_required
# def edit_phone(user_id):
#     if request.method == 'POST':
#         data = request.get_json()
#         new_phone = data.get('phone_nr')
#         user = Users.query.get(user_id)
#         if user:
#             user.phone_nr = new_phone
#             db.session.commit()
#             flash('Phone number updated successfully!', category='success')
#             return redirect(url_for('profile.getProfile'))
#         else:
#             return {"error": "User not found"}, 404
#     return render_template('edit_phone_number.html', user_id=user_id)
