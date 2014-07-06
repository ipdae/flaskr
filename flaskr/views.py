from __future__ import with_statement
from flask import Flask, request, session, redirect, url_for, abort
from flask import render_template, flash

app = Flask(__name__)
app.config.from_object('config')

from flaskr.database import db_session
from flaskr.models import Login, Entry, Comment, FacebookLogin
from flask.ext.mail import Mail
from rq import Queue
from worker import conn
from utils import count_words_at_url
from flask_oauthlib.client import OAuth

oauth = OAuth(app)
mail = Mail(app)
q = Queue(connection=conn)
facebook = oauth.remote_app('facebook',
                            app_key='FACEBOOK')

github = oauth.remote_app('github',
                          app_key='GITHUB')

google = oauth.remote_app('google',
                          app_key='GOOGLE')

oauth.init_app(app)


@app.route('/')
def show_list():
    if 'logged_in' in session:
        cur = db_session.query(Entry)
        List = [dict(id=entry.id, title=entry.title) for entry in cur]
        session['logged_in'] = True
        return render_template('show_list.html', List=List)
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = db_session.query(Login).filter(Login.username ==
                                             request.form['username'],
                                             Login.password ==
                                             request.form['password']).all()
        if len(cur) == 0:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
        return redirect(url_for('show_list'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        flash('You were logout')
    else:
        flash('You must login first')
    return redirect(url_for('show_list'))


@app.route('/fb_login')
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next')
                                               or request.referrer
                                               or None, _external=True))


@app.route('/fb_login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'], request.args['error_description'])
    session['facebook_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    cur = db_session.query(FacebookLogin).filter(
        FacebookLogin.email == me.data['email']).all()
    if len(cur) != 0:
        session['logged_in'] = True
        flash('Facebook Logged in as email %s' % me.data['email'])
    else:
        flash('please check your email address')
    return redirect(url_for('show_list'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')


@app.route('/git_login')
def github_login():
    return github.authorize(callback=url_for('github_authorized',
                                             _external=True))


@app.route('/git_login/authorized')
@github.authorized_handler
def github_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'], request.args['error_description'])
    session['github_token'] = (resp['access_token'], '')
    session['logged_in'] = True
    me = github.get('user')
    flash('Github logged in as id %s' % me.data['login'])
    return redirect(url_for('show_list'))


@github.tokengetter
def get_oauth_token():
    return session.get('github_token')


@app.route('/gg_login')
def google_login():
    return google.authorize(callback=url_for('google_authorized',
                                             _external=True))


@app.route('/gg_login/authorized')
@google.authorized_handler
def google_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'], request.args['error_description'])
    session['google_token'] = (resp['access_token'], '')
    session['logged_in'] = True
    me = google.get('userinfo', token=session['google_token'])
    flash('Google Logged in as email %s' % me.data['email'])
    return redirect(url_for('show_list'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/entry')
def show_entry():
    entry = db_session.query(Entry).\
        filter(Entry.id == request.args['id']).\
        one()
    comments = db_session.query(Comment).\
        filter(Comment.id2 == request.args['id']).\
        all()
    return render_template('show_entry.html', entry=entry, comments=comments)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entry = Entry(request.form['title'], request.form['text'],
                  request.form['pw'])
    db_session.add(entry)
    db_session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_list'))


@app.route('/edit', methods=['POST'])
def edit_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = db_session.query(Entry).\
        filter(Entry.id == request.args['id']).\
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
def del_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = db_session.query(Entry).\
        filter(Entry.id == request.args['id']).\
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
    comments = Comment(request.args['id'], request.form['author'],
                       request.form['comment'],
                       request.form['addCommentPassword'])
    db_session.add(comments)
    db_session.commit()
    flash('New comment was successfully posted')
    return redirect(url_for('show_entry', id=request.args['id']))


@app.route('/delComment', methods=['POST'])
def del_comment():
    password = request.form.get("delCommentPassword")
    cur = db_session.query(Comment).\
        filter(Comment.id == request.args['id2'],
               Comment.id2 == request.args['id']).\
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
    q.enqueue(count_words_at_url, 'http://heroku.com',
              str(request.form['mailAddress']))
    flash('check your e-mail')
    return redirect(url_for('show_list'))
