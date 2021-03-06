# _*_ coding: utf-8 _*_
from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentView, AddCommentView, VideoPlayView

__author__ = 'onewei'
__date__ = '2017/2/23 22:41'

from django.conf.urls import url, include

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name="course_comment"),
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
    url(r'^video/(?P<video_id>\d+)/$',VideoPlayView.as_view(), name="video_play"),

]
