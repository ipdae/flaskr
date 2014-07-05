from flask import current_app, request
from flask.ext.mail import Mail, Message
import requests
import os

def count_words_at_url(url, mailAddress):
    resp = requests.get(url)
    result = len(resp.text.split())
    mail = Mail(current_app)
    msg = Message("test", recipients=["qooraven@gmail.com"])
    msg.body = str(result)
    msg.add_recipient(str(mailAddress))
    mail.send(msg)
    return result
