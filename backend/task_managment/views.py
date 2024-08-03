from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    CompoundSearchFilterBackend
)

from .models import Task
from .documents import TaskDocument
from .permissions import IsOwnerOrReadOnlyOrAdmin
from .schemas import COLLECT_SCHEMA, TASK_DOCUMENT_VIEWSET_SCHEMA
from .serializers import TaskSerializer, TaskDocumentSerializer
from task_managment.tasks import process_task


@extend_schema_view(**COLLECT_SCHEMA)
class TaskViewSet(viewsets.ModelViewSet):
    """
    Кастомный ViewSet задач.
    """
    queryset = Task.objects.select_related("user").all()
    serializer_class = TaskSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        """
        Возвращает соответствующие разрешения в зависимости от действия.
        """

        action_permissions = {
            "list": (IsOwnerOrReadOnlyOrAdmin(),),
            "retrieve": (IsOwnerOrReadOnlyOrAdmin(),),
            "create": (IsAuthenticated(),),
            "update": (IsOwnerOrReadOnlyOrAdmin(),),
            "partial_update": (IsOwnerOrReadOnlyOrAdmin(),),
            "destroy": (IsOwnerOrReadOnlyOrAdmin(),),
        }
        return action_permissions.get(self.action, super().get_permissions())

    def get_queryset(self):
        """
        QuerySet, отфильтрованный по текущему пользователю.
        Если не авторизован, то выдаем сообщение.
        """

        user = self.request.user
        if user.is_authenticated:
            return super().get_queryset().filter(user=user)
        else:
            raise PermissionDenied("Необходимо авторизоваться!")

    def list(self, request, *args, **kwargs):
        """
        Возвращает список задач.
        """
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Создание новой задачи.
        """
        try:
            serializer.save(user=self.request.user)
            task_id = serializer.instance.id
            process_task.delay(task_id)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        """
        Обновляет данные о задаче.
        """
        try:
            task = serializer.instance
            if self.request.user == task.user:
                serializer.save(
                    user=task.user,
                    created_at=task.created_at,
                )
            else:
                serializer.save()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        """
        Удаляет текущую задачу.
        """
        try:
            instance.delete()

        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(**TASK_DOCUMENT_VIEWSET_SCHEMA)
class TaskDocumentViewSet(DocumentViewSet):
    """Кастомный viewset для TaskDocument (Elasticsearch)."""
    document = TaskDocument
    serializer_class = TaskDocumentSerializer
    # lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        #SearchFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
    ]
    # Define search fields
    search_fields = ("name", "description",)
    filter_fields = {
        "name": "name",
        "description": "description",
    }
    ordering_fields = {
        "created_at": "created_at",
    }
    ordering = ("created_at",)