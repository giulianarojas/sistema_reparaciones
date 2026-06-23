from rest_framework import serializers
from .models import ProblemCategory, Repair, RepairHistory

class ProblemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCategory
        fields = "_all_"


class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = "_all_"

class RepairHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairHistory
        fields = "_all_"
