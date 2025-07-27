from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running on Render"

def run():
    app.run(host="0.0.0.0", port=8090)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()
