# from django_elasticsearch_dsl import Document, fields
# from django_elasticsearch_dsl.registries import registry
# from .models import Task
#
# @registry.register_document
# class TaskIndex(Document):
#     """Задаем индексы."""
#     name = fields.TextField()
#     description = fields.TextField()
#     status = fields.KeywordField()
#
#     class Index:
#         name = "tasks"
#
#     def get_object(self):
#         return Task.objects.get(id=self.meta.id)
#
# def index_exist_tasks():
#     """Индекс задач (которые уже есть)."""
#     tasks = Task.objects.all()
#     for task in tasks:
#         task_index = TaskIndex(
#             meta={'id': task.id},
#             name=task.name,
#             description=task.description,
#             status=task.status
#         )
#         task_index.save()
#
# def index_exist_tasks():
#     """Индекс задач(которые уже есть)."""
#     tasks = Task.objects.all()
#     for task in tasks:
#         task_index = TaskIndex(
#             meta={'id': task.id},
#             user=task.user.username,
#             name=task.name,
#             description=task.description,
#             status=task.status,
#             created_at=task.created_at
#         )
#         task_index.save()
