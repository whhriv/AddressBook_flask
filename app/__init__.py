from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from datetime import datetime
from flask_login import LoginManager





app = Flask(__name__)
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"

login = LoginManager()
login.login_view = 'login' 
login.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.create_all()


from app.blueprints.api import api
app.register_blueprint(api)

from . import routes, models, forms