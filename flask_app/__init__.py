from flask import Flask
import os
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = Flask('__name__')
app.use_reloader=False
app.config.from_object('flask_app.config')
db = SQLAlchemy(app)

MIGRATION_DIR = os.path.join('flask_app', 'migrations')
migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from extensions.random_messages_tongo import models
from flask_app.controllers import default


def run():
	app.run(host="0.0.0.0", port=8080, use_reloader=False)


def start_flask():
	t = Thread(target=run)
	t.start()
