import os
SECRET_KEY = 'devlopment key'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_SMTP_LOGIN', None)
MAIL_PASSWORD = os.environ.get('MAIL_SMTP_PASSWORD', None)
MAIL_DEFAULT_SENDER = 'qooraven@gmail.com'
FACEBOOK = dict(base_url='https://graph.facebook.com/',
                request_token_url=None,
                access_token_url='/oauth/access_token',
                authorize_url='https://www.facebook.com/dialog/oauth',
                consumer_key=os.environ.get('FACEBOOK_APP_ID'),
                consumer_secret=os.environ.get('FACEBOOK_APP_SECRET'),
                request_token_params={'scope': 'email'})
