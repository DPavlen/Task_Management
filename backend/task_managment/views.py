from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION,
    FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    DefaultOrderingFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
    FunctionalSuggesterFilterBackend,
    CompoundSearchFilterBackend
)

from .models import Task
from .documents import TaskDocument
from .permissions import IsOwnerOrReadOnlyOrAdmin
from .schemas import COLLECT_SCHEMA
from .serializers import TaskSerializer, TaskDocumentSerializer
from task_managment.tasks import process_task


@extend_schema_view(**COLLECT_SCHEMA)
class TaskViewSet(viewsets.ModelViewSet):
    """
    Кастомный ViewSet задач.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

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


class TaskDocumentViewSet(DocumentViewSet):
    document = TaskDocument
    serializer_class = TaskDocumentSerializer
    lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
        OrderingFilterBackend,
        # CompoundSearchFilterBackend
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

    # Suggester fields
    suggester_fields = {
        'name_suggest': {
            'field': 'name.suggest',
            'suggesters': [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
        },
        'salutation.suggest': {
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
        },
    }

    # Functional suggester fields
    functional_suggester_fields = {
        'name_suggest': {
            'field': 'name.raw',
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            # 'serializer_field': 'name',
        },
        'salutation_suggest': {
            'field': 'salutation.raw',
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            # 'serializer_field': 'salutation',
        },
        'salutation.raw': {
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            # 'serializer_field': 'salutation',
        },
    }