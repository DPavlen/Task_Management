from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


COLLECT_SCHEMA = {
    "list": extend_schema(
        summary="Получить список всех задач пользователей (Необходимо авторизоваться!)",
        description="Получить список всех задач пользователей",
    ),
    "create": extend_schema(
        summary="Создание новой задачи (Необходимо аутентификация!) ",
        description=(
            "Создать новую задачу. При успешном создании задачи, "
            "она отправляется на обработку с помощью Celery и RabbitMQ, "
            "и будет доступна для мониторинга в Flower."
        ),
    ),
    "partial_update": extend_schema(
        summary="Обновить информацию о задаче частично. (Доступно только автору или админу).",
        description="Обновляет данные о задаче, например имя задачи или ее описание!"
                    "При этом автор задачи и дата создания задачи не меняются!"

    ),
    "update": extend_schema(
        summary="Обновить информацию о задаче.  (Доступно только автору или админу).",
        description="Обновляет данные о задаче, например имя задачи или ее описание!"
                    "При этом автор задачи и дата создания задачи не меняются!",
    ),
    "destroy": extend_schema(
        summary="Удаляет текущую задачу (Доступно только автору или админу)",
        description="Удаляет текущую задачу!",
    ),
    "retrieve": extend_schema(
        summary="Получить информацию о задаче по ID. (Доступно только автору или админу).",
        description="Получить информацию о задаче по его ID. Возвращает "
        "информацию о конкретном запрошенной задаче!"
    ),
}

TASK_DOCUMENT_VIEWSET_SCHEMA = {
    "list": extend_schema(
        summary="Поиск задач по названию(name) и описанию(description) через Elasticsearch",
        description="Позволяет осуществлять поиск задач по частям слова в полях 'name' и 'description'.",
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Поиск по частям слова в полях 'name' и 'description'.",
            ),
        ],
    ),
    "retrieve": extend_schema(
        summary="Получить информацию о задаче по ID.",
        description="Получить информацию о задаче по его ID. Возвращает "
        "информацию о конкретном запрошенной задаче!"
    ),
}
