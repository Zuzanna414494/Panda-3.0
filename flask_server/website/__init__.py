import yaml
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .LuckyNumberGenerator import generateLuckyNumber
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from sqlalchemy import and_

db = SQLAlchemy()


def create_app():
    # stworzenie instancji Flask
    app = Flask(__name__)

    with open("C:\\Users\\Gabi\\PycharmProjects\\Inżynieria_oprogramowania\\Inżynieria_oprogramowania\\flask_server\\website\\config.yml", "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        app.config.update(config)

    db.init_app(app)

    # stworzenie blueprint - jeden do autoryzacji (logowanie, wylogowywanie i rejestracja) i jeden do obsługi reszty funkcjonalności
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users, Students, Teachers, Parents, Announcements

    # deklaracja LoginManager do obsługi logowania i zapamiętywania zalogowanych użytkowników, sesji
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # funkcja potrzebna dla LoginManagera do zapamiętania użytkownika
    @login_manager.user_loader
    def loader_user(user_id):
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
