from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
    }
}
AUTH_USER_MODEL = "user.User"
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
