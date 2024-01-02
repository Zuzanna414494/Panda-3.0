from flask import Flask, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .LuckyNumberGenerator import generateLuckyNumber
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time
from sqlalchemy import and_
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"

    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://dziennik_baza_user:MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc@dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com/dziennik_baza'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users, Students, Teachers, Parents, Announcements

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def loader_user(user_id):
        return Users.query.get(int(user_id))

    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    @app.context_processor
    def inject_lucky_number():
        number = generateLuckyNumber()
        return dict(lucky_number=number)

    def archive_old_announcements():
        with app.app_context():
            month_ago = datetime.now() - timedelta(days=30)
            old_announcements = Announcements.query.filter(
                and_(Announcements.add_date <= month_ago,
                    Announcements.in_archive == False)
                ).all()
            for announcement in old_announcements:
                announcement.in_archive = True
                db.session.commit()

    scheduler = BackgroundScheduler()
    scheduler.add_job(archive_old_announcements, trigger='interval', hour=0) # Uruchomienie codziennie o
    # północy

    scheduler.start()

    return app



