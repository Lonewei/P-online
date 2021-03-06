# _*_ coding: utf-8 _*_

__author__ = 'onewei'
__date__ = '2017/2/9 19:27'

from users.models import EmailVerifyRecord
from Mxonline.settings import EMAIL_FROM
from django.core.mail import send_mail
from random import Random
import string


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "天唯在线学习网激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "天唯在线学习网密码重置"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)

    elif send_type == "update_email":
        email_title = "天唯在线学习网修改邮箱"
        email_body = "验证码为：{0}".format(code)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass


# 生产随机字符串
def random_str(random_length=8):
    str = ''
    chars = string.letters + string.digits
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        # random.randint(a,b)
        str += chars[random.randint(0, length)]
    return str
