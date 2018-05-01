
from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    user_agent= request.headers.get('User-Agent')
    return '<p>your browser is %s</p>' % user_agent

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

@app.route('/input/main_form')
def goto_main_form():
    return '<h1>Main Form</h1>'

@app.route('/not_found')
def not_found():
    return '<h1>Not Found</h1>',400

@app.route('/return_response')
def ret_response():
    response = make_response('<h1>This Document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

@app.route('/google')
def goto_google():
    return redirect('https://www.google.com/')

@app.route('/abort')
def goto_abort():
    abort(404)
    return "Not Exist"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(505)
def internal_server_error(e):
    return render_template('505.html'),505

if __name__ == "__main__":
    app.run(debug=True)