from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select id, title, text from entries order by id desc')
    entries = [dict(id = row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/del')
def del_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('delete from entries where id = ?', [request.args['id']])
    g.db.commit()
    flash('Delete entry success')
    return redirect(url_for('show_entries'))

@app.route('/edit', methods=['POST'])
def edit_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('update entries set title=?, text=? where id=?', [request.form['title'], request.form['text'], request.args['id']])
    g.db.commit()
    flash('Edit Sucess')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from logins where username = ?', [request.form['username']])
        result = cur.fetchall()
        if len(result) == 0:
            error = 'Invalid username'
        else:
            password = result[0][1]
            if request.form['password'] != password:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.debug = True
    app.run()
