import django_heroku
from .defaults import *

# Configure Django App for Heroku.
django_heroku.settings(locals())
