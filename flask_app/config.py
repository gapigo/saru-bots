import os
# basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_app/db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'edfdbf24-a409-4h5d-8da1-f01g6ad62c4a'
