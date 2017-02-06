# _*_ coding: utf-8 _*_
import xadmin

__author__ = 'onewei'
__date__ = '2017/2/3 16:02'

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student']
    search_fields = ['name', 'desc', 'detail', 'degree', 'student']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', ]
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['lesson', 'name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
