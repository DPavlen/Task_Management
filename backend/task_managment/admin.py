from django.contrib import admin

from task_managment.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Настроенная панель админки управления задачами.
    """

    list_display = (
        "id",
        "user",
        "name",
        "description",
        "status",
        "created_at",
    )
    search_fields = (
        "id",
        "user",
        "created_at",
    )
    list_filter = (
        "id",
        "user",
        "created_at",
    )
    empty_value_display = "-пусто-"