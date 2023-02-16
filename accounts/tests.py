from django.test import TestCase, Client
from .models import User
from rest_framework.test import APIClient
from rest_framework.test import APIClient


# 회원 가입
class signupTestCase(TestCase):
    # 정상적 회원가입 201
    def test_signup(self):
        response = self.client.post(
            "/accounts/register",
            {
                "phone_number": "000-0000-0000",
                "username": "signup",
                "email": "signup@test.com",
                "password": "test@pass65",
            },
        )
        self.assertEqual(response.status_code, 201)

    # 비밀 번호를 틀리게 함 400
    def test_signup_with_wrong_password(self):
        response = self.client.post(
            "/accounts/register",
            {
                "phone_number": "000-0000-0000",
                "username": "signup",
                "email": "signup@test.com",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)

    # 이메일 형식를 틀리게 함 400
    def test_signup_with_wrong_email(self):
        response = self.client.post(
            "/accounts/register",
            {
                "phone_number": "000-0000-0000",
                "username": "signup",
                "email": "signup",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)

    # 하나를 빼 먹음 400
    def test_signup_with_wrong(self):
        response = self.client.post(
            "/accounts/register",
            {
                # "phone_number": "000-0000-0000",
                "username": "signup",
                "email": "signup",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)


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

    # 정상적 로그인 200
    def test_login(self):
        response = self.client.post(
            "/accounts/login", {"email": self.email, "password": self.password}
        )
        self.assertEqual(response.status_code, 200)

    # 비밀번호를 다르게 400
    def test_login_with_wrong_credentials(self):
        response = self.client.post(
            "/accounts/login",
            {"email": self.email, "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 400)


# 로그인 안한 유저가 정보를 바꿀려고 하면 접근권한 없음 403
class AnonymousUserPATCHTestCase(TestCase):
    def test_anonymous_user_PATCH(self):
        response = self.client.patch(
            "/accounts/current",
            {"username": "update Username223"},
        )
        self.assertEqual(response.status_code, 403)


# 로그인 한 유저가 정보 바꿀려고 하면 성공 201
class LoginUserPATCHTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser222"
        self.email = "TESTL222@test.com"
        self.password = "test@pass1265"
        self.phone_number = "000-0000-0000"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            phone_number=self.phone_number,
            password=self.password,
        )

    # 201확인, 값을 확인은 모르겠다...
    def test_login_PATCH_username(self):
        Token_ = (f"Token {self.user.token}".split("'"))[1]
        headers = {
            "HTTP_AUTHORIZATION": "token " + Token_,
        }
        response = self.client.patch(
            "/accounts/current",
            {"username": "update Username223"},
            **headers,
        )
        self.assertEqual(response.status_code, 201)
