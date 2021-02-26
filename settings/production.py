from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'n)ld0h^%9bwe(djz%mw@9#lzsr3n3h&p3y2(r6u_0d+zvdw*43')