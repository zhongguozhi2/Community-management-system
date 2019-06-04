from django.utils.deprecation import MiddlewareMixin

from club.def_common import verify_club_token
from club.models import Member
from club_admin.def_common import verify_club_admin_token
from club_admin.models import ClubAdmin


class verify_login(MiddlewareMixin):
    def process_request(self, request):
        path_info = request.META.get('PATH_INFO', None)
        if not path_info:
            pass
        if path_info.startswith('/club_admin'):
            token = request.COOKIES.get('token') or None
            club_admin = ClubAdmin.objects.filter(token=token).first()

            if verify_club_admin_token(token=token) and club_admin:
                request.admin = club_admin
            else:
                request.admin = None

        # request.admin = ClubAdmin.objects.first()
