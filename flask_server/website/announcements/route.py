from flask import *
from datetime import datetime
from flask_login import login_required, current_user
from flask_server.website.extensions import db
from flask_server.website.models import Announcements

announcements = Blueprint('announcements',
                          __name__,
                          static_folder='../static',
                          template_folder='templates',
                          url_prefix='/announcements')

# endpoint wyświetlający ogłoszenia
@announcements.route('/')
@login_required
def getAnnouncements():
    filtered_announcements = Announcements.query.filter(Announcements.in_archive == False).order_by(
        Announcements.add_date.desc()).all()
    return render_template("announcements.html", user=current_user, filtered_announcements=filtered_announcements,
                           user_id=current_user.user_id)


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
@announcements.route('/edit/<int:announcement_id>', methods=["GET", "POST"])
@login_required
def editAnnouncement(announcement_id):
    announcement = Announcements.query.get_or_404(announcement_id)
    if request.method == "POST":
        data = request.json
        announcement_id = data.get("announcement_id")
        new_description = data.get("description")
        # Znajdujemy ogłoszenie o podanym announcement_id
        announcement = Announcements.query.filter_by(announcement_id=announcement_id).first()
        if announcement is not None:
            try:
                announcement.description = new_description
                db.session.commit()
                return redirect(url_for('announcements.getAnnouncements'))
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": "Failed to update description", "details": str(e)}), 500
        else:
            return jsonify({"error": "Announcement not found"}), 404

    return render_template("edit_announcement.html", user=current_user, announcement_id=announcement_id,
                           announcement=announcement)


# endpoint służący do dodawania nowych ogłoszeń
@announcements.route('/add', methods=["GET", "POST"])
@login_required
def addAnnouncement():
    if request.method == "POST":

        # sprawdzenie, czy poprawnie wprowadzono dane
        if not request.form.get("description"):
            flash('Empty place!', category='error')

        # dodanie nowego ogłoszenia do bazy
        else:
            new_announcement = Announcements(
                description=request.form.get("description"),
                add_date=datetime.now(),
                in_archive=False,
                teacher_id=current_user.user_id)
            db.session.add(new_announcement)
            db.session.commit()
            announcement_id = new_announcement.announcement_id

    return render_template("add_announcement.html", user=current_user)
