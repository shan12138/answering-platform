"""the testcase of creating room_calendar"""
from django.contrib.auth.models import User
from django.test import TestCase
from room_info.models import Room
from platform_system_admin.models import College
from teachers.models import Teacher


# Create your tests here.
class RoomCalendarCreateTest(TestCase):
    """the class is used for room_calendar operate"""
    def setUp(self):
        College.objects.create(name='software college')
        teacher_user = User.objects.create_user(
            username='157252469@qq.com', password='123456**')
        teacher = Teacher(user=teacher_user, email='157252469@qq.com')
        teacher.save()
        Room.objects.create(
            title='', college_id=1, description='',
            password='222222', host_email_id='157252469@qq.com', is_white_board=1, is_code_editor=1)


    def test_create_room_calendar(self):
        """the function is used to create room_calendar"""
        test_data = {
            'room_id': 1,
            'weeks': '1,3,5',
            'day': '3',
            'open_time': '17:30',
            'close_time': '18:30'
        }
        response = self.client.post('/teachers/create_room_calendar', test_data)
        print(response.content, '((((((((((((((((((((((((')
