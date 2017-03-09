# -*- coding: utf-8 -*-
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
# Create your views here.
from django.views.generic import View

from courses.models import Course
from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import CourseOrg, CityDict, Teacher


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 机构排名
        hot_orgs = all_orgs.order_by("click_num")[:3]
        # 城市
        all_citys = CityDict.objects.all()
        # 取出筛选城市ID
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'study':
                all_orgs = all_orgs.order_by('study_num')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('course_num')

        # 课程数量
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 4, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html",
                      {"all_orgs": orgs,
                       "all_citys": all_citys,
                       "org_nums": org_nums,
                       "city_id": city_id,
                       "category": category,
                       "hot_orgs": hot_orgs,
                       "sort": sort
                       })


class AddUserAskView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        # 页面标识
        course_page = "home"
        # 获取对应id的机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_typ=2):
                has_fav = True

        # 通过course_org 这个外键反向获得所有course值
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses, "all_teachers": all_teachers,
            "course_org": course_org,
            "course_page": course_page,
            "has_fav":has_fav
        }, )


class OrgCourseView(View):
    """
    机构课程页
    """

    def get(self, request, org_id):
        course_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_typ=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, "org-detail-course.html", {
            "all_courses": all_courses, "course_org": course_org,
            "course_page": course_page,
            "has_fav":has_fav
        }, )


class OrgDescView(View):
    """
    机构介绍页
    """

    def get(self, request, org_id):
        course_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_typ=2):
                has_fav = True
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "course_page": course_page,
            "has_fav":has_fav
        }, )


class OrgTeacherView(View):
    """
    讲师页
    """

    def get(self, request, org_id):
        course_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_typ=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "course_page": course_page,
            "has_fav":has_fav
        }, )


class AddFavView(View):
    """
    用户收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_typ=int(fav_type))
        if exist_records:
            # 若记录已存在，则取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"已取消收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite(user=request.user)
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_typ = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):
        all_teacher = Teacher.objects.all()
        return render(request, 'teachers-list.html', {
            "all_teacher": all_teacher,
        })