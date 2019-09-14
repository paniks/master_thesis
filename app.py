import os
import json
import pandas as pd
from flask import Flask, render_template, redirect, request

from utils.keystroke_dynamics import log_values
from utils.path_utlis import project_root


project = 'keystroke_dynamics'

app = Flask(__name__,  template_folder=f'web/{project}/view', static_folder=f'web/{project}/utils')


@app.route("/")
def index():
    return render_template('welcome.html')


@app.route("/save", methods=["POST", "GET"])
def save():

    # get data
    response = request.form['strikes']
    data = pd.DataFrame(json.loads(response))

    # save data to json
    json_handler = open(os.path.join(project_root(), 'local_tmp', 'file.json'), 'r+')
    log_values(data, json_handler)

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
