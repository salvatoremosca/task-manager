from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    def get_queryset(self):
        user = self.request.user
        # only admin can see all tasks
        if user.is_staff or user.is_superuser:
            return Task.objects.all().order_by("-created_at")
        return Task.objects.filter(owner=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
