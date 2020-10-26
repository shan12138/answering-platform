"""the test is used to test the dict can be share"""
from collections import deque

from django.test import TestCase

from room_operation.views import RoomQueue


class RoomQueueTest(TestCase):
    """The class is used to test the part of RoomQueue"""

    def test_init_of_room_queue(self):
        """Test the dict contains all the key-value"""
        queue1 = deque()
        RoomQueue(1, queue1)
        queue2 = deque()
        RoomQueue(2, queue2)
        print(RoomQueue.dict)
