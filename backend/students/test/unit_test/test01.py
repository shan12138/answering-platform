"""the test is used to test student's operation to room"""
from collections import deque
from django.test import TestCase
from django.contrib.auth.models import User
from students.models import Student
from room_info.models import Room
from teachers.models import Teacher
from room_operation.views import RoomQueue
from room_operation.models import RoomStudent

class StudentRoomTest(TestCase):
    """the class is used for student operate"""
    def setUp(self):
        user = User.objects.create(username='2016215156', password='123456**')
        student = Student.objects.create(real_name='huanglf', user=user)
        tea_user = User.objects.create(username='157252469@qq.com', password='123456**')
        Teacher.objects.create(email="157252469@qq.com", user=tea_user)
        room = Room.objects.create(host_email_id='157252469@qq.com')
        RoomStudent.objects.create(room_id_id=room.id, student_id_id=student.id)

    def test_apply_to_ask(self):
        """the function is used to apply to ask"""
        test_data = {
            'room_id': 1,
            'user_id': 1
        }
        RoomQueue.dict[1] = deque()
        response = self.client.post('/students/apply_ask', test_data)
        print(response)
        print(RoomQueue.dict[1], '********************')
