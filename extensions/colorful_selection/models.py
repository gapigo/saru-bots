from flask_app import db
from datetime import datetime

"""
{'selection': '```css\n[ Mensagem exemplo ]\n```',
 'config': {'error': '', 'private': True, 'delete': True,
            'name': 'laranja', 'color': 'o', 'message': 'Mensagem exemplo'}, 
  'user': '325384616221474818'}
"""

class ColorfulSelection(db.Model):
    __tablename__ = "colorful_selection"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    name = db.Column(db.String(200), unique=True, nullable=False)
    selection = db.Column(db.String(1999), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(1999), nullable=False)
    user = db.Column(db.String(20), nullable=True)
    private = db.Column(db.Boolean, default=False, nullable=False)
    delete = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name, selection, color, message, user, private=False, delete=False):
        # types: undefined, aggressive, cheerful, funny, sad, nosense, annoying
        self.created_at = datetime.now()
        self.name = name
        self.selection = selection
        self.color = color
        self.message = message
        self.user = user
        self.private = private
        self.delete = delete
