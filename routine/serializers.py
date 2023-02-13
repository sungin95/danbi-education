from rest_framework import serializers
from .models import Routine, RoutineDay, RoutineResult


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ("title", "category", "goal", "is_alarm", "routine_id")


class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineDay
        fields = ("pk",)


class RoutineResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = ("pk",)
