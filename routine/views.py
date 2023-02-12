from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Routine
from .serializers import RoutineSerializer, RoutineDaySerializer
from rest_framework.parsers import JSONParser

from rest_framework.fields import CurrentUserDefault
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from datetime import datetime, timedelta

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
def createRoutine(request):
    if request.method == "POST":
        # request를 parse와 JSONParser를 거쳐서 딕셔너리 형태로 data가 완성된다.
        data = JSONParser().parse(request)
        serializer = RoutineSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data["account_id"] = request.user
            serializer.validated_data["days"] = str(data["days"])
            serializer.save()
            # 루틴 생성과 루틴 데이들을 생성해야 한다.
            today = datetime.today().weekday() + 1
            now = datetime.now()
            week = now + timedelta(weeks=0, days=-(today % 7))
            routine = Routine.objects.get(pk=serializer["pk"].value)
            for d in data["days"]:
                temp = week + timedelta(days=week_day[d])
                temp_time = temp.strftime("%Y-%m-%d")

                serializer2 = RoutineDaySerializer(data=data)
                if serializer2.is_valid():
                    serializer2.validated_data["day"] = temp_time
                    serializer2.validated_data["routine_id"] = routine
                    serializer2.save()
            return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


def test(request):
    print(request.user)
    return


# @api_view(["GET"])
# def randomQuiz(reuest, id):
#     totalQuizs = Quiz.objects.all()
#     randomQuizs = random.sample(list(totalQuizs), id)
#     serializer = QuizSerializer(randomQuizs, many=True)
#     return Response(serializer.data)
