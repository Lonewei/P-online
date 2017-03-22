# _*_ coding: utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite, CourseComments, UserCourse
from .models import Course, CourseResource, Video
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class CourseListView(View):
    """
    课程列表
    """

    def get(self, request):
        # -add_time 为降序排序
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_num")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # icontains 忽略大小写
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'student':
                all_courses = all_courses.order_by("-student")
            elif sort == 'hot':
                all_courses = all_courses.order_by("-click_num")

        # 课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses

        })


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        courses = Course.objects.get(id=int(course_id))

        # 课程点击数
        courses.click_num += 1
        courses.save()

        # 课程收藏
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=courses.id, fav_typ=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=courses.coures_org.id, fav_typ=2):
                has_fav_org = True

        # 课程标签
        tag = courses.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "courses": courses,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 课程点击数
        course.student += 1
        course.save()

        # 查询用户是否已关联课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        # 列表生成式 [x * x for x in range(1, 11)]
        # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        user_id = [user_course.user.id for user_course in user_courses]

        user_courses = UserCourse.objects.filter(course=course)
        all_resources = CourseResource.objects.filter(course=course)
        all_user_courses = UserCourse.objects.filter(user_id__in=user_id)
        # 获取所有课程ID
        course_id = [user_course.course.id for user_course in user_courses]
        # 获取用户学过的所有课程
        relate_courses = Course.objects.filter(id__in=course_id).order_by('-click_num')[:5]
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })


class CommentView(LoginRequiredMixin, View):
    """
    课程评论
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        # 获取用户学过的所有课程
        relate_courses = Course.objects.filter(id__in=course_id).order_by('-click_num')[:5]
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
            "relate_courses": relate_courses
        })


class AddCommentView(View):
    """
    用户评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            # 当前用户
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


class VideoPlayView(View):
    """
    视频播放
    """

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否已关联课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        # 列表生成式 [x * x for x in range(1, 11)]
        # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        user_id = [user_course.user.id for user_course in user_courses]

        user_courses = UserCourse.objects.filter(course=course)
        all_resources = CourseResource.objects.filter(course=course)
        all_user_courses = UserCourse.objects.filter(user_id__in=user_id)
        # 获取所有课程ID
        course_id = [user_course.course.id for user_course in user_courses]
        # 获取用户学过的所有课程
        relate_courses = Course.objects.filter(id__in=course_id).order_by('-click_num')[:5]
        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video
        })
