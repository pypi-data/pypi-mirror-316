from datetime import datetime, UTC

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
