"""room_info views"""
import json
from datetime import datetime
from django.http import HttpResponse
from room_operation.views import RoomQueue
from platform_system_admin.models import College
from backend.utils import JsonUtil
from backend.settings import MAX_WEEK
from room_info.models import RoomCalendar
# Create your views here.


def list_room_calendar(request):
    """the function of students and teachers listing room calendar"""
    room_id = request.POST.get('room_id')
    week = request.POST.get("week")
    rooms = RoomCalendar.objects.filter(room_id_id=room_id, week=week)
    if rooms.count():
        rooms = JsonUtil.json_util(rooms)
        data = {'code': '0000', 'msg': '查询成功', 'data': rooms}
    else:
        data = {'code': '0001', 'msg': '该房间暂无日历信息', 'data': None}
    return HttpResponse(json.dumps(data))


def list_colleges(request):
    """the function of getting all colleges"""
    colleges = College.objects.all()
    college_list = JsonUtil.json_util(colleges)
    data = {'code': '0000', 'msg': '查询成功', 'data': college_list}
    return HttpResponse(json.dumps(data))


def get_curr_max_week(request):
    """the function of get the current and max week of the room's caledar"""
    BEGIN_DAY = datetime.strptime('2018-9-3', '%Y-%m-%d')
    today = datetime.now()
    current_week = int((today - BEGIN_DAY).days / 7) + 1
    data = {
        'current_week': current_week,
        'max_week': MAX_WEEK
    }
    data = {'code': '0000', 'msg': '获取成功', 'data': data}
    return HttpResponse(json.dumps(data), content_type="application/json")


def look_answer_deque(request):
    """return the answer deque with order and name"""
    room_id = int(request.POST.get('room_id'))
    current_deque = RoomQueue.ask_dict[room_id]
    current_list = list(current_deque)
    return HttpResponse(json.dumps({'code':'0000', 'msg':'获取等待队列成功', 'data':current_list}))
