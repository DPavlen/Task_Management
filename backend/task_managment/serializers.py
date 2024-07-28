from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """."""
    user = serializers.SerializerMethodField()
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
    def get_user(instance):
        """Получаем username пользователя."""
        return instance.user.username
