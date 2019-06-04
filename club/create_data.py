import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from club.models import Member, Club


def create(request):
    club_list = ['美术社', '轮滑社', '舞蹈社', '篮球社', '文学社', '武术社', '街舞社', '书法社']
    for _ in club_list:
        try:
            club = Club()
            club.name = _
            club.save()
        except:
            pass

    club = Club.objects.all()
    club_num = club.__len__()

    for _ in range(10000000, 10000400):
        try:
            member = Member()
            member.sid = '2015' + str(_)
            member.name = '名字' + str(_)
            member.save()

            r = club[random.randint(0, club_num)].id
            member.club.add(r)
            y = club[random.randint(0, club_num)].id
            if r != y:
                member.club.add(y)

            if member.id % 10 < 3:
                member.admin.add(r)

            # per = random.randint(0, 10)
            # if per == 4:
            #     member.admin.add(r)
            # if per == 3 and r != y:
            #
            #     member.admin.add(r)
            #     member.admin.add(y)
            # member.save()
        except:
            pass

    return HttpResponse('添加完成')
