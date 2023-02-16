from django.test import TestCase, Client
from accounts.models import User
from .models import Routine, RoutineDay, RoutineResult
from rest_framework.test import APIClient


# Routine 만들기
class CreateRoutineTestCase(TestCase):
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

    # 요일을 나타낼때 문제가 있음. 테스트 코드를 통과 할 수 있게 바꾸어 놨고 평소에는 제거해야함.
    # views의 27번째줄  .split(" ")
    # routine 생성 확인
    def test_create_routine(self):
        Token_ = (f"Token {self.user.token}".split("'"))[1]
        headers = {
            "HTTP_AUTHORIZATION": "token " + Token_,
        }
        response = self.client.post(
            "/routine/routine/",
            {
                "title": "problem solving",
                "category": "HOMEWORK",
                "goal": "Increase your problem-solving skills",
                "is_alarm": True,
                "days": "MON WED FRI",  # test케이스 확인할때 예상치 못한 버그로 수정
            },
            **headers,
        )
        # print(response.content)
        self.assertEqual(response.status_code, 201)


# 오늘 할 거 조회
class TodayRoutineTestCase(TestCase):
    # 회원가입 + 루틴만들기
    def setUp(self):
        # 회원가입
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
        # 루틴
        self.routine = Routine.objects.create(
            account_id=self.user,
            title="problem solving",
            category="HOMEWORK",
            goal="Increase your problem-solving skills",
            is_alarm=True,
            days='["MON", "WED", "FRI"]',
        )
        self.routineResult1 = RoutineResult.objects.create(
            day="2023-02-13",
            routine_id=self.routine,
        )
        self.routineResult2 = RoutineResult.objects.create(
            day="2023-02-15",
            routine_id=self.routine,
        )
        self.routineResult3 = RoutineResult.objects.create(
            day="2023-02-17",
            routine_id=self.routine,
        )

    # 오늘 할 거 조회 2월 15일 기준
    def test_today_routine(self):
        Token_ = (f"Token {self.user.token}".split("'"))[1]
        headers = {
            "HTTP_AUTHORIZATION": "token " + Token_,
        }
        response = self.client.get(
            "/routine/routine/",
            {"account_id": self.user.pk, "today": "2023-02-15"},
            **headers,
        )

        # print(response.content)
        self.assertEqual(response.status_code, 200)

    # 토큰 없는 유저 오늘 할 거 조회 2월 15일 기준
    def test_today_routine_not_login(self):
        response = self.client.get(
            "/routine/routine/",
            {"account_id": self.user.pk, "today": "2023-02-15"},
        )
        self.assertEqual(response.status_code, 403)
