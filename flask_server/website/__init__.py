import yaml
from flask import Flask
from flask_login import LoginManager
from flask_server.website.profile.service import generateLuckyNumber
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from sqlalchemy import and_
from pathlib import Path
from flask_server.website.extensions import db


def create_app(config_name=None):
    # stworzenie instancji Flask
    app = Flask(__name__)

    base_dir = Path(__file__).parent
    if config_name == 'testing':
        app.config["SECRET_KEY"] = "TEST_SECRET_KEY"
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        config_path = base_dir / "config.yml"
        with open(config_path, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            app.config.update(config)

    db.init_app(app)

    # stworzenie blueprint - jeden do autoryzacji (logowanie, wylogowywanie i rejestracja) i jeden do obsługi reszty funkcjonalności
    from .authorization.route import authorization
    from .grades.route import grades
    from .timetable.route import timetable
    from .announcements.route import announcements
    from .profile.route import profile
    from .messages.route import messages
    from .behavioral_notes.route import behavioral_notes

    app.register_blueprint(authorization)
    app.register_blueprint(grades)
    app.register_blueprint(timetable)
    app.register_blueprint(announcements)
    app.register_blueprint(profile)
    app.register_blueprint(messages)
    app.register_blueprint(behavioral_notes)

    # deklaracja LoginManager do obsługi logowania i zapamiętywania zalogowanych użytkowników, sesji
    login_manager = LoginManager()
    login_manager.login_view = 'authorization.login'
    login_manager.init_app(app)

    # funkcja potrzebna dla LoginManagera do zapamiętania użytkownika
    @login_manager.user_loader
    def loader_user(user_id):
        from .authorization.model import Users
        return Users.query.get(int(user_id))

    # funkcja odpowiedzialna za to, żeby po wylogowaniu nie dało się wrócić do widoku strony zalogowanego użytkownika
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    @app.context_processor
    def inject_lucky_number():
        number = generateLuckyNumber()
        return dict(lucky_number=number)

    def archive_old_announcements():
        from flask_server.website.announcements.model import Announcements
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
    scheduler.add_job(archive_old_announcements, trigger='cron', hour=0)
    # Uruchomienie codziennie o północy

    scheduler.start()

    return app
