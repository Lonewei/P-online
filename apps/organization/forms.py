# _*_ coding: utf-8 _*_
import re

__author__ = 'onewei'
__date__ = '2017/2/17 17:44'
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 验证手机号格式
    # 必须以clean开头
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        mobile_matching = r"^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\d{8}$"
        # 预编译正则表达式，提高运行效率
        p = re.compile(mobile_matching)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"请填写正确的手机号", code="mobile_invalid")
