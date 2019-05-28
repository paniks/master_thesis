import json
from flask import Flask, render_template, redirect, request

project = 'keystroke_dynamics'

app = Flask(__name__,  template_folder=f'web/{project}/view', static_folder=f'web/{project}/utils')


@app.route("/")
def index():
    return render_template('welcome.html')


@app.route("/save", methods=["POST", "GET"])
def save():
    data = request.form['strikes']
    json_list = json.loads(data)
    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
