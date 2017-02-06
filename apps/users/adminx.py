# _*_ coding: utf-8 _*_
__author__ = 'onewei'
__date__ = '2017/2/3 0:43'

import xadmin
from  xadmin import views

from .models import EmailVerifyRecord, Banner


# 后台标题
class BaseSetting(object):
    enable_themes = True
    # 设置左侧导航栏为下拉菜单
    use_bootswatch = True


# 后台底标
class GlobalSetting(object):
    site_title = "后台管理系统"
    site_footer = "天唯在线学习网"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
