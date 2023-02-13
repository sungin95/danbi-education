from django.urls import path, include
from . import views

urlpatterns = [
    path("create/", views.createRoutine),
    path("today_todos/", views.today_todos),
    path("modify/<int:pk>/", views.modify),
    path("delete/<int:pk>/", views.delete),
    path("restore/<int:pk>/", views.restore),
]
