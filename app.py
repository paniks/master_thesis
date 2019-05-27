from flask import Flask, render_template

project = 'keystroke_dynamics'

app = Flask(__name__,  template_folder=f'web/{project}/view', static_folder=f'web/{project}/utils')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'


@app.route("/")
def keystroke_app():
    return render_template('welcome.html')


if __name__ == "__main__":
    app.debug = True
    app.run()