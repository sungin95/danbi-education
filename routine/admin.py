from django.contrib import admin
from .models import Routine, RoutineDay, RoutineResult

# Register your models here.
admin.site.register(Routine)
admin.site.register(RoutineDay)
admin.site.register(RoutineResult)
