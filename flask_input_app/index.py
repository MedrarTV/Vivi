from flask import Flask, render_template, session, redirect, url_for, jsonify, request, Response
import json
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from input_form import InputForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vtrardem'
app.config['DEBUG'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


NAMES = ["abc", "abcd", "abcde", "abcdef"]


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(NAMES), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))



if __name__ == '__main__':
    manager.run()
