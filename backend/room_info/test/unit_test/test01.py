"""the test for room info"""
from django.test import TestCase
from django.contrib.auth.models import User
from teachers.models import Teacher
from platform_system_admin.models import College

# Create your tests here.
class RoomInfoTest(TestCase):
    """the class for create room"""

    def setUp(self):
        tea_user = User.objects.create(username='157252469@qq.com', password='123456**')
        Teacher.objects.create(email="157252469@qq.com", user=tea_user)
        College.objects.create(name='soft')

    def test_create_room(self):
        """this test is used to test create room for teachers"""
        test_data = {
            'user_id':1,
            'title':'jinyue',
            'description':'this is jinyue"s home',
            'college':1,
            'password':'',
            'is_white_board':0,
            'is_code_editor':1
        }
        response = self.client.post('/teachers/create_room', test_data)
        print(response.content)
