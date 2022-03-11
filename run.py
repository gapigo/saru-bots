import os
from bots import run_bots
from flask_app import app
from threading import Thread

def run_flask():
    app.run(host="0.0.0.0", port=8080, use_reloader=False)


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    Thread(target=run_flask).start()  # run flask
    run_bots()  # run discord
