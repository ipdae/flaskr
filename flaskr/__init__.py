from __future__ import with_statement
from contextlib import closing
import sqlite3
import pdb
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

import flaskr.views

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

@app.route('/del')
def del_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select id, password from entries where id=?', [request.args['id']])
    result = cur.fetchall()
    if request.form['entryPassword2'] == str(result[0][1]):        
        g.db.execute('delete from entries where id = ?', [request.args['id']])
        g.db.commit()
        flash('Delete entry success')
    else:
        flash('Invalid password')
    return redirect(url_for('show_list'))


