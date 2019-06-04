import uuid

from club.con_common import CLUB_TOKEN_PREFIX, SUPER_ADMIN_TOKEN_PREFIX
from club.models import Member, Club


def generate_token(prefix=''):
    return prefix + uuid.uuid4().hex


def generate_club_token(prefix=CLUB_TOKEN_PREFIX):
    return generate_token(prefix=prefix)


def generate_super_admin_token(prefix=SUPER_ADMIN_TOKEN_PREFIX):
    return generate_token(prefix=prefix)


def verify_token(token, prefix=''):
    try:
        if not token.startswith(prefix):
            return False
    except Exception:
        return False
    return True


def verify_club_token(token, prefix=CLUB_TOKEN_PREFIX):
    return verify_token(token, prefix=prefix)


def verify_super_admin_token(token, prefix=SUPER_ADMIN_TOKEN_PREFIX):
    return verify_token(token, prefix=prefix)


def merge_dict(dict1, dict2):
    return dict(dict1, **dict2)


def verify_login(request):
    if not request.user:
        return False
    return True


# 验证社团成员是否有添加，删除 普通社员权限
def verify_permission(club_id, member_id):
    member = Member.objects.filter(pk=member_id).first()
    member_club_admin = member.admin.all()
    club = Club.objects.filter(pk=club_id).first()
    if club in member_club_admin:
        return True
    return False


# 社团添加社员前,执行检查该社员是否已经注册该系统,没有则自动注册
def get_member(**kwargs):
    sid = kwargs.get('sid', None)
    name = kwargs.get('name', None)

    if not (sid and name):
        return False
    member = Member.objects.filter(sid=sid).first()
    if not member:
        try:
            member = Member()
            member.sid = sid
            member.name = name
            member.save()
        except Exception:
            return False
    return member
