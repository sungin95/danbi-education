from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Routine, RoutineDay, RoutineResult
from .serializers import (
    RoutineSerializer,
    RoutineDaySerializer,
    RoutineResultSerializer,
)
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView


# @api_view(["POST"])
week_day = {
    "MON": 1,
    "TUE": 2,
    "WED": 3,
    "THU": 4,
    "FRI": 5,
    "SAT": 6,
    "SUN": 7,
}


@csrf_exempt
# 루틴 생성 및 루틴 데이 생성
def createRoutine(request):
    if request.method == "POST":
        # request를 parse와 JSONParser를 거쳐서 딕셔너리 형태로 data가 완성된다.
        data = JSONParser().parse(request)
        # create Routine
        serializer = RoutineSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data["account_id"] = request.user
            serializer.validated_data["days"] = str(data["days"])
            serializer.save()
            # create RoutineDay.
            today = datetime.today().weekday() + 1
            now = datetime.now()
            week = now + timedelta(weeks=0, days=-(today % 7))
            routine = Routine.objects.get(routine_id=serializer["routine_id"].value)
            for d in data["days"]:
                temp = week + timedelta(days=week_day[d])
                temp_time = temp.strftime("%Y-%m-%d")
                serializer2 = RoutineDaySerializer(data=data)
                if serializer2.is_valid():
                    serializer2.validated_data["day"] = temp_time
                    serializer2.validated_data["routine_id"] = routine
                    serializer2.save()
                serializer3 = RoutineResultSerializer(data=data)
                if serializer3.is_valid():
                    serializer3.validated_data["day"] = temp_time
                    serializer3.validated_data["routine_id"] = routine
                    serializer3.save()
            return JsonResponse(
                {
                    "data": {"routine_id": serializer.data["routine_id"]},
                    "message": {
                        "msg": "You have successfully created the routine.",
                        "status": "ROUTINE_CREATE_OK",
                    },
                },
                status=201,
            )
    return JsonResponse(serializer.errors, status=400)


# 오늘 할 일 조회
@api_view(["GET"])
def today_todos(request):
    if request.method == "GET":
        data = JSONParser().parse(request)
        today = data["today"]
        account_id = data["account_id"]

        query_set = Routine.objects.filter(account_id=account_id)
        query_list = []
        for query in query_set:
            for d in query.routineresult_set.all():
                if str(d.day) == today:
                    dict_ = {}
                    dict_["goal"] = query.goal
                    dict_["id"] = account_id
                    dict_["result"] = d.result
                    dict_["title"] = query.title
                    query_list.append(dict_)
        return Response(
            {
                "data": query_list,
                "message": {
                    "msg": "Routine lookup was successful.",
                    "status": "ROUTINE_LIST_OK",
                },
            }
        )


@csrf_exempt
def modify(request, pk):
    # 수정
    obj = get_object_or_404(Routine, pk=pk)
    if obj.account_id == request.user:
        if request.method == "POST":
            data = JSONParser().parse(request)
            if str(data["days"]) == obj.days:
                # 수정은 따로 만들어야 하나? 확인 필요
                serializer = RoutineSerializer(obj, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        {
                            "data": {"routine_id": serializer.data["routine_id"]},
                            "message": {
                                "msg": "The routine has been modified.",
                                "status": "ROUTINE_UPDATE_OK",
                            },
                        },
                        status=201,
                    )
            else:
                # days가 바뀌면 삭제하고 다시 만든다.
                obj.delete()
                serializer = RoutineSerializer(data=data)
                if serializer.is_valid():
                    serializer.validated_data["account_id"] = request.user
                    serializer.validated_data["days"] = str(data["days"])
                    serializer.save()
                    # create RoutineDay.
                    today = datetime.today().weekday() + 1
                    now = datetime.now()
                    week = now + timedelta(weeks=0, days=-(today % 7))
                    routine = Routine.objects.get(
                        routine_id=serializer["routine_id"].value
                    )
                    for d in data["days"]:
                        temp = week + timedelta(days=week_day[d])
                        temp_time = temp.strftime("%Y-%m-%d")
                        serializer2 = RoutineDaySerializer(data=data)
                        if serializer2.is_valid():
                            serializer2.validated_data["day"] = temp_time
                            serializer2.validated_data["routine_id"] = routine
                            serializer2.save()
                        serializer3 = RoutineResultSerializer(data=data)
                        if serializer3.is_valid():
                            serializer3.validated_data["day"] = temp_time
                            serializer3.validated_data["routine_id"] = routine
                            serializer3.save()
                    return JsonResponse(
                        {
                            "data": {"routine_id": serializer.data["routine_id"]},
                            "message": {
                                "msg": "The routine has been modified.",
                                "status": "ROUTINE_UPDATE_OK",
                            },
                        },
                        status=201,
                    )
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def delete(request, pk):
    obj = get_object_or_404(Routine, pk=pk)
    if request.method == "DELETE":
        if obj.account_id == request.user:
            obj.soft_delete()
        return HttpResponse(status=204)


@csrf_exempt
def restore(request, pk):
    obj = Routine.all_objects.get(pk=pk)
    if request.method == "POST":
        if obj.account_id == request.user:
            obj.restore()
        return HttpResponse(status=204)
