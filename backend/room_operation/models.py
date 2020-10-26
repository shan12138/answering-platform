"""room _operation models"""
from django.db import models
from teachers.models import Teacher


# Create your models here.
class RoomTeacher(models.Model):
    """the class of teachers authenticated in the room"""
    room_id = models.ForeignKey('room_info.Room', on_delete=models.CASCADE)
    teacher_email = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class RoomStudent(models.Model):
    """the class of students authenticated in the room"""
    room_id = models.ForeignKey('room_info.Room', on_delete=models.CASCADE)
    student_id = models.ForeignKey('students.Student', on_delete=models.CASCADE)


class RoomBanStudent(models.Model):
    """the class of students banned speaking in the room"""
    room_id = models.ForeignKey('room_info.Room', on_delete=models.CASCADE)
    student_id = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    ban_open_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    ban_close_time = models.DateTimeField(auto_now=False, auto_now_add=False)
