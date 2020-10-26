"""the test is used to test teacher can change the answer queue"""
from collections import deque
from django.test import TestCase
from django.contrib.auth.models import User
from room_operation.views import RoomQueue
from room_info.models import Room
from platform_system_admin.models import College
from teachers.models import Teacher


class RoomQueueTest(TestCase):
    """The class is used to test the change of RoomQueue"""
    def setUp(self):
        College.objects.create(name='software college')
        teacher_user = User.objects.create(
            username='157252469@qq.com', password='123456**')
        teacher = Teacher(user=teacher_user, email='157252469@qq.com')
        teacher.save()
        Room.objects.create(
            title='', college_id=1, description='',
            password='222222', host_email_id='157252469@qq.com', is_white_board=1, is_code_editor=1)


    def test_change_queue(self):
        """Test teacher can change the answer queue"""
        test_data = {
            'room_id':1,
            'name' :'2016215156',
            'move' :-2
        }
        deque1 = deque()
        deque1.append('2016215151')
        deque1.append('2016215152')
        deque1.append('2016215153')
        deque1.append('2016215156')
        RoomQueue.dict[1] = deque1
        response = self.client.post('/teachers/change_queue', test_data)
        print(response)
        print(RoomQueue.dict[1], '****************')
