from django.urls import path, include
from . import views

urlpatterns = [
    path("create/", views.createRoutine),
    path("test/", views.test),
]
