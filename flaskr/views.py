from flaskr import app
from flaskr.database import db_session
from flaskr.models import Login, Entry, Comment
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from rq import Queue
from worker import conn
from utils import count_words_at_url
from flask.ext.mail import Mail, Message

mail = Mail(app)
q = Queue(connection=conn)

@app.route('/')
def show_list():
    cur = db_session.query(Entry)
    List = [dict(id = entry.id, title=entry.title) for entry in cur]
    return render_template('show_list.html', List=List)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = db_session.query(Login).filter(Login.username==request.form['username'], Login.password==request.form['password']).all()
        if len(cur) == 0:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
        return redirect(url_for('show_list'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_list'))

@app.route('/entry')
def show_entry():
    entry = db_session.query(Entry).\
            filter(Entry.id==request.args['id']).\
            one()
    comments = db_session.query(Comment).\
               filter(Comment.id2==request.args['id']).\
               all()
    return render_template('show_entry.html', entry=entry, comments=comments)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
        entry = Entry(request.form['title'], request.form['text'], request.form['pw'])
        db_session.add(entry)
        db_session.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_list'))

@app.route('/edit', methods=['POST'])
def edit_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = db_session.query(Entry).\
          filter(Entry.id==request.args['id']).\
          one()
    if request.form['entryPassword1'] == str(cur.password):
        cur.title = request.form['title']
        cur.text = request.form['text']
        db_session.commit()
        flash('Edit entry Success')
    else:
        flash('Invalid password')
    return redirect(url_for('show_entry', id=request.args['id']))

@app.route('/del', methods=['POST'])
def del_e():
    if not session.get('logged_in'):
        abort(401)
    cur = db_session.query(Entry).\
          filter(Entry.id==request.args['id']).\
          one()
    if request.form['entryPassword2'] == str(cur.password):
        db_session.delete(cur)
        db_session.commit()
        flash('Delete entry success')
    else:
        flash('Invalid password')
    return redirect(url_for('show_list'))

@app.route('/addComment', methods=['POST'])
def add_comment():
    comments = Comment(request.args['id'], request.form['author'], request.form['comment'], request.form['addCommentPassword'])
    db_session.add(comments)
    db_session.commit()
    flash('New comment was successfully posted')
    return redirect(url_for('show_entry', id=request.args['id']))

@app.route('/delComment', methods=['POST'])
def del_comment():
    password = request.form.get("delCommentPassword")
    cur = db_session.query(Comment).\
          filter(Comment.id==request.args['id2'], Comment.id2==request.args['id']).\
          one()
    if password != cur.password:
        flash('Invalid password')
    else:
        db_session.delete(cur)
        db_session.commit()
        flash('Delete comment success')
    return redirect(url_for('show_entry', id=request.args['id']))

@app.route('/worker', methods=['GET', 'POST'])
def worker():
    return render_template('send_mail.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    working = q.enqueue(count_words_at_url, 'http://heroku.com', str(request.form['mailAddress']))
    flash('check your e-mail')
    return redirect(url_for('show_list'))

