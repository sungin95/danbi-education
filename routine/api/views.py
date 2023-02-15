from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Routine, RoutineDay, RoutineResult
from .serializers import (
    RoutineSerializer,
    RoutineDaySerializer,
    RoutineResultSerializer,
)
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta

from rest_framework.permissions import AllowAny, IsAuthenticated  # 모든사람, 로그인한 사용자만
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

# from .renderers import RoutineJSONRenderer
from rest_framework import status
from django.http import Http404


# 중복된 내용 이므로 함수화
def create_day_result(serializer, data):
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


class CreateRoutineAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoutineSerializer
    # renderer_classes = (RoutineJSONRenderer,)

    def post(self, request):
        data = JSONParser().parse(request)

        serializer = self.serializer_class(data=data)
        # create Routine
        if serializer.is_valid():
            serializer.validated_data["account_id"] = request.user
            serializer.validated_data["days"] = str(data["days"])
            serializer.save()
            create_day_result(serializer, data)
            return Response(
                {
                    "data": {"routine_id": serializer.data["routine_id"]},
                    "message": {
                        "msg": "You have successfully created the routine.",
                        "status": "ROUTINE_CREATE_OK",
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response("valid errors", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
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
            },
            status=status.HTTP_201_CREATED,
        )


class RoutineDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoutineSerializer
    # renderer_classes = (RoutineJSONRenderer,)

    def get_object(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        # 수정
        obj = self.get_object(pk)
        if obj.account_id == request.user:
            if request.method == "PUT":
                data = JSONParser().parse(request)
                if str(data["days"]) == obj.days:
                    serializer = RoutineSerializer(obj, data=data)
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
                        create_day_result(serializer, data)
                        return Response(
                            {
                                "data": {"routine_id": serializer.data["routine_id"]},
                                "message": {
                                    "msg": "The routine has been modified.",
                                    "status": "ROUTINE_UPDATE_OK",
                                },
                            },
                            status=201,
                        )
        return Response("errors", status=400)

    @api_view(["POST"])
    def delete(request, pk):
        obj = get_object_or_404(Routine, pk=pk)
        if request.method == "DELETE":
            if obj.account_id == request.user:
                obj.soft_delete()
            return HttpResponse(status=204)

    @api_view(["POST"])
    def restore(request, pk):
        obj = Routine.all_objects.get(pk=pk)
        if request.method == "POST":
            if obj.account_id == request.user:
                obj.restore()
            return HttpResponse(status=204)
