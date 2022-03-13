from flask_app import db
from datetime import datetime


class TongoMessage(db.Model):
    __tablename__ = "tongo_messages"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    message = db.Column(db.String(1999), unique=True, nullable=False)
    type = db.Column(db.String(16), nullable=True)

    def __init__(self, message, type="undefined"):
        # types: undefined, aggressive, cheerful, funny, sad, nosense, annoying
        self.message = message
        self.type = type
        self.created_at = datetime.now()

