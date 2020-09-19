from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://test_3:test_3@localhost/test_3?auth_plugin=mysql_native_password"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False # Autocommit
    SQLALCHEMY_TRACK_MODIFICATIONS = False # ??? Если не прописать, то будет Warning
    SECRET_KEY = 'we4fh%gC_za:*8G5v=fbv'

app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app=app, session_options={'autoflush': False})

client = app.test_client()
