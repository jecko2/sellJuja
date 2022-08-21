from account.models import BaseUserModel
from django.test import TestCase


class TestBaseUserModel(TestCase):
    user = BaseUserModel.objects.create(email="test@gmail.com")
    def test_user_created(self):
        
        self.assertTrue(self.user)
        
    def test_created_email(self):
        email = BaseUserModel.objects.filter(email="test@gmail.com").first()
        self.assertEqual(email, "test@gmail.com")
        
    