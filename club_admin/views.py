from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from club.models import Club
from club_admin.def_common import merge_dict, generate_club_admin_token
from club_admin.models import ClubAdmin


def admin_data(request):
    admin = request.admin
    clubs = Club.objects.all()

    data = {
        'admin': admin,
        'clubs': clubs,
    }
    return data


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'club_admin/login.html')
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    temp = False
    admin = ClubAdmin.objects.filter(username=username).first()
    if admin:
        temp = True
    if temp and check_password(password, admin.password):
        token = generate_club_admin_token()
        admin.token = token
        admin.save()
        response = redirect(reverse('club_admin:index'))
        response.set_cookie('token', token)
        return response
    else:
        data = {
            'login_error': True,
            'login_error_message': '用户名/密码错误',
        }
        data = merge_dict(data, admin_data(request))
        return render(request, 'club_admin/login.html', context=data)


# 登出
def logout(request):
    response = redirect(reverse('club_admin:index'))
    response.delete_cookie('token')
    admin = request.admin
    admin.token = generate_club_admin_token()
    admin.save()
    return response


# 修改密码
def edit(request):
    if not request.admin:
        return redirect(reverse('club_admin:login'))
    if request.method == 'GET':
        data = admin_data(request)
        return render(request, 'club_admin/edit.html', context=data)
    data = {
        'edit_success': True,
        'edit_success_message': '密码更改成功',
        'edit_error': False,
    }
    data = merge_dict(data, admin_data(request))
    password = request.POST.get('password', None)
    re_password = request.POST.get('re_password', None)
    if not password == re_password:
        data.update(edit_error=True, edit_success=False, edit_error_message='两次输入密码不一致，更改失败')
    else:
        admin = request.admin
        admin.password = make_password(password)
        admin.save()
    return render(request, 'club_admin/edit.html', context=data)


# 首页
def index(request):
    if not request.admin:
        return redirect(reverse('club_admin:login'))
    data = admin_data(request)
    return render(request, 'club_admin/index.html', context=data)


# 新建社团
def add_club(request):
    if not request.admin:
        return redirect(reverse('club_admin:login'))
    if request.method == 'GET':
        data = admin_data(request)
        return render(request, 'club_admin/add_club.html', context=data)
    club_name = request.POST.get('club_name', None)
    temp = True
    try:
        club = Club()
        club.name = club_name
        club.save()
    except Exception:
        temp = False
    data = {}
    if temp:
        data = {
            'add_club_success': True,
            'add_club_success_message': '添加社团-%s成功' % club_name
        }
    else:
        data = {
            'add_club_error': True,
            'add_club_error_message': '已经存在社团-%s，添加失败' % club_name
        }
    data = merge_dict(data, admin_data(request))
    return render(request, 'club_admin/add_club.html', context=data)


# 编辑社团
def edit_club(request):
    if not request.admin:
        return redirect(reverse('club_admin:login'))
    if request.method == 'GET':
        data = admin_data(request)
        return render(request, 'club_admin/edit_club.html', context=data)
    return render(request, '404.html', status=404)


# 删除社团
def delete_club(request, club_id):
    if not request.admin:
        return redirect(reverse('club_admin:login'))
    data = admin_data(request)
    club = Club.objects.filter(pk=club_id).first()
    if club:
        Club.delete(club)
    return render(request, 'club_admin/edit_club.html', context=data)


# 编辑社团页面
def edit_club_page(request, club_id):
    if not request.admin:
        return redirect(reverse('club_admin:login'))

    data = {}
    club = Club.objects.filter(pk=club_id).first()
    if club:
        old_club_name = club.name
        data.update(club=club)
    else:
        return redirect(reverse('club_admin:edit_club'))
    data = merge_dict(data, admin_data(request))
    if request.method == 'GET':
        return render(request, 'club_admin/edit_club_page.html', context=data)

    club_name = request.POST.get('club_name')
    club_name = club_name.strip()
    if (club_name == '') or club_name == old_club_name:
        data.update(edit_club_error=True, edit_club_error_message='社团名称未更改')
        return render(request, 'club_admin/edit_club_page.html', context=data)

    club.name = club_name
    club.save()
    data.update(edit_club_success=True, edit_club_success_message='更改社团-%s 为-%s 成功' % (old_club_name, club_name))
    return render(request, 'club_admin/edit_club_page.html', context=data)


# 添加社团成员
def add_club_member(request):
    if not request.admin:
        return redirect(reverse('club_admin:login'))
    if request.method == 'POST':
        club_id = request.POST.get('club_id', None)
        action = request.POST.get('action', None)
        club = Club.objects.filter(pk=club_id).first()
        if not club_id and club:
            return render(request, '404.html', status=404)
        if (not action) or action != 'add_member':
            data = {
                'club': club,
            }
            data = merge_dict(data, admin_data(request))
            return render(request, 'club_admin/add_club_member.html', context=data)
        if action == 'add_member':

            sid = request.POST.get('sid', None)
            name = request.POST.get('name', None)
            phone = request.POST.get('phone', None)
            qq = request.POST.get('qq', None)
            is_admin = request.POST.get('is_admin', None)
            if not is_admin:
                return render(request, '404.html', status=404)
            if sid:
                sid = sid.strip()
            if name:
                name = name.strip()
            if phone:
                phone = phone.strip()
            if qq:
                qq = phone.strip()

            # 是否存在学号为sid的社员，不存在则（注册），添加。如果存在，则更改社团信息
    return render(request, '404.html', status=404)

# 添加社团成员页面
# def add_club_member_page(request):
#     if request.method == 'POST':
#         pass
#     if request.method == 'GET':
#         pass
#
#     return render(request, '404.html', status=404)
