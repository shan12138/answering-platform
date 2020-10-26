"""the testcase of altering room_info"""
from django.contrib.auth.models import User
from django.test import TestCase
from room_info.models import Room
from platform_system_admin.models import College
from teachers.models import Teacher


# Create your tests here.
class ALterRoomInfoTest(TestCase):
    """the class is used for room_info operate"""
    def setUp(self):
        College.objects.create(name='software college')
        teacher_user = User.objects.create_user(
            username='157252469@qq.com', password='123456**')
        teacher = Teacher(user=teacher_user, email='157252469@qq.com')
        teacher.save()
        Room.objects.create(
            title='shanshan', college_id=1, description='This is used to answer java questions',
            password='222222', host_email_id='157252469@qq.com', is_white_board=1, is_code_editor=1)

    def test_alter_room_info(self):
        """the function is used to alter room_info"""
        test_data = {
            'room_id': 1,
            'title': 'jinyue',
            'description': 'This is used to answer python questions',
            'college': 1,
            'password': '000000',
            'is_white_board': 0,
            'is_code_editor': 0
        }
        response = self.client.post('/teachers/alter_room', test_data)
        print(response.content, ')))))))))))))))))))))))')
