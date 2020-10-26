"""students views"""
import json
import re
from datetime import datetime, timedelta
from random import choice
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from room_operation.views import RoomQueue
from backend.settings import REGEX_MOBILE, API_KEY
from backend.utils import YunPian
from .models import Student, VerifyCode


def signup(request):
    """the function of students signup"""
    if request.method == 'POST':
        student_id = request.POST.get('username')
        password = request.POST.get('password')
        telephone = request.POST.get('telephone')
        code = request.POST.get('code')
        data = validate_code(telephone, code)
        if data['code'] == "0000":
            try:
                with transaction.atomic():
                    try:
                        user = User.objects.create_user(username=student_id, password=password)
                    except Exception:
                        data = {'code': '0002', 'msg': '学号输入错误，请重新输入'}
                        return HttpResponse(json.dumps(data))
                    student = Student(user=user, telephone=telephone)
                    student.save()
                    data = {'code': '0000', 'msg': '注册成功'}
            except Exception:
                data = {'code': '0001', 'msg': '手机号输入错误，请重新输入'}
        return HttpResponse(json.dumps(data))
    return None


def change_password(request):
    """the function of students change_password"""
    user_id = request.POST.get('user_id')
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    user = User.objects.get(id=user_id)
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        data = {'code': '0000', 'msg': '修改密码成功'}
    else:
        data = {'code': '0003', 'msg': '原密码错误'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def change_name(request):
    """the function of students change_name"""
    name = request.POST.get('name')
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    student = Student.objects.get(user=user)
    student.real_name = name
    student.save()
    data = {'code': '0000', 'msg': '修改名字成功'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def change_email(request):
    """the function of student change email"""
    email = request.POST.get('email')
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    user.email = email
    user.save()
    data = {'code': '0000', 'msg': '修改邮箱成功'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_real_name(request):
    """the function of student's real name"""
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    student = Student.objects.get(user=user)
    name = student.real_name
    data = {'code': '0000', 'msg': '获取姓名成功', 'name': name}
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_email(request):
    """the function of student's email"""
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    email = user.email
    data = {'code': '0000', 'msg': '获取邮箱成功', 'email': email}
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_id(request):
    """the function of student's id"""
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    stu_id = user.username
    data = {'code': '0000', 'msg': '获取学号成功', 'stuId': stu_id}
    return HttpResponse(json.dumps(data), content_type="application/json")


class StudentBackend(ModelBackend):
    """students sign_in authenticate token"""
    def authenticate(self, request, username=None, password=None):
        username = username.strip()
        password = password.strip()
        student = Student.objects.filter(telephone=username)
        if len(student) == 1:
            if student[0].user.check_password(password):
                return student[0].user
        else:
            user = User.objects.filter(email=username)
            if len(user) == 1:
                if user[0].check_password(password):
                    return user[0]
            else:
                return None
        return None


def apply_to_ask(request):
    """the function of student apply_to_ask"""
    user_id = int(request.POST.get('user_id'))
    room_id = int(request.POST.get('room_id'))
    user = User.objects.get(id=user_id)
    current_deque = RoomQueue.ask_dict[room_id]
    order = current_deque.len
    dict1 = {order:user.username}
    current_deque.append(dict1)
    RoomQueue.dict[room_id] = current_deque
    return HttpResponse(json.dumps({'code': '0000', 'msg': '申请上台成功，敬请等待！'}))


def validate_mobile(mobile):
    """the function of validating mobile"""
    if Student.objects.filter(telephone=mobile).count():
        data = {'code': '0001', 'msg': '手机号已经注册！'}
    elif not re.match(REGEX_MOBILE, mobile):
        data = {'code': '0002', 'msg': '手机号非法!'}
    else:
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if  VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            data = {'code': '0003', 'msg': '距离上一次发送未超过60秒!'}
        else:
            data = {'code': '0000', 'msg': '手机号验证通过'}
    return data


def send_code(request):
    """the function of sending code"""
    mobile = request.POST.get('telephone')
    data = validate_mobile(mobile)
    if data['code'] == "0000":
        yunpian = YunPian(API_KEY)
        code = generate_code()
        sms_status = yunpian.send_msg(code=code, mobile=mobile)
        if sms_status["code"] != 0:
            data = {'code': '0004', 'msg': sms_status['msg']}
        else:
            VerifyCode.objects.create(mobile=mobile, code=code)
            data = {'code': '0000', 'msg': '验证码发送成功， 请注意查收！'}
    return HttpResponse(json.dumps(data))


def generate_code():
    """the function of creating 4 radom code"""
    seeds = "1234567890"
    random_str = []
    i = 0
    while True:
        random_str.append(choice(seeds))
        if i == 4:
            break
        i += 1
    return "".join(random_str)


def validate_code(mobile, code):
    """the function of validating code"""
    verify_codes = VerifyCode.objects.filter(mobile=mobile).order_by("-add_time")
    if verify_codes:
        last_code = verify_codes[0]
        five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=20, seconds=0)
        last_add_time = last_code.add_time.replace(tzinfo=None)
        if five_minutes_ago < last_add_time:
            data = {'code': '0004', 'msg': '验证码过期，请重新发送'}
        else:
            if code != last_code.code:
                data = {'code': '0005', 'msg': '验证码输入错误'}
            else:
                data = {'code': '0000'}
    else:
        data = {'code': '0006', 'msg': '该手机未获取到验证码'}
    return data


def change_tele(request):
    """the function of student's change telephone"""
    user_id = request.POST.get('user_id')
    code = request.POST.get('code')
    telephone = request.POST.get('telephone')
    student = Student.objects.get(user_id=user_id)
    data = validate_code(telephone, code)
    if data['code'] == "0000":
        student.telephone = telephone
        student.save()
        data = {'code': '0000', 'msg': '修改手机号码成功'}
    else:
        data = {'code': '0001', 'msg': data['msg']}
    return HttpResponse(json.dumps(data))
