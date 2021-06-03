from flask import Flask

app = Flask(__name__)

@app.route("/api/status")
def hello_world():
    return "!23"
