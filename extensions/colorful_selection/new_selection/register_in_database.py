# from replit import db
import os
from flask_app import db
from ..models import ColorfulSelection
from sqlalchemy.exc import IntegrityError, OperationalError

"""
{'selection': '```css\n[ Mensagem exemplo ]\n```',
 'config': {'error': '', 'private': True, 'delete': True,
            'name': 'laranja', 'color': 'o', 'message': 'Mensagem exemplo'}, 
  'user': '325384616221474818'}
"""


def register_in_database(data):
    #db.create_all()     # Create tables if doesn't exist
    # IF database exists
    # if "colorful_selections" in db.keys():
    #     if selection_name_exists(data['config']['name']):
    #         return False
    #     colorful_selections = db["colorful_selections"]
    #     colorful_selections.append(data)
    #     db["colorful_selections"] = colorful_selections
    # # IF database doesn't exist
    # else:
    #     db["colorful_selections"] = [data]
    #     db.create_all()
    tries: int = 0
    while True:
        db.session.rollback()
        try:
            i = ColorfulSelection(data['config']['name'], 
                                data['selection'], 
                                data['config']['color'], 
                                data['config']['message'], 
                                data['user'], 
                                data['config']['private'], 
                                data['config']['delete'])
            db.session.add(i)
            db.session.commit()
            #print("Nobo cor cororido corocado.")
            return True
        except IntegrityError:
            #print("Ja ejisute esuta coru, non ho adisionaru.")
            return False
        except OperationalError:
            if tries < 1:
                db.create_all()
                # db.migrate()
                # os.system('python flask_run.py db migrate')
                # os.system('python flask_run.py db upgrade')
                #db.session.rollback()
                #db.session.remove()
                tries += 1
            else:
                return False


def selection_name_exists(name):
    for selection in db['colorful_selections']:
        if selection['config']['name'] == name:
            return True
    return False
