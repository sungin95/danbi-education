from rest_framework import serializers
from .models import Routine, RoutineDay


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ("title", "category", "goal", "is_alarm", "pk")


class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineDay
        fields = ("pk",)
