# _*_ coding: utf-8 _*_
import xadmin

__author__ = 'onewei'
__date__ = '2017/2/3 16:28'

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_num']
    search_fields = ['name', 'desc', 'click_num', 'fav_num']
    list_filter = ['name', 'desc', 'click_num', 'fav_num']
    # 更改为ajax 只有进行课程机构搜索时才会加载数据
    # 避免对数据库大量请求
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company']
    search_fields = ['org', 'name', 'work_year', 'work_company']
    list_filter = ['org', 'name', 'work_year', 'work_company']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
