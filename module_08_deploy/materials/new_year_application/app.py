import os
from flask import Flask, render_template, send_from_directory

static_folder = "static"
root_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(root_dir, "templates")
static_directory = os.path.join(root_dir, "static")

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<path:filename>")
def send_static(filename):
    return send_from_directory(static_directory, filename)


if __name__ == "__main__":
    app.run()

