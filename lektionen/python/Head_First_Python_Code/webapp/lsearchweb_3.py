from flask import Flask, render_template, request, escape
from lsearch import search_for_letters
import mysql.connector

app = Flask (__name__)

def log_request(req: 'flask_request', res: str) -> None:
  """Log details of the web request and the results."""

  dbconfig = { 'host': '127.0.0.1',
               'user': 'lsearch',
               'password': '1234567',
               'database': 'lsearchlogDB', }

  conn = mysql.connector.connect(**dbconfig)
  cursor = conn.cursor()

  _SQL = """insert into log
             (phrase, letters, ip, browser_string, results)
             values
             (%s, %s, %s, %s, %s)"""

  cursor.execute(_SQL, (req.form['phrase'],
                        req.form['letters'],
                        req.remote_addr,
                        req.user_agent.browser,
                        res, ))

  conn.commit()
  cursor.close()
  conn.close()


@app.route('/search_for', methods=['POST'])
def do_search() -> 'html':
  phrase = request.form['phrase']
  letters = request.form['letters']
  results = str(sorted(search_for_letters(phrase, letters)))
  title = 'Here are your results'
  log_request(request, results)
  return render_template('results.html', 
                         the_title=title, 
                         the_phrase=phrase, 
                         the_letters=letters, 
                         the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
  return render_template('entry.html', 
                         the_title = "Welcome to search for letters")


@app.route('/viewlog')
def view_log() -> 'html':
  contents = []
  with open('lsearch.log') as log:
    for line in log:
      contents.append([])
      for item in line.split('|'):
        contents[-1].append(escape(item))
  titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
  return render_template('viewlog.html', 
                         the_title='View Log', 
                         the_row_titles=titles, 
                         the_data=contents)


if __name__=='__main__':
  app.run(debug=True)
