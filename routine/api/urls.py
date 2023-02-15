from django.urls import path, include
from . import views


urlpatterns = [
    path("routine/", views.CreateRoutineAPIView.as_view()),
    path("routine_detail/<int:pk>/", views.RoutineDetailAPIView.as_view()),
]
