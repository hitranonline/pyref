# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<<< SECRET_KEY >>>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADS_TOKEN = '<<< ADS_TOKEN >>>'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<<< DATABASE NAME >>>',
        'USER': '<<< DATABASE USER >>>',
        'PASSWORD': '<<< DATABASE USER PASSWORD >>>',
        'HOST': '',
        'PORT': '',
    }
}

