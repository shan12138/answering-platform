"""the testcase of searching room_calendar"""
from django.contrib.auth.models import User
from django.test import TestCase
from room_info.models import Room, RoomCalendar
from platform_system_admin.models import College
from teachers.models import Teacher


# Create your tests here.
class RoomCalendarSearchTest(TestCase):
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
        RoomCalendar.objects.create(
            room_id_id=1, week='1', day='3', open_time='17:30', end_time='18:30')

    def test_search_room_calendar(self):
        """the function is used to search room_calendar"""
        test_data = {
            'room_id': 1,
            'week': '1'
        }
        response = self.client.post('/teachers/list_room_calendar', test_data)
        print(response.content, ')))))))))))))))))))))))')
