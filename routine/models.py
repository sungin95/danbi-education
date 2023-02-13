from django.db import models
from django.conf import settings

category_CHOICES = (
    ("기상", "기상"),
    ("HOMEWORK", "HOMEWORK"),
)


class Routine(models.Model):
    # routine_id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=category_CHOICES)
    goal = models.CharField(max_length=150)
    # 알람 on off
    is_alarm = models.BooleanField(default=True)
    # 삭제를 할려면 True로
    is_deleted = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # JSON으로 받으면 문자열로 받아야 하니까
    days = models.CharField(max_length=70)


result_CHOICES = (
    ("NOT", "NOT(안함)"),
    ("TRY", "TRY(시도)"),
    ("DONE", "DONE(완료)"),
)


class RoutineResult(models.Model):
    # routine_result_id = models.AutoField(primary_key=True)
    # 일정 끝난 다음날 체크
    day = models.DateField()
    routine_id = models.ForeignKey("Routine", on_delete=models.CASCADE)
    result = models.CharField(max_length=50, default="NOT")
    # 삭제
    is_deleted = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class RoutineDay(models.Model):
    day = models.DateField()
    routine_id = models.ForeignKey("Routine", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
