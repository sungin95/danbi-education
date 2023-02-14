from django.urls import path, include
from .views import RegistrationAPIView


urlpatterns = [
    path("register", RegistrationAPIView.as_view()),
]


# from django.urls import path
# from .api import views
# from django.conf.urls import include

# urlpatterns = [
#     path("", include("dj_rest_auth.urls")),  # 해당 라인 추가
#     path("registration/", include("dj_rest_auth.registration.urls")),
# ]