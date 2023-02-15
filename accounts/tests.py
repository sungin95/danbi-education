from django.test import TestCase, Client
from .models import User
from django.urls import reverse


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.email = "TESTL@test.com"
        self.password = "test@pass1265"
        self.phone_number = "000-0000-0000"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            phone_number=self.phone_number,
        )

    def test_login(self):
        response = self.client.post(
            "/users/login", {"email": self.email, "password": self.password}
        )
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_credentials(self):
        response = self.client.post(
            "/users/login",
            {"email": self.email, "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 400)
