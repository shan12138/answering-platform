"""admin_manage views"""
import json
from django.core import serializers
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import transaction
import xlrd
from teachers.models import Teacher
from backend.utils import JsonUtil
from .models import College


def create_teacher(request):
    """admin create teacher"""
    if request.method == "POST":
        file = request.FILES.get('file')
        excel_type = file.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            wb = xlrd.open_workbook(filename=None, file_contents=file.read())
            table = wb.sheets()[0]
            rows = table.nrows
            data = atomic_create_teacher(table, rows)
        else:
            data = {'code': '0005', 'msg': '上传文件类型错误'}
    else:
        data = {'code': '0006', 'msg': '请求方法错误'}
    return HttpResponse(json.dumps(data))


def create_college(request):
    """admin create college"""
    if request.method == "POST":
        file = request.FILES.get('file')
        excel_type = file.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            work_book = xlrd.open_workbook(filename=None, file_contents=file.read())
            table = work_book.sheets()[0]
            rows = table.nrows
            data = atomic_create_college(table, rows)
        else:
            data = {'code': '0005', 'msg': '上传文件类型错误'}
    else:
        data = {'code': '0006', 'msg': '请求方法错误'}
    return HttpResponse(json.dumps(data))


def atomic_create_teacher(table, rows):
    """the function of admin atomic_create_teacher"""
    try:
        with transaction.atomic():
            for i in range(1, rows):
                row_values = table.row_values(i)
                teacher_user = User.objects.create_user(
                    username=row_values[0], password=row_values[1])
                teacher = Teacher(user=teacher_user, email=row_values[0])
                teacher.save()
    except Exception:
        data = {'code': '0003', 'msg': '导入教师账号失败'}
    else:
        teachers = Teacher.objects.all()
        data_json = json.loads(serializers.serialize("json", teachers))
        return_data = []
        for data in data_json:
            primary_key = data["pk"]
            fields = data["fields"]
            fields["pk"] = primary_key
            del fields["user"]
            return_data.append(fields)
        data = {'code': '0000', 'msg': '导入教师账号成功', 'data': return_data}
    return data


def atomic_create_college(table, rows):
    """the function of admin atomic_create_college"""
    try:
        with transaction.atomic():
            for i in range(1, rows):
                row_values = table.row_values(i)
                college = College.objects.create(name=row_values[0])
                college.save()
    except Exception:
        data = {'code': '0003', 'msg': '导入专业信息失败'}
    else:
        colleges = College.objects.all()
        colleges = JsonUtil.json_util(colleges)
        data = {'code': '0000', 'msg': '导入专业信息成功', 'data': colleges}
    return data


class AdminBackend(ModelBackend):
    """admin sign_in authenticate token"""
    def authenticate(self, request, username=None, password=None):
        username = username.strip()
        password = password.strip()
        admin = User.objects.filter(username=username)
        if admin.count() == 1:
            if admin[0].check_password(password):
                return admin[0]
        else:
            return None
