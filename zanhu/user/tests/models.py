from django.test import TestCase
from .models import User
# Create your tests here.


class UserModelTests(TestCase):

    def test__str__(self):
        self.assertEqual(self.user.__str__(), 'testuser')
