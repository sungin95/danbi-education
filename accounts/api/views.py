from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, LoginSerializer
from .renderers import UserJSONRenderer


# Create your views here.
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    # 1.
    def post(self, request):
        # 2.
        user = request.data

        # 3.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        # 4.
        return Response(serializer.data, status=status.HTTP_200_OK)


# 1. def post는 자동으로 실행되는 건가?
# 2. 받은 정보를 user로 넣어 준다.
# 3. 아까 만든 LoginSerializer로 보내 검증을 한다.
# 4. 검증 성공하면 정보 반환
