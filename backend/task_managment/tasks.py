from celery import shared_task
import time

from task_managment.models import Task


@shared_task
def process_task(self, task_id):
    time.sleep(10)
    task = Task.objects.get(id=task_id)
    if task.status == "in_queue":
        task.status = "completed"
        # task.kwargs = {
        #     "Сообщение": f"Статус задачи {self.task.name} у пользователя {self.task.user} изменен!"
        # }
        # task.result = "Текущий статус задачи Завершена"
        task.save()