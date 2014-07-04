import os

SECRET_KEY = 'devlopment key'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_SMTP_LOGIN', None)
MAIL_PASSWORD = os.environ.get('MAIL_SMTP_PASSWORD', None)
MAIL_DEFAULT_SENDER = 'qooraven@gmail.com'
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
