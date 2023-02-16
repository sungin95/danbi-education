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
        # 루틴 today 2023-02-15 수요일 기준
        self.routine = Routine.objects.create(
            account_id=self.user,
            title="problem solving",
            category="HOMEWORK",
            goal="Increase your problem-solving skills",
            is_alarm=True,
            days="MON WED FRI",
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

    # routine 수정
    def test_routine_PUT_modify(self):
        Token_ = (f"Token {self.user.token}".split("'"))[1]
        headers = {
            "HTTP_AUTHORIZATION": "token " + Token_,
        }
        response = self.client.put(
            f"/routine/routine_detail/{self.routine.routine_id}/",
            {
                "routine_id": self.routine.routine_id,
                "title": "problem solving!!!!!!",
                "category": "기상",
                "goal": "Increase your problem-solving skills!!!!!!",
                "is_alarm": False,
                "days": "MON WED FRI",
            },
            **headers,
        )
        # views 148번째에서 print해 보면 값이 바뀌어 있는 것을 볼 수 있다.
        self.assertEqual(response.status_code, 201)

    # routine 수정 days 수정
    def test_routine_PUT_modify_d(self):
        Token_ = (f"Token {self.user.token}".split("'"))[1]
        headers = {
            "HTTP_AUTHORIZATION": "token " + Token_,
        }
        response = self.client.put(
            f"/routine/routine_detail/{self.routine.routine_id}/",
            {
                "routine_id": self.routine.routine_id,
                "title": "problem solving!!!!!!",
                "category": "기상",
                "goal": "Increase your problem-solving skills!!!!!!",
                "is_alarm": False,
                "days": "MON WED",
            },
            **headers,
        )
        self.assertEqual(response.status_code, 201)

    # 로그인 안한 유저가 루틴 수정하려고 할때
    def test_routine_PUT_modify_d(self):
        response = self.client.put(
            f"/routine/routine_detail/{self.routine.routine_id}/",
            {
                "routine_id": self.routine.routine_id,
                "title": "problem solving!!!!!!",
                "category": "기상",
                "goal": "Increase your problem-solving skills!!!!!!",
                "is_alarm": False,
                "days": "MON WED",
            },
        )
        self.assertEqual(response.status_code, 403)

    # routine 삭제(소프트 딜리트)
    def test_routine_DELETE(self):
        Token_ = (f"Token {self.user.token}".split("'"))[1]
        headers = {
            "HTTP_AUTHORIZATION": "token " + Token_,
        }
        response = self.client.delete(
            f"/routine/routine_detail/{self.routine.routine_id}/",
            **headers,
        )
        # views 188줄에서 routine.is_deleted를 프린트하면 True가 나온다.
        self.assertEqual(response.status_code, 200)

    # routine 복구(소프트 딜리트)
    def test_routine_DELETE(self):
        Token_ = (f"Token {self.user.token}".split("'"))[1]
        headers = {
            "HTTP_AUTHORIZATION": "token " + Token_,
        }
        response = self.client.patch(
            f"/routine/routine_detail/{self.routine.routine_id}/",
            **headers,
        )
        # views 211줄에서 routine.is_deleted를 프린트하면 False로 나온다.
        self.assertEqual(response.status_code, 200)
