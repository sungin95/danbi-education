from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path("accounts", views.user_list),
    path("accounts/<int:pk>", views.user),
    path("login", views.login),
    path("auth", include("rest_framework.urls", namespace="rest_framework")),
]
