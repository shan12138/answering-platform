"""room_info models"""
from django.db import models


class Room(models.Model):
    """the class of the rooms"""
    title = models.CharField(max_length=50, null=True)
    college = models.ForeignKey(
        'platform_system_admin.College', on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    password = models.CharField(max_length=10, null=True)
    host_email = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE)
    is_white_board = models.BooleanField(null=True)
    is_code_editor = models.BooleanField(null=True)


class RoomCalendar(models.Model):
    """the class of the room_calendar"""
    room_id = models.ForeignKey('room_info.Room', on_delete=models.CASCADE)
    week = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    open_time = models.CharField(null=True, max_length=8)
    end_time = models.CharField(null=True, max_length=8)
    class Meta:
        """set the room's unique key"""
        unique_together = (("room_id", "week", "day", "open_time", "end_time"),)
