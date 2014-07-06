from sqlalchemy import Column, Integer, String
from flaskr.database import Base


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    text = Column(String(120))
    password = Column(Integer)
    etc = Column(String(255))

    def __init__(self, title, text, password):
        self.title = title
        self.text = text
        self.password = password


class Login(Base):
    __tablename__ = 'logins'
    id = Column(Integer, primary_key=True)
    username = Column(String(80))
    password = Column(String(120))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Login %r>' % (self.username)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    id2 = Column(Integer)
    author = Column(String(50), unique=True)
    comment = Column(String(120), unique=True)
    password = Column(String(80))

    def __init__(self, id2=None, author=None, comment=None, password=None):
        self.id2 = id2
        self.author = author
        self.comment = comment
        self.password = password


class FacebookLogin(Base):
    __tablename__ = 'facebooklogins'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)

    def __init__(self, email=None):
        self.email = email
