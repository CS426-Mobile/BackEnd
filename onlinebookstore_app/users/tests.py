from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class UserRegistrationTest(TestCase):
    def test_register_success(self):
        data = {
            "email": "test@example.com",
            "password": "password123",
            "password2": "password123"
        }
        response = self.client.post(reverse('register'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Account was created for test@example.com")
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        print("UserRegistrationTest.test_register_success")

    def test_register_password_mismatch(self):
        data = {
            "email": "test2@example.com",
            "password": "password123",
            "password2": "password321"
        }
        response = self.client.post(reverse('register'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Passwords do not match")
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_register_email_taken(self):
        User.objects.create_user(email="test@example.com", password="password123")
        data = {
            "email": "test@example.com",
            "password": "password123",
            "password2": "password123"
        }
        response = self.client.post(reverse('register'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Email is already taken")
