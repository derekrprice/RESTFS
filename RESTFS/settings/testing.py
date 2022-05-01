import dj_database_url
from .defaults import *

DEBUG = True

SECRET_KEY = 'd80d9d6084e28fea49c4484b2288abbc861feeafba7e9c3e0a917a40679f0eca13d86db9a2d6a5b3863533e0da332a73c42f9d0fdb7f0d48cce2bddfcc6339dd204eb13ec16fa52fdfa2aac4635acd258a352f029bc9dd7f2d4449a542b181d292bfedb7'

DATABASES = {
    'default': {
        'TEST': {
            'NAME': 'da9hr9aavnh95b',
        },
    },
}
heroku_test_db = dj_database_url.config(default='postgres://jmukcvysqyyfkq:2db414d02e08782baccd77001027583a18edde5c1694b10ab4cdae21aa4fef74@ec2-3-217-113-25.compute-1.amazonaws.com:5432/da9hr9aavnh95b')
DATABASES['default'].update(heroku_test_db)