from flask import Flask
from threading import Thread
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.use_reloader=False
app.config.from_object('flask_app.config')
db = SQLAlchemy(app)

def run():
	app.run(host="0.0.0.0", port=8080, use_reloader=False)

def start_flask():
	t = Thread(target=run)
	t.start()


from flask_app.controllers import default
from flask_app.models import tables
