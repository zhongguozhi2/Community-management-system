from django.utils.deprecation import MiddlewareMixin

from club.def_common import verify_club_token
from club.models import Member


class verify_login(MiddlewareMixin):
    def process_request(self, request):
        path_info = request.META.get('PATH_INFO', None)
        if not path_info:
            pass
        if path_info == '/' or path_info.startswith('/club'):
            token = request.COOKIES.get('token') or None
            club_member = Member.objects.filter(token=token).first()

            if verify_club_token(token=token) and club_member:
                request.user = club_member
            else:
                request.user = None

        request.user = Member.objects.first()
