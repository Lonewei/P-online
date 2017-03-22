# _*_ coding: utf-8 _*_
import xadmin

__author__ = 'onewei'
__date__ = '2017/2/3 16:02'

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'get_zj_num', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'student']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student']
    # 默认排序为点击数倒叙排列
    ordering = ['-click_num']

    # 设置只读字段
    readonly_fields = ['click_num']

    # 隐藏字段
    exclude = ['fav_nums']

    # 列表页中直接进行数据修改
    list_editable = ['degree', 'desc']

    # 页面定时刷新功能
    refresh_times = [3, 5]

    # 添加嵌套
    inlines = [LessonInline, CourseResourceInline]

    # 设置ueditor样式
    style_fields = {"detail": "ueditor"}
    import_excel = True

    # 对轮播课程进行过滤
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 保存课程时统计课程机构课程数
        obj = self.new_obj
        obj.save()
        if obj.coures_org is not None:
            coures_org = obj.coures_org
            coures_org.course_num = Course.objects.filter(coures_org=coures_org).count()
            coures_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student']
    search_fields = ['name', 'desc', 'detail', 'degree', 'student']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student']
    # 默认排序为点击数倒叙排列
    ordering = ['-click_num']

    # 设置只读字段
    readonly_fields = ['click_num']

    # 隐藏字段
    exclude = ['fav_nums']

    # 添加嵌套
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', ]
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
