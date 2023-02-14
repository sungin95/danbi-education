from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


# Create your views here.
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import User
# from .serializers import UserSerializer
# from rest_framework.parsers import JSONParser
# from rest_framework.response import Response
# from rest_framework.decorators import api_view


# # account_list - 계정 전체 조회(GET), 회원가입(POST)
# # account - pk로 특정 계정 조회(GET), 수정(PUT), 삭제(DELETE)
# # login - 로그인(POST)


# @api_view(["GET", "POST"])
# def user_list(request):
#     if request.method == "GET":
#         query_set = User.objects.all()
#         serializer = UserSerializer(query_set, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# def user(request, pk):
#     obj = User.objects.get(pk=pk)

#     if request.method == "GET":
#         serializer = UserSerializer(obj)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(obj, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == "DELETE":
#         obj.delete()
#         return HttpResponse(status=204)


# @csrf_exempt
# def login(request):
#     if request.method == "POST":
#         data = JSONParser().parse(request)
#         search_email = data["email"]
#         obj = User.objects.get(email=search_email)

#         if data["password"] == obj.password:
#             return HttpResponse(status=200)
#         else:
#             return HttpResponse(status=400)