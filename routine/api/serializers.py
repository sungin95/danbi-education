from rest_framework import serializers
from routine.models import Routine, RoutineDay, RoutineResult


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ("title", "category", "goal", "is_alarm", "routine_id")


class RoutineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ("title", "category", "goal", "is_alarm", "routine_id")

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineDay
        fields = ("pk",)


class RoutineResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = ("pk",)
