from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


app = Flask(__name__)

app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://dziennik_baza_user:MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc@dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com/dziennik_baza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
