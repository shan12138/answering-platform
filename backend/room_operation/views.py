"""room_operation views"""
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from room_info.models import Room
from students.models import Student
from teachers.models import Teacher
from platform_system_admin.models import College
from backend.utils import JsonUtil
from .models import RoomStudent, RoomBanStudent, RoomTeacher


def search_room_by_condition(request):
    """the function of searching eligible rooms of the teachers and students"""
    if request.method == "POST":
        query_condition = request.POST.get('query_condition')
        page = int(request.POST.get('page'))
        limit = int(request.POST.get('limit'))
        start_position = page * limit
        if not query_condition:
            room = Room.objects.all()[start_position:start_position+limit]
        else:
            room = search_by_diff_condition(query_condition, start_position, limit)
            if not room:
                return HttpResponse(json.dumps({'code': '0001', 'msg': '查询结果为空', 'data': ''}))
        rooms = JsonUtil.json_util(room)
        for room in rooms:
            college = College.objects.get(id=int(room['college']))
            teacher = Teacher.objects.get(email=room['host_email'])
            room['college'] = college.name
            room['teacher_name'] = teacher.real_name
        if rooms:
            data = {'code': '0000', 'msg': '查询成功', 'data': rooms}
        else:
            data = {'code': '0001', 'msg': '查询结果为空', 'data': ''}
        return HttpResponse(json.dumps(data))
    return None


def search_by_diff_condition(query_condition, start_position, limit):
    """get the rooms by different query condition"""
    room = Room.objects.filter(title=query_condition)[start_position:start_position+limit]
    if room.count() == 0:
        teacher = Teacher.objects.filter(real_name=query_condition)
        if teacher.count() != 0:
            tmp_query_condition = teacher[0].email
            room = Room.objects.filter(
                host_email_id=tmp_query_condition)[start_position:start_position+limit]
        else:
            college = College.objects.filter(name=query_condition)
            if college.count() != 0:
                tmp_query_condition = college[0].id
                room = Room.objects.filter(
                    college_id=tmp_query_condition)[start_position:start_position+limit]
            else:
                room = None
    return room


class RoomQueue:
    """the class of roomqueue"""
    ask_dict = {}
    authenticated_dict = {}

    def __init__(self, room_id, queue):
        self.room_id = room_id
        self.queue = queue
        RoomQueue.authenticated_dict[room_id] = queue


def search_room_info(request):
    """the function of teachers and students searching room info"""
    room_id = request.POST.get("room_id")
    user_id = request.POST.get("user_id")
    room = Room.objects.get(id=room_id)
    host_email = room.host_email_id
    teacher = Teacher.objects.get(email=host_email)
    college = College.objects.get(id=room.college_id)
    fields = {}
    fields['description'] = room.description
    fields['title'] = room.title
    fields['teacher_name'] = teacher.real_name
    fields['college'] = college.name
    if int(user_id) == teacher.user_id:
        is_password = False
    else:
        is_password = True
    data = {
        'room_info': fields,
        'is_password': is_password,
    }
    return HttpResponse(json.dumps({'code': '0000', 'msg': '查询成功', 'data': data}))


def enter_password(request):
    """the function of enter room's password for teachers and students"""
    room_id = request.POST.get('room_id')
    password = request.POST.get('password')
    room = Room.objects.filter(id=room_id, password=password)
    if room.count():
        data = {'code': '0000', 'msg': '成功进入房间'}
    else:
        data = {'code': '0001', 'msg': '房间密码输入错误，请重新输入'}
    return HttpResponse(json.dumps(data))


def enter_room(request):
    """the function of enter_room for
    teachers and students with getting speaking and authentication state"""
    room_id = int(request.POST.get('room_id'))
    user_id = int(request.POST.get('user_id'))
    student = Student.objects.filter(user_id=user_id)
    if student.count():
        user = User.objects.get(id=student[0].user_id)
        data = get_student_state(room_id, user.username, student[0])
    else:
        teacher = Teacher.objects.filter(user_id=user_id)
        if teacher.count():
            data = get_teacher_state(room_id, teacher.email, teacher[0])
    return HttpResponse(json.dumps({'code': '0000', 'msg': '查询成功', 'data': data}))


def get_student_state(room_id, username, student):
    """the function of getting student's state"""
    data = {}
    authenticated_student = RoomStudent.objects.filter(
        student_id_id=student.id, room_id_id=room_id)
    if authenticated_student.count():
        data["authenticated_state"] = True
    else:
        data["authenticated_state"] = False
    data['student_id'] = username
    authenticated_queue = RoomQueue.authenticated_dict[room_id]
    authenticated_queue.append(data)
    ban_student = RoomBanStudent.objects.filter(
        student_id_id=student.id, room_id_id=room_id)
    if ban_student.count():
        data["spoken_state"] = False
    else:
        data["spoken_state"] = True
    return data


def get_teacher_state(room_id, email, teacher):
    """the function of getting teacher's state"""
    data = {}
    authenticated_teacher = RoomTeacher.objects.filter(
        teacher_email_id=teacher.email, room_id_id=room_id)
    if authenticated_teacher.count():
        data["authenticated_state"] = True
    else:
        data["authenticated_state"] = False
    data['teacher_email'] = email
    authenticated_queue = RoomQueue.authenticated_dict[room_id]
    authenticated_queue.append(data)
    return data
