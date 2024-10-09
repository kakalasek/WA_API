from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    create_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    text = db.Column(db.Text, nullable=False)
