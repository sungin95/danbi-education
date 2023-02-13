from django.urls import path, include
from . import views

urlpatterns = [
    path("create/", views.createRoutine),
    path("today_todos/", views.today_todos),
    path("test/", views.test),
]
