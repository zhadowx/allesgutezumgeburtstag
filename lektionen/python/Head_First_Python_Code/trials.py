from flask import Flask, render_template, request, escape, session
from checker import check_logged_in


app = Flask(__name__)

app.secret_key = 'biberon'

@app.route('/login')
def do_login() -> str:
  user_pass = input('Input password: ')
  if user_pass == app.secret_key:
    session['logged_in'] = True
    return 'You are now logged in.'
  return 'Wrong password'
  do_login()  


@app.route('/logout')
def do_logout() -> str:
  session.pop('logged_in')
  return 'You are now logged out.'



@app.route('/status')
def check_status() -> str:
  if 'logged_in' in session:
    return 'You are logged in.'
  return 'You are NOT logged in.'


@app.route('/')
def hello() -> str:
  return 'Hello from the simple webapp.'

@app.route('/page1')
@check_logged_in
def page1() -> str:
  return 'This is page 1'


@app.route('/page2')
@check_logged_in
def page2() -> str:
  return 'This is page 2'


@app.route('/page3')
@check_logged_in
def page3() -> str:
  return 'This is page 3'


if __name__ == '__main__':
  app.run(debug=True)
