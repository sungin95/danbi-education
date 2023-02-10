from django.db import models
from django.contrib.auth.models import AbstractUser
from routine.models import Quiz


class User(AbstractUser):
    # age = models.PositiveIntegerField()
    learning_subject = models.ManyToManyField(Quiz, related_name="learning_user")
    email = models.EmailField(unique=True)
