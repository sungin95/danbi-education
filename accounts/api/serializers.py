from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from django.utils import timezone


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "phone_number", "password", "token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # 1.
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)

    # 2.
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        # 3.
        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        # 4.
        user = authenticate(username=email, password=password)

        # 5.
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found"
            )

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        # 6.
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # 7.
        return {
            "email": user.email,
            "username": user.username,
            "last_login": user.last_login,
        }


# 1. read_only는 전송만 가능하게 하기 위해
# write_only는 수정만 가능하게(아마 비밀번호는 암호화 하는 과정을 거쳐야 되기 때문에 수정이 필요한거 같다. )
# 2. 검증
# 3. 이메일 or 비밀번호 둘 다 입력 했니?
# 4. 데이터 베이스에서 검증(검증이 안되면 None 반환)
# 5. None이면 돌려 보냄
# 6. 통과 되었고 마지막 로그인 시간 최신화
# 7. 값 리턴


# 1.
class UserSerializer(serializers.ModelSerializer):
    # 2.
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "token"]

        # 3.
        read_only_fields = ("token",)

    # 4.
    def update(self, instance, validated_data):
        # 5.
        password = validated_data.pop("password", None)

        # 6.
        for key, value in validated_data.items():
            # 7.
            setattr(instance, key, value)

        if password is not None:
            # 8.
            instance.set_password(password)

        # 9.
        instance.save()

        return instance


# 1.?
# 2.
# 3. 앞에 케이스는 max_length같은 옵션을 설정해 줘야 했지만 토큰은 road_only 옵션 한개면 되므로, ;read_only_fields'만 주었다.
# 4. update할때 사용
# 5. setattr는 setattr(객체(인스턴스), 속성명(필드 이름), 속성값) 구조로 하면 해당 속성명의 속성값을 바꾸어 주는 함수이다.
# 비밀번호는 setatter같은 함수는 사용 못하고 따로 정해진 함수를 사용해야 한다.(set_password)
# 6.
# 7. setattr를 활용하여 값을 바꾸어 준다.
# 8. set_password 메서드를 활용하여 password를 변경해 준다.
# 9. 저장
