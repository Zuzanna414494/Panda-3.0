from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dziennik_baza_user:MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc@dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com/dziennik_baza'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users, Students, Teachers, Parents

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def loader_user(user_id):
        return Users.query.get(user_id)

    return app
