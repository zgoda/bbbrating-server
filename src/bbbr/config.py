import os

SECRET_KEY = os.environ['SECRET_KEY']
JWT_TOKEN_LOCATION = ['headers', 'cookies']
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
