from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from .documents import TaskDocument
from django_elasticsearch_dsl.registries import registry


@receiver(post_save, sender=Task)
def update_task_index(sender, instance, **kwargs):
    """
    Обеспечить индексацию задач при создании и обновлении.
    """

    registry.update(instance)