from django.apps import AppConfig


class TaskManagmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task_managment"
    verbose_name = "Управление задачами"

    def ready(self):
        """"
        Регистрируем сигналы при запуске app task_managment.
        """

        import task_managment.signals