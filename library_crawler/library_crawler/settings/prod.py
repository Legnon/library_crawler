from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, "..", "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")

DATABASES = {
	'default': {
		'ENGINE': os.environ.get('DJANGO_DATABASE_ENGINE', 'django.db.backends.postgresql_psycopg2'),
		'NAME': os.environ.get('DJANGO_DATABASE_NAME', 'kong'),
		'USER': os.environ.get('DJANGO_DATABASE_USER', 'ubuntu'),
		'PASSWORD': os.environ.get('DJANGO_DATABASE_PASSWORD', 'konghyeontaek'),
		'HOST': os.environ.get('DJANGO_DATABASE_HOST', '127.0.0.1'),
	}
}
