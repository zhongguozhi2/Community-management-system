from django.contrib.auth.hashers import make_password

ORDINARY_USER = 1
ADMIN_USER = 2
SUPER_ADMIN_USER = 4

COOKIE_SALT = 'fdsagtreqgreg'
MEMBER_DEFAULT_PASSWORD = make_password('000000')

CLUB_TOKEN_PREFIX = 'club'
SUPER_ADMIN_TOKEN_PREFIX = 'sa'

MEMBER_ID = '201510000040'
