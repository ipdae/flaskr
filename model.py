from sqlalchemy import Column, Integer, String
from model.database import Base

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text = db.Column(db.String(120))
    password = db.Column(db.Integer)

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def by_id(cls, titleId):
        return db.query(cls).filter(cls.id==titleId).first()

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
    
    @classmethod
    def by_id(cls, userid):
        return db.query(cls).filter(cls.id==userid).first()

    @classmethod
    def by_username(cls, name):
        return db.query(cls).filter(cls.name==name).first()

def init_db(app):
    db.init_app(app)
    return app 
