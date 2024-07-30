from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Task
# from .search_indexes import TaskDocument
#
#
# @receiver(post_save, sender=Task)
# def index_task(sender, instance, **kwargs):
#     task = TaskDocument(
#         meta={'id': instance.id},
#         name=instance.name,
#         description=instance.description,
#         status=instance.status,
#         created_at=instance.created_at,
#     )
#     task.save()
