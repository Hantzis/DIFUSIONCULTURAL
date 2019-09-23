from .base import *

DEBUG = False

ALLOWED_HOSTS = ['http://difusioncultural.umich.mx/','https://difusioncultural.umich.mx/']

try:
    from .local import *
except ImportError:
    pass
