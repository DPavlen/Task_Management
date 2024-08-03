from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .models import Task
from .documents import TaskDocument


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Task.
    """

    user = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)
    status_text = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "user",
            "name",
            "description",
            "status",
            "status_text",
            "created_at",
        )

    @staticmethod
    def get_user(instance) -> str:
        """Получаем username пользователя."""
        return instance.user.username


class TaskDocumentSerializer(DocumentSerializer):
    """
    Сериализатор для модели TaskDocument.
    """
    class Meta:
        document = TaskDocument
        fields = (
            "id",
            "user",
            "name",
            "description",
            "status",
            "created_at",
        )
