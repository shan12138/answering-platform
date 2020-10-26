"""teachers views"""
import json
import time
from collections import deque
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core import serializers
from django.db import transaction
from room_operation.views import RoomQueue
from room_operation.models import RoomBanStudent, RoomTeacher, RoomStudent
from room_info.models import Room, RoomCalendar
from teachers.models import Teacher
from students.models import Student
from platform_system_admin.models import College
from backend.settings import MAX_WEEK
from backend.utils import JsonUtil
# Create your views here.


def change_password(request):
    """the function of teachers change_password"""
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
    """the function of teachers change_name"""
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    user = User.objects.get(id=user_id)
    teacher = Teacher.objects.get(user=user)
    teacher.real_name = name
    teacher.save()
    data = {'code': '0000', 'msg': '修改名字成功'}
    return HttpResponse(json.dumps(data), content_type="application/json")


class TeacherBackend(ModelBackend):
    """teachers sign_in authenticate token"""
    def authenticate(self, request, username=None, password=None):
        teacher = Teacher.objects.filter(email=username)
        if len(teacher) == 1:
            if teacher[0].user.check_password(password):
                return teacher[0].user
        else:
            return None
        return None


def get_teacher_name(request):
    """the function of getting teacher's name"""
    user_id = request.POST.get("user_id")
    try:
        user = User.objects.get(id=user_id)
        teacher = Teacher.objects.get(user_id=user.id)
        data = {'code': '0000', 'msg': '获取成功', 'data': teacher.real_name}
    except Exception:
        data = {'code': '0001', 'msg': '获取该老师姓名失败'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_teacher_email(request):
    """the function of getting teacher's email"""
    user_id = request.POST.get("user_id")
    try:
        user = User.objects.get(id=user_id)
        teacher = Teacher.objects.get(user_id=user.id)
        data = {'code': '0000', 'msg': '获取成功', 'email': teacher.email}
    except Exception:
        data = {'code': '0001', 'msg': '获取该老师邮箱失败'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def change_queue(request):
    """the function for teacher to change queue"""
    room_id = int(request.POST.get('room_id'))
    name = request.POST.get('name')
    move = int(request.POST.get('move'))
    deque1 = RoomQueue.dict[room_id]
    pos = deque1.index(name)
    next_pos = pos + move
    deque1.remove(name)
    deque1.insert(next_pos, name)
    RoomQueue.dict[room_id] = deque1
    return HttpResponse(json.dumps({'code': '0000', 'msg': '调整成功'}))


def confirm_teachers(request):
    """the function of teacher confirm_teachers in the room"""
    if request.method == 'POST':
        room_id = int(request.POST.get('room_id'))
        user_id = request.POST.get('user_id')
        try:
            teacher = Teacher.objects.get(user_id=user_id)
            RoomTeacher.objects.create(room_id_id=room_id, teacher_email_id=teacher.email)
            data = {'code': '0000', 'msg': '确认教师身份成功'}
        except Exception:
            data = {'code': '0005', 'msg': '确认教师身份失败'}
    return HttpResponse(json.dumps(data))


def ban_students(request):
    """the function of teacher ban students in the room"""
    room_id = request.POST.get('room_id')
    user_id = request.POST.get('user_id')
    student = Student.objects.get(user_id=user_id)
    RoomBanStudent.objects.create(
        room_id_id=room_id, student_id_id=student.id,
        ban_open_time=datetime.now(), ban_close_time=datetime.now())
    return HttpResponse(json.dumps({'code': '0000', 'msg': '禁言成功'}))


def close_ban_students(request):
    """the function of teacher close ban students in the room"""
    room_id = request.POST.get('room_id')
    user_id = request.POST.get('user_id')
    student = Student.objects.get(user_id=user_id)
    RoomBanStudent.objects.filter(room_id=room_id, student_id_id=student.id).delete()
    return HttpResponse(json.dumps({'code': '0000', 'msg': '解除禁言成功'}))


def open_living(request):
    """teacher open the living and the answer deque was inited"""
    room_id = int(request.POST.get('room_id'))
    current_deque = deque()
    RoomQueue.ask_dict[room_id] = current_deque
    return HttpResponse(json.dumps({'code':'0000', 'msg':'开启直播成功!'}))


def close_living(request):
    """teacher close living so the answer deque was destroyed"""
    room_id = int(request.POST.get('room_id'))
    del RoomQueue.ask_dict[room_id]
    return HttpResponse(json.dumps({'code':'0000', 'msg':'关闭直播成功！'}))


def delete_room_calendar(request):
    """the function of teacher delete room's calendar"""
    primary_key = request.POST.get("pk")
    RoomCalendar.objects.filter(pk=primary_key).delete()
    return HttpResponse(json.dumps({'code':'0000', 'msg':'成功删除日历信息!'}))


def list_room_students(request):
    """the function of listing the students in the room"""
    room_id = int(request.POST.get('room_id'))
    authenticated_queue = RoomQueue.authenticated_dict[room_id]
    return HttpResponse(json.dumps(
        {'code': '0000', 'msg': '查询待认证队列成功', 'data': list(authenticated_queue)}))


def list_own_rooms(request):
    """list all rooms which are created by the current teacher"""
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    teacher = Teacher.objects.get(user=user)
    host_email = teacher.email
    teachers_rooms = Room.objects.filter(
        host_email_id=host_email)
    rooms = JsonUtil.json_util(teachers_rooms)
    for room in rooms:
        college = College.objects.get(id=int(room['college']))
        room['college'] = college.name
    data = {'code': '0000', 'msg': '查询成功', 'data': rooms}
    return HttpResponse(json.dumps(data))


def list_resolved_rooms(request):
    """list all rooms which are resolved with the current teacher"""
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    teacher = Teacher.objects.get(user=user)
    host_email = teacher.email
    teachers_rooms = RoomTeacher.objects.filter(teacher_email_id=host_email)
    host_rooms = Room.objects.values('host_email_id').filter(host_email_id=host_email)
    rooms = JsonUtil.json_util(teachers_rooms)
    data = []
    for room in rooms:
        room_object = Room.objects.filter(id=room['room_id'])
        data_json = json.loads(serializers.serialize("json", room_object))
        college = College.objects.get(id=int(data_json[0]['fields']['college']))
        data_json[0]['fields']['college'] = college.name
        if not is_host(host_rooms, data_json[0]['fields']['host_email']):
            data.append(data_json[0]['fields'])
    data = {'code': '0000', 'msg': '查询成功', 'data': data}
    return HttpResponse(json.dumps(data))


def is_host(host_rooms, host_eamil):
    """"judge the current teacher is the room host"""
    for room in host_rooms:
        if host_eamil == room['host_email_id']:
            return True
    return False


def create_room(request):
    """the function of teacher creating the room"""
    user_id = request.POST.get('user_id')
    title = request.POST.get('title')
    description = request.POST.get('description')
    college = request.POST.get('college')
    password = request.POST.get('password')
    is_white_board = request.POST.get('is_white_board')
    is_code_editor = request.POST.get('is_code_editor')
    if is_white_board == 'true':
        is_white_board = 1
    else:
        is_white_board = 0
    if is_code_editor == 'true':
        is_code_editor = 1
    else:
        is_code_editor = 0
    user = User.objects.get(id=user_id)
    teacher = Teacher.objects.get(user=user)
    host_email = teacher.email
    data = atomic_create_room(
        host_email, title, description, college, password, is_code_editor, is_white_board)
    return HttpResponse(json.dumps(data), content_type="application/json")


def atomic_create_room(
        host_email, title, description, college, password, is_code_editor, is_white_board):
    """the function of teacher atomic creating the room """
    try:
        with transaction.atomic():
            Room.objects.create(host_email_id=host_email, title=title,
                                description=description, college_id=college, password=password,
                                is_code_editor=is_code_editor, is_white_board=is_white_board)
            room = Room.objects.filter(host_email_id=host_email).order_by("-id")
            room_id = room[0].id
            RoomTeacher.objects.create(room_id_id=room_id, teacher_email_id=host_email)
            authenticated_queue = deque()
            RoomQueue.authenticated_dict[room_id] = authenticated_queue
            data = {'code': '0000', 'msg': '创建房间成功'}
    except Exception:
        data = {'code': '0005', 'msg': '出现未知错误'}
    return data


def create_room_calendar(request):
    """the function of teacher creating room_calendar"""
    room_id = request.POST.get("room_id")
    weeks = request.POST.get("weeks")
    days = request.POST.get("days")
    open_time = request.POST.get("open_time")[0:5]
    close_time = request.POST.get("close_time")[0:5]
    week_array = weeks.split(',')
    day_array = days.split(',')
    if len(week_array) == 0:
        week_array = weeks
    if len(day_array) == 0:
        day_array = days
    data = atomic_create_room_calendar(room_id, week_array, day_array, open_time, close_time)
    return HttpResponse(json.dumps(data))


def atomic_create_room_calendar(room_id, weeks, days, open_time, close_time):
    """the function of teacher atomic_create_room_calendar"""
    try:
        with transaction.atomic():
            for week in weeks:
                for day in days:
                    room_calendar_curr = RoomCalendar.objects.filter(
                        room_id_id=room_id, week=week, day=day)
                    if room_calendar_curr.count() != 0:
                        for room_calendar in room_calendar_curr:
                            open_time_curr = room_calendar.open_time
                            close_time_curr = room_calendar.end_time
                            if (is_bigger_than_another(
                                close_time_curr, close_time) & is_bigger_than_another(
                                    close_time, open_time_curr)):
                                data = {'code': '0002', 'msg': '创建房间日历失败，时间段重复'}
                                return data
                            if (is_bigger_than_another(
                                open_time, open_time_curr) & is_bigger_than_another(
                                    close_time_curr, open_time)):
                                data = {'code': '0002', 'msg': '创建房间日历失败，时间段重复'}
                                return data
                    RoomCalendar.objects.create(
                        room_id_id=int(room_id), week=int(week) + 1, day=int(day),
                        open_time=open_time, end_time=close_time)
            data = {'code': '0000', 'msg': '创建房间日历成功'}
    except Exception:
        data = {'code': '0001', 'msg': '创建房间日历失败'}
    return data


def is_bigger_than_another(first_time, second_time):
    """the function of compare two time's size"""
    first_time = time.strptime(first_time, '%H:%M:%S')
    second_time = time.strptime(second_time, '%H:%M:%S')
    if first_time > second_time:
        return True
    else:
        return False


def alter_room(request):
    """the function of teacher alter room's info"""
    room_id = request.POST.get("room_id")
    title = request.POST.get('title')
    description = request.POST.get('description')
    college = request.POST.get('college')
    password = request.POST.get('password')
    is_white_board = request.POST.get('is_white_board')
    is_code_editor = request.POST.get('is_code_editor')
    if is_code_editor == 'true':
        is_code_editor = 1
    else:
        is_code_editor = 0
    if is_white_board == 'true':
        is_white_board = 1
    else:
        is_white_board = 0
    room = Room.objects.get(id=room_id)
    room.title = title
    room.description = description
    room.college_id = college
    room.password = password
    room.is_white_board = is_white_board
    room.is_code_editor = is_code_editor
    room.save()
    data = {'code': '0000', 'msg': '修改成功'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def alter_room_calendar(request):
    """the function of teacher alter room's calendar"""
    primary_key = request.POST.get("pk")
    week = request.POST.get("week")
    day = request.POST.get('day')
    open_time = request.POST.get('open_time')
    end_time = request.POST.get('end_time')
    try:
        room_calendar = RoomCalendar.objects.get(pk=primary_key)
        room_calendar.week = week
        room_calendar.day = day
        room_calendar.open_time = open_time
        room_calendar.end_time = end_time
        room_calendar.save()
        data = {'code': '0000', 'msg': '修改日历成功'}
    except Exception:
        data = {'code': '0001', 'msg': '修改日历失败'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def confirm_students(request):
    """the function of teacher confirm_students in the room"""
    if request.method == 'POST':
        room_id = int(request.POST.get('room_id'))
        user_id = request.POST.get('name')
        try:
            student = Student.objects.get(user_id=user_id)
        except Exception:
            return HttpResponse(json.dumps({'code': '0005', 'msg': '出现未知错误，操作失败'}))
        RoomStudent.objects.create(room_id_id=room_id, student_id_id=student.id)
        return HttpResponse(json.dumps({'code': '0000', 'msg': '确认学生身份成功'}))
    return HttpResponse(json.dumps({'code': '0005', 'msg': '出现未知错误，操作失败'}))


def cancel_confirm_students(request):
    """the function of teacher cancel confirmed student"""
    room_id = request.POST.get('room_id')
    user_id = request.POST.get('name')
    try:
        student = Student.objects.get(user_id=user_id)
    except Exception:
        return HttpResponse(json.dumps({'code': '0005', 'msg': '出现未知错误，操作失败'}))
    RoomStudent.objects.filter(room_id_id=room_id, student_id_id=student.id).delete()
    return HttpResponse(json.dumps({'code': '0000', 'msg': '取消认证成功'}))


def get_all_calendars(request):
    """the function of getting all room's calendar"""
    room_id = int(request.POST.get('room_id'))
    room_calendar = RoomCalendar.objects.filter(room_id_id=room_id)
    room_calendar = JsonUtil.json_util(room_calendar)
    room_calendars = {
        'timetable': room_calendar,
        'max_week': MAX_WEEK
    }
    data = {'code': '0000', 'msg': '获取成功', 'data': room_calendars}
    return HttpResponse(json.dumps(data))
