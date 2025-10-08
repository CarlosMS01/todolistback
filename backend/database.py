# backend/database.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def init_app():
    load_dotenv()
    app = Flask(__name__)

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL no está definido en el entorno. Verifica tu archivo .env.")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    return app

