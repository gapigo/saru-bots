from flask_app import app

@app.route('/')
def home():
	return "Hello. I am alive!"
