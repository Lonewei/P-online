# _*_ coding: utf-8 _*_
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__author__ = 'onewei'
__date__ = '2017/2/26 0:35'


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
