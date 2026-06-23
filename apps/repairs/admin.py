from django.contrib import admin
from .models import ProblemCategory, Repair, RepairHistory

admin.site.register(ProblemCategory)
admin.site.register(Repair)
admin.site.register(RepairHistory)


