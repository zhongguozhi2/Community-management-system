import uuid

from club_admin.con_common import CLUB_ADMIN_TOKEN_PREFIX


def merge_dict(dict1, dict2):
    return dict(dict1, **dict2)


def generate_token(prefix=''):
    return prefix + uuid.uuid4().hex


def generate_club_admin_token(prefix=CLUB_ADMIN_TOKEN_PREFIX):
    return generate_token(prefix=prefix)


def verify_token(token, prefix=''):
    try:
        if not token.startswith(prefix):
            return False
    except Exception:
        return False
    return True


def verify_club_admin_token(token, prefix=CLUB_ADMIN_TOKEN_PREFIX):
    return verify_token(token, prefix=prefix)


def verify_login(request):
    if not request.admin:
        return False
    return True
