from flask import *
from datetime import datetime
from flask_login import login_required, current_user
from flask_server.website.extensions import db
from flask_server.website.announcements.model import Announcements

announcements = Blueprint('announcements',
                          __name__,
                          static_folder='../static',
                          template_folder='templates',
                          url_prefix='/announcements')

# endpoint wyświetlający ogłoszenia
@announcements.route('/')
@login_required
def getAnnouncements():
    filtered_announcements = Announcements.query \
        .filter(Announcements.in_archive == False) \
        .order_by(Announcements.add_date.desc()) \
        .all()
    return render_template("announcements.html",
                           user=current_user,
                           filtered_announcements=filtered_announcements)



# endpoint wyświetlający szczegóły ogłoszenia
@announcements.route('/<int:announcement_id>', methods=["GET", "POST"])
def getAnnouncementDetails(announcement_id):
    announcement = Announcements.query.get_or_404(announcement_id)
    if request.method == "POST":
        Announcements.query.filter_by(announcement_id=request.form.get("announcement_id")).delete()
        db.session.commit()
        flash('Announcement deleted!', category='success')
        filtered_announcements = Announcements.query.filter(Announcements.in_archive == False).order_by(
            Announcements.add_date.desc()).all()
        return render_template("announcements.html", user=current_user, filtered_announcements=filtered_announcements)
    return render_template('announcement_details.html', user=current_user, announcement=announcement)


# endpoint służący do edytowania ogłoszeń
# @announcements.route('/edit/<int:announcement_id>', methods=["GET", "POST"])
# @login_required
# def editAnnouncement(announcement_id):
#     announcement = Announcements.query.get_or_404(announcement_id)
#     if request.method == "POST":
#         data = request.json
#         announcement_id = data.get("announcement_id")
#         new_description = data.get("description")
#         # Znajdujemy ogłoszenie o podanym announcement_id
#         announcement = Announcements.query.filter_by(announcement_id=announcement_id).first()
#         if announcement is not None:
#             try:
#                 announcement.description = new_description
#                 db.session.commit()
#                 return redirect(url_for('announcements.getAnnouncements'))
#             except Exception as e:
#                 db.session.rollback()
#                 return jsonify({"error": "Failed to update description", "details": str(e)}), 500
#         else:
#             return jsonify({"error": "Announcement not found"}), 404

#     return render_template("edit_announcement.html", user=current_user, announcement_id=announcement_id,
#                            announcement=announcement)

@announcements.route('/edit/<int:announcement_id>', methods=["GET", "POST"])
@login_required
def editAnnouncement(announcement_id):
    announcement = Announcements.query.get_or_404(announcement_id)

    # Zabezpieczenie – tylko autor lub admin
    if current_user.user_type != 'admin' and current_user.user_id != announcement.teacher_id:
        flash("You don't have permission to edit this announcement.", category="error")
        return redirect(url_for('announcements.getAnnouncements'))

    if request.method == "POST":
        new_description = request.form.get("description")

        if not new_description:
            flash("Description is required.", category="error")
        else:
            print("EDYTUJEMY:", new_description)  # ✅ sprawdź w konsoli
            announcement.description = new_description
            db.session.commit()
            flash("Announcement updated.", category="success")
            return redirect(url_for('announcements.getAnnouncementDetails', announcement_id=announcement.announcement_id))

    return render_template("edit_announcement.html", user=current_user, announcement=announcement)


# endpoint służący do dodawania nowych ogłoszeń
@announcements.route('/add', methods=["GET", "POST"])
@login_required
def addAnnouncement():
    if request.method == "POST":
        description = request.form.get("description")
        if not description:
            flash("Description is required.", category="error")
        else:
            new_announcement = Announcements(
                description=description,
                add_date=datetime.now(),
                in_archive=False,
                teacher_id=current_user.user_id
            )
            db.session.add(new_announcement)
            db.session.commit()
            flash("Announcement added!", category="success")
            return redirect(url_for('announcements.getAnnouncements'))  # ✅ ważne przekierowanie

    return render_template("add_announcement.html", user=current_user)

