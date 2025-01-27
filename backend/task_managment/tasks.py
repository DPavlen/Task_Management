import logging
from celery import shared_task
import time

from task_managment.models import Task


@shared_task
def process_task(task_id):
    logging.info("Задача запущена")
    time.sleep(30)
    task = Task.objects.get(id=task_id)
    if task.status == "in_queue":
        task.status = "completed"
        task.kwargs = {
            "Сообщение": f"Статус задачи {task.name} у пользователя {task.user} изменен!"
        }
        task.result = "Текущий статус задачи: Завершена"
        task.save()
    logging.info("Задача завершена")