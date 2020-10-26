"""the test is used to test teacher confirm student"""
from django.test import TestCase
from django.contrib.auth.models import User
from students.models import Student
from room_info.models import Room
from teachers.models import Teacher


class RoomOperationTest(TestCase):
    """the class is used for teacher operate"""
    def setUp(self):
        user = User.objects.create(username='2016215156', password='123456**')
        Student.objects.create(real_name='huanglf', user=user)
        tea_user = User.objects.create(username='157252469@qq.com', password='123456**')
        Teacher.objects.create(email="157252469@qq.com", user=tea_user)
        Room.objects.create(host_email_id='157252469@qq.com')

    def test_confirm_student(self):
        """the function is used for confirm student"""
        test_data = {
            'room_id': 1,
            'name': '2016215156'
        }
        response = self.client.post('/teachers/confirm_students', test_data)
        print(response)
