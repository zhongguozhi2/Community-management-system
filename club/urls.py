from django.conf.urls import url

from club import views

urlpatterns = [
    # 主页面
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index),
    # 注册
    url(r'register/$', views.register, name='register'),
    # 登录页面
    url(r'^login/$', views.login, name='login'),
    # 加入的社团
    url(r'^join/(?P<join_club_id>\d+)/$', views.show_join_club, name='join_club'),
    # 查看社团成员信息
    url(r'^join/(?P<join_club_id>\d+)/(?P<member_id>\d+)/$', views.see_member, name='see_member'),
    # 查看管理的社团
    url(r'^manage/(?P<club_id>\d+)/$', views.manage_club, name='manage_club'),
    # 查看社团管理员信息
    url(r'^manage/(?P<join_club_id>\d+)/(?P<member_id>\d+)/$', views.see_admin, name='see_admin'),
    # 添加社团普通社员信息
    url(r'^manage/add/$', views.add, name='add'),
    # 执行添加社员
    url(r'^manage/exe_add/', views.exe_add, name='exe_add'),
    # 删除社团成员
    url(r'^manage/delete/(?P<club_id>\d+)/(?P<member_id>\d+)/', views.delete, name='delete'),
    # 所有社团
    url(r'^all/(?P<club_id>\d+)/$', views.all, name='all'),
    # 查看社团成员信息
    url(r'^all/(?P<join_club_id>\d+)/(?P<member_id>\d+)/$', views.see_all, name='see_all'),
    # 退出登录
    url(r'^logout/$', views.logout, name='logout'),
    # 编辑我的个人资料
    url(r'^edit/$', views.edit, name='edit'),
    # 退出社团页面
    url(r'^quit/$', views.quit, name='quit'),
    # 执行退出社团
    url(r'^quit/(?P<club_id>\d+)/$', views.exe_quit, name='exe_quit')
]
