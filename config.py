import os
SECRET_KEY = 'devlopment key'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_SMTP_LOGIN', None)
MAIL_PASSWORD = os.environ.get('MAIL_SMTP_PASSWORD', None)
MAIL_DEFAULT_SENDER = 'qooraven@gmail.com'
GOOGLE = dict(consumer_key='353184524484-crdgp30oquu434rog5utk54ekfjif231.apps.googleusercontent.com',
              consumer_secret='VvxTR4_X6B0I-cQ7yFruut4Q',
              request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email'},
              base_url='https://www.googleapis.com/oauth2/v1/',
              request_token_url=None,
              access_token_method='POST',
              access_token_url='https://accounts.google.com/o/oauth2/token',
              authorize_url='https://accounts.google.com/o/oauth2/auth'
)
GITHUB = dict(consumer_key='592f084f3b8289856708',
              consumer_secret='164876d382ac5b4514c23e4454102028606ef7f0',
              request_token_params={'scope': 'user:email'},
              base_url='https://api.github.com/',
              request_token_url=None,
              access_token_method='POST',
              access_token_url='https://github.com/login/oauth/access_token',
              authorize_url='https://github.com/login/oauth/authorize'
)
FACEBOOK = dict(base_url='https://graph.facebook.com/',
                request_token_url=None,
                access_token_url='/oauth/access_token',
                authorize_url='https://www.facebook.com/dialog/oauth',
                consumer_key=os.environ.get('FACEBOOK_APP_ID'),
                consumer_secret=os.environ.get('FACEBOOK_APP_SECRET'),
                request_token_params={'scope': 'email'})

