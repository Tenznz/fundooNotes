from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
    }
}
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
