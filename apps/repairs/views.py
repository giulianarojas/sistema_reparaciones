from rest_framework import viewsets

from .models import ProblemCategory, Repair, RepairHistory

from .serializers import (
    ProblemCategorySerializer,
    RepairSerializer,
    RepairHistorySerializer
)

class ProblemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProblemCategory.objects.all()
    serializer_class = ProblemCategorySerializer


class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer

class RepairHistoryViewSet(viewsets.ModelViewSet):
    queryset = RepairHistory.objects.all()
    serializer_class = RepairHistorySerializer