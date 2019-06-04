from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from club.def_common import merge_dict, verify_permission, get_member, generate_club_token
from club.models import Member, Club


def user_data(request):
    user = request.user
    clubs = Club.objects.all()

    data = {
        'user': user,
        'clubs': clubs,
    }
    return data


# 社员登录页面
def generate_password(args):
    pass


def login(request):
    if request.method == 'GET':
        try:
            HttpResponse.delete_cookie('token')
        except Exception:
            pass
        return render(request, 'club/login.html')

    sid = request.POST.get('sid', '') or ''
    password = request.POST.get('password', '') or ''
    user = Member.objects.filter(sid=sid).first()
    temp = False
    if user:
        user_password = user.password
        temp = check_password(password, user_password)
    if not (sid and password and user and temp):
        login_error = True
        login_error_message = '用户名/密码错误'
        data = {
            'login_error': login_error,
            'login_error_message': login_error_message,
        }
        data = merge_dict(data, user_data(request))
        return render(request, 'club/login.html', context=data)
    # 重新生成token
    token = generate_club_token()
    user.token = token
    user.save()

    response = redirect(reverse('club:index'))
    response.set_cookie('token', token)
    return response


# 系统首页
def index(request):
    if not request.user:
        return redirect(reverse('club:login'))
    data = user_data(request)
    return render(request, 'club/index.html', data)


# 显示加入的社团的详细信息
def show_join_club(request, join_club_id):
    if not request.user:
        return redirect(reverse('club:login'))
    join_club = Club.objects.filter(pk=join_club_id).first()

    if not join_club:
        return render(request, 'club/404.html', status=404)
    key_word = query(request)
    if key_word:
        join_club_admin1 = join_club.member_club.all().filter(admin=join_club_id).filter(sid__contains=key_word)
        join_club_admin2 = join_club.member_club.all().filter(admin=join_club_id).filter(name__contains=key_word)
        join_club_member1 = join_club.member_club.all().exclude(admin=join_club_id).filter(sid__contains=key_word)
        join_club_member2 = join_club.member_club.all().exclude(admin=join_club_id).filter(name__contains=key_word)
        join_club_admin = join_club_admin1 | join_club_admin2
        join_club_member = join_club_member1 | join_club_member2

    else:
        join_club_admin = join_club.member_club.all().filter(admin=join_club_id)
        join_club_member = join_club.member_club.all().exclude(admin=join_club_id)

    data = {
        'key': key_word,
        'join_club': join_club,
        'join_club_admin': join_club_admin,
        'join_club_member': join_club_member,
    }
    data = merge_dict(data, user_data(request))
    return render(request, 'club/join_list.html', context=data)


# 查看社团成员基本信息
def see_member(request, join_club_id, member_id):
    if not request.user:
        return redirect(reverse('club:login'))
    club_member = Member.objects.filter(pk=member_id).first()
    join_club = Club.objects.filter(pk=join_club_id).first()
    if not (club_member and join_club):
        return render(request, 'club/404.html', status=404)
    data = {
        'club_member': club_member,
        'join_club': join_club,
    }
    data = merge_dict(data, user_data(request))
    return render(request, 'club/see_member.html', context=data)


# 管理社团列表
def manage_club(request, club_id):
    if not request.user:
        return redirect(reverse('club:login'))
    manage_club = Club.objects.filter(pk=club_id).first()
    key_word = query(request)
    if key_word:
        manage_club_admin1 = manage_club.member_club.all().filter(admin=club_id).filter(sid__contains=key_word)
        manage_club_admin2 = manage_club.member_club.all().filter(admin=club_id).filter(name__contains=key_word)
        manage_club_member1 = manage_club.member_club.all().exclude(admin=club_id).filter(sid__contains=key_word)
        manage_club_member2 = manage_club.member_club.all().exclude(admin=club_id).filter(name__contains=key_word)
        manage_club_admin = manage_club_admin1 | manage_club_admin2
        manage_club_member = manage_club_member1 | manage_club_member2


    else:
        manage_club_admin = manage_club.member_club.all().filter(admin=club_id)
        manage_club_member = manage_club.member_club.all().exclude(admin=club_id)

    data = {
        'key': key_word,
        'manage_club': manage_club,
        'manage_club_admin': manage_club_admin,
        'manage_club_member': manage_club_member,
    }
    data = merge_dict(data, user_data(request))
    return render(request, 'club/manage_list.html', context=data)


