from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated  # 모든사람, 로그인한 사용자만
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
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


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    # 1.
    def get(self, request, *args, **kwargs):
        # 2.
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 3.
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        # 4.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        # 5.
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# 1.
# 2. 단순히 User객체를 client에게 보내주기 위한 serializer
# 3. update관련 부분
# 4. request.user가 인스턴스, data가 속성명과 속성값, partial=True는 부분 수정 허용
# 5. 저장
