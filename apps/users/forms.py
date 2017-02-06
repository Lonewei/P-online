# _*_ coding: utf-8 _*_
__author__ = 'onewei'
__date__ = '2017/2/6 23:31'

from django import forms

class LoginForm(forms.Form):
    # 必须与html代码中 form表单的name相同
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)
