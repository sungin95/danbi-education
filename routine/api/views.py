from ..models import Routine, RoutineDay, RoutineResult
from .serializers import (
    RoutineSerializer,
    RoutineDaySerializer,
    RoutineResultSerializer,
)
from datetime import datetime, timedelta
from django.http import Http404

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # 로그인한 사용자만
from rest_framework.views import APIView
from rest_framework import status


# 중복된 내용 이므로 함수화
def create_routine_day_result(serializer, data, request):
    serializer.validated_data["account_id"] = request.user
    serializer.validated_data["days"] = str(data["days"])
    serializer.save()
    today = datetime.today().weekday() + 1
    now = datetime.now()
    week = now + timedelta(weeks=0, days=-(today % 7))
    routine = Routine.objects.get(routine_id=serializer["routine_id"].value)
    for d in data["days"]:
        temp = week + timedelta(days=week_day[d])
        temp_time = temp.strftime("%Y-%m-%d")
        # day
        serializer_day = RoutineDaySerializer(data=data)
        if serializer_day.is_valid():
            serializer_day.validated_data["day"] = temp_time
            serializer_day.validated_data["routine_id"] = routine
            serializer_day.save()
        # result
        serializer_result = RoutineResultSerializer(data=data)
        if serializer_result.is_valid():
            serializer_result.validated_data["day"] = temp_time
            serializer_result.validated_data["routine_id"] = routine
            serializer_result.save()


week_day = {
    "MON": 1,
    "TUE": 2,
    "WED": 3,
    "THU": 4,
    "FRI": 5,
    "SAT": 6,
    "SUN": 7,
}


# 루틴 생성 및 조회
class CreateRoutineAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoutineSerializer

    def post(self, request):
        data = JSONParser().parse(request)

        serializer = self.serializer_class(data=data)
        # create Routine
        if serializer.is_valid():
            create_routine_day_result(serializer, data, request)
            return Response(
                {
                    "data": {"routine_id": serializer.data["routine_id"]},
                    "message": {
                        "msg": "You have successfully created the routine.",
                        "status": "ROUTINE_CREATE_OK",
                    },
                },
                # 201 Created (요청이 성공적 + 결과로 새로운 리소스 생성 | POST, PUT)
                status=status.HTTP_201_CREATED,
            )
        # Bad Request (사용자의 잘못된 요청을 처리할 수 없음)
        return Response("valid errors", status=status.HTTP_400_BAD_REQUEST)

    # 철수의 오늘 루틴 체크
    def get(self, request):
        data = JSONParser().parse(request)
        # 오늘
        today = data["today"]
        # 철수
        account_id = data["account_id"]

        # 철수 루틴
        routine_name = Routine.objects.filter(account_id=account_id)
        routine_list = []
        for routine in routine_name:
            for d in routine.routineresult_set.all():
                # 오늘 루틴만
                if str(d.day) == today:
                    dict_ = {}
                    dict_["goal"] = routine.goal
                    dict_["id"] = account_id
                    dict_["result"] = d.result
                    dict_["title"] = routine.title
                    routine_list.append(dict_)
        return Response(
            {
                "data": routine_list,
                "message": {
                    "msg": "Routine lookup was successful.",
                    "status": "ROUTINE_LIST_OK",
                },
            },
            # OK (요청이 성공적으로 수행되었음)
            status=status.HTTP_200_OK,
        )


# 루틴 수정(PUT) 및 삭제(DELETE), 복구(PATCH)
class RoutineDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoutineSerializer

    def get_routine(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            # Not found (요청한 페이지(리소스) 없음)
            raise Http404

    def put(self, request, pk):
        # 수정
        routine = self.get_routine(pk)
        # 본인만 루틴 수정 가능
        if routine.account_id == request.user:
            data = JSONParser().parse(request)
            # days가 같으면 값만 수정
            if str(data["days"]) == routine.days:
                serializer = RoutineSerializer(routine, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "data": {"routine_id": serializer.data["routine_id"]},
                            "message": {
                                "msg": "The routine has been modified.",
                                "status": "ROUTINE_UPDATE_OK",
                            },
                        },
                        # Created (요청이 성공적 + 결과로 새로운 리소스 생성 | POST, PUT)
                        status=status.HTTP_201_CREATED,
                    )
            # days가 달라지면 삭제하고 다시 만듬
            else:
                routine.delete()
                serializer = RoutineSerializer(data=data)
                if serializer.is_valid():
                    create_routine_day_result(serializer, data, request)
                    return Response(
                        {
                            "data": {"routine_id": serializer.data["routine_id"]},
                            "message": {
                                "msg": "The routine has been modified.",
                                "status": "ROUTINE_UPDATE_OK",
                            },
                        },
                        # Created (요청이 성공적 + 결과로 새로운 리소스 생성 | POST, PUT)
                        status=status.HTTP_201_CREATED,
                    )
        # Forbidden (접근 권한없음)
        return Response(
            "Bad Request",
            status=status.HTTP_403_FORBIDDEN,
        )

    def delete(self, request, pk):
        routine = self.get_routine(pk)
        if routine.account_id == request.user:
            routine.soft_delete()
            return Response(
                {
                    "data": {"routine_id": routine.routine_id},
                    "message": {
                        "msg": "The routine has been deleted.",
                        "status": "ROUTINE_DELETE_OK",
                    },
                },
                #  OK (요청이 성공적으로 수행되었음)
                status=status.HTTP_200_OK,
            )
        # Forbidden (접근 권한없음)
        return Response(
            "Forbidden (접근 권한없음)",
            status=status.HTTP_403_FORBIDDEN,
        )

    # 복구
    def patch(self, request, pk):
        routine = Routine.all_objects.get(pk=pk)
        if routine.account_id == request.user:
            routine.restore()
            return Response(
                {
                    "data": {"routine_id": routine.routine_id},
                    "message": {
                        "msg": "The routine has been restored.",
                        "status": "ROUTINE_RESTORE_OK",
                    },
                },
                #  OK (요청이 성공적으로 수행되었음)
                status=status.HTTP_200_OK,
            )
        # Forbidden (접근 권한없음)
        return Response(
            "Forbidden (접근 권한없음)",
            status=status.HTTP_403_FORBIDDEN,
        )
