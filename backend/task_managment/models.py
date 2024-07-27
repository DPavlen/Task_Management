import uuid

from django.db import models

from users.models import CustUser


class Task(models.Model):
    """
    Модель управления задачами.
    """

    STATUS_CHOICES = (
        ("in_queue", "В очереди"),
        ("in_process", "В процессе"),
        ("completed", "Завершена"),
    )
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        CustUser,
        on_delete=models.CASCADE,
        related_name="user_task",
        verbose_name="Пользователь задачи"
    )
    name = models.CharField(
        "Название задачи",
        max_length=150,
        unique=True,
    )
    description = models.TextField(
        "Описание"
    )
    status = models.CharField(
        "Статус задачи",
        max_length=50,
        choices=STATUS_CHOICES,
        default="in_queue",
    )
    created_at = models.DateTimeField(
        "Дата и время создания задачи",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ("name",)

    def __str__(self):
        return self.name
