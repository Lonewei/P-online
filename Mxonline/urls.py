# -*- coding: utf-8 -*-
"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from Mxonline.settings import MEDIA_ROOT
from organization.views import OrgView

from users.views import LoginView, LogoutView, ActiveUserView, ResetView, ModifyPwdView, IndexView
from users.views import RegisterView, ForgetPwdView

# in root_url needn't /
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url('^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url('^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    # 课程机构url
    url(r'^org/', include("organization.urls", namespace="org")),
    # 课程列表页
    url(r'^course/', include("courses.urls", namespace="course")),
    # 上传文件访问处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    # 个人信息页面
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]

# 全局404页面配置,名称固定
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
