from django.conf.urls import url

from club_admin import views

urlpatterns = [
    # 首页
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index),
    # 登录
    url(r'^login/$', views.login, name='login'),
    # 登出
    url(r'^logout/$', views.logout, name='logout'),
    # 修改admin
    url(r'^edit/$', views.edit, name='edit'),
    # 新建社团
    url(r'^add_club/$', views.add_club, name='add_club'),
    # 编辑社团
    url(r'^edit_club/$', views.edit_club, name='edit_club'),
    # 删除社团
    url(r'^delete/(?P<club_id>\d+)/$', views.delete_club, name='delete_club'),
    # 编辑社团页面
    url(r'^edit_club_page/(?P<club_id>\d+)/$', views.edit_club_page, name='edit_club_page'),
    # 添加社团成员
    url(r'^add_club_member/$', views.add_club_member, name='add_club_member'),
    # 添加社团成员页面
    # url(r'^add_club_member_page/$', views.add_club_member_page, name='add_club_member_page'),
]
