from flask import Flask
from config import Config
from models import db
from api import api, jwt

app = Flask(__name__)

app.config.from_object(Config)

from views.auth import auth
from views.dash import dash

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(dash, url_prefix='/')

with app.app_context():
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    db.create_all()

if __name__ == "__main__":
    app.run()