# 查看社团管理员
def see_admin(request, join_club_id, member_id):
    if not request.user:
        return redirect(reverse('club:login'))
    manage_club = Club.objects.filter(pk=join_club_id).first()
    manage_admin = Member.objects.filter(pk=member_id).first()
    if not (manage_club and manage_admin):
        return render(request, 'club/404.html')
    data = {
        'manage_admin': manage_admin,
        'manage_club': manage_club,
    }
    data = merge_dict(data, user_data(request))
    return render(request, 'club/see_admin.html', context=data)


# 添加社员界面
def add(request):
    if not request.user:
        return redirect(reverse('club:login'))
    if request.method == 'POST':
        join_club_id = request.POST.get('club_id', None)
        member_id = request.POST.get('member_id', None)

        if not (join_club_id and member_id and verify_permission(join_club_id, member_id)):
            print(join_club_id)
            print(member_id)
            print(verify_permission(join_club_id, member_id))
            return render(request, 'club/404.html')
        club = Club.objects.filter(pk=join_club_id).first()
        data = {
            'manage_club': club,
        }
        data = merge_dict(data, user_data(request))
        return render(request, 'club/add_member.html', context=data)


# 执行添加社团
def exe_add(request):
    if not request.user:
        return redirect(reverse('club:login'))
    print(request.method)
    sid = request.POST.get('sid', None)
    name = request.POST.get('name', None)
    join_club_id = request.POST.get('club_id', None)
    member = get_member(sid=sid, name=name)
    club = Club.objects.filter(pk=join_club_id).first()

    member_id = request.user.id
    # 添加失败
    if not member:
        if not (join_club_id and member_id and verify_permission(join_club_id, member_id) and join_club_id):
            return render(request, 'club/404.html')
        add_fail = True
        add_fail_message = '学号/姓名填写不规范,请重新填写'
        data = {
            'manage_club': club,
            'add_fail': add_fail,
            'add_fail_message': add_fail_message,
        }
        data = merge_dict(data, user_data(request))
        return render(request, 'club/add_member.html', context=data)

    # 确认是否添加成功。
    try:
        member.club.add(join_club_id)
        member.save()
        temp = True
    except Exception:
        temp = False

    # 该社员已经加入了该社团
    if not temp:
        add_fail = True
        add_fail_message = '该成员已经加入过此社团，请勿重复操作'
        data = {
            'manage_club': club,
            'add_fail': add_fail,
            'add_fail_message': add_fail_message,
        }
        data = merge_dict(data, user_data(request))
        return render(request, 'club/add_member.html', context=data)

    # 添加成功
    add_success = True
    add_success_message = '添加社员' + member.name + '成功'
    data = {
        'manage_club': club,
        'add_success': add_success,
        'add_success_message': add_success_message,
    }
    # data = merge_dict(data, user_data(request))
    print(add_success)
    print(add_success_message)
    print(data)
    return render(request, 'club/add_member.html', context=data)


# 删除社团成员
def delete(request, club_id, member_id):
    if not request.user:
        return redirect(reverse('club:login'))
    join_club_id = club_id
    if not (verify_permission(join_club_id, request.user.id) and not verify_permission(join_club_id, member_id)):
        return render(request, 'club/404.html', status=404)
    club = Club.objects.filter(pk=join_club_id).first()
    member = Member.objects.filter(pk=member_id).first()
    club.member_club.remove(member)
    return redirect(reverse('club:manage_club', kwargs={'club_id': join_club_id}))


# 模糊查询
def query(request):
    key_word = request.POST.get('key_word', None)
    if key_word:
        key_word = key_word.strip()
    return key_word


# 所有社团
def all(request, club_id):
    if not request.user:
        return redirect(reverse('club:login'))
    club_show = Club.objects.all().filter(pk=club_id).first()
    if not club_show:
        return render(request, 'club/404.html', status=404)

    key_word = query(request)

    if key_word:
        club_admin1 = club_show.member_club.all().filter(admin=club_id).filter(sid__contains=key_word)
        club_admin2 = club_show.member_club.all().filter(admin=club_id).filter(name__contains=key_word)
        club_member1 = club_show.member_club.all().exclude(admin=club_id).filter(sid__contains=key_word)
        club_member2 = club_show.member_club.all().exclude(admin=club_id).filter(name__contains=key_word)
        club_admin = club_admin1 | club_admin2
        club_member = club_member1 | club_member2

    else:
        club_admin = club_show.member_club.all().filter(admin=club_id)
        club_member = club_show.member_club.all().exclude(admin=club_id)

    data = {
        'key': key_word,
        'club': club_show,
        'club_admin': club_admin,
        'club_member': club_member,
    }
    data = merge_dict(data, user_data(request))
    return render(request, 'club/all_list.html', context=data)


# 查询‘所有’ 社团成员信息
def see_all(request, join_club_id, member_id):
    if not request.user:
        return redirect(reverse('club:login'))
    club_member = Member.objects.filter(pk=member_id).first()
    join_club = Club.objects.filter(pk=join_club_id).first()
    if not (club_member and join_club):
        return render(request, 'club/404.html', status=404)
    data = {
        'club_member': club_member,
        'join_club': join_club,
    }
    data = merge_dict(data, user_data(request))
    return render(request, 'club/see_all.html', context=data)


# 退出登录
def logout(request):
    response = redirect(reverse('club:login'))
    response.delete_cookie('token')
    user = request.user
    # 重新生成token
    user.token = generate_club_token()
    user.save()
    return response


# 修改普通社员信息
def edit(request):
    if not request.user:
        return redirect(reverse('club:login'))
    if request.method == 'GET':
        data = user_data(request)
        return render(request, 'club/edit.html', context=data)
    data = user_data(request)
    data.update(
        edit_error=False,
        edit_success=False,
        edit_error_message='',
        edit_success_message='更改成功',
    )

    # 修改我的信息
    sid = request.POST.get('sid', None)
    name = request.POST.get('name', None)
    phone = request.POST.get('phone', None)
    qq = request.POST.get('qq', None)
    password = request.POST.get('password', None)
    re_password = request.POST.get('re_password', None)
    if not password == re_password:
        data.update(edit_error=True, edit_error_message='两次输入密码不一致')
        return render(request, 'club/edit.html', context=data)

    try:
        user = request.user
        member = Member.objects.filter(sid=sid).first()
        if member and member != user:
            data.update(edit_error=True, edit_error_message='已经存在社员学号为-%s 更改失败' % (sid))
            return render(request, 'club/edit.html', context=data)

        user.sid = sid
        user.name = name
        user.phone = phone
        user.qq = qq
        if password == re_password and password == '':
            user.save()
        elif password == re_password and password != '':
            user.password = make_password(password)
            user.save()
        else:
            data.update(edit_error=True, edit_error_message='发生未知错误，更改失败')
            return render(request, 'club/edit.html', context=data)
    except Exception:
        print('----------')
        data.update(edit_error=True, edit_error_message='发生未知错误，更改失败')
        return render(request, 'club/edit.html', context=data)

    data.update(edit_success=True, edit_success_message='更改成功')
    return render(request, 'club/edit.html', context=data)


def quit(request):
    if not request.user:
        return redirect(reverse('club:login'))
    data = user_data(request)
    return render(request, 'club/quit.html', context=data)


def exe_quit(request, club_id):
    if not request.user:
        return redirect(reverse('club:login'))
    user = request.user
    club = Club.objects.filter(pk=club_id).first()
    club.member_club.remove(user)
    club.member_admin.remove(user)
    return redirect(reverse('club:quit'))


# 注册
def register(request):

    if request.method == 'GET':
        return render(request, 'club/register.html')
    data = {'register_success': False, 'register_error': True, 'register_error_message': ''}
    sid = request.POST.get('sid', None)
    password = request.POST.get('password', None)
    re_password = request.POST.get('re_password', None)
    if not sid:
        data.update(register_error_message='请填写学号')
    elif Member.objects.filter(sid=sid).first():
        data.update(register_error_message='此学号已经被注册')
    elif not password:
        data.update(register_error_message='请填写密码')
    elif not password == re_password:
        data.update(register_error_message='两次填写密码不一致，请确认密码')
    else:
        data.update(register_error=False, register_success=True)
    try:
        member = Member()
        member.sid = sid
        member.password = make_password(password)
        member.save()
    except Exception:
        data.update(register_error=True, register_success=False, register_error_message='未知错误，注册失败')
    return render(request, 'club/register.html', context=data)
