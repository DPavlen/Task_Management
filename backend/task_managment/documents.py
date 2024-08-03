from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Task


@registry.register_document
class TaskDocument(Document):
    """
    Elasticsearch документ для модели Task.
    Поля "name" и "description" проиндексированы с использованием
    стандартного анализатора(analyzer="standard",), что позволяет
    выполнять поиск по частям слов, а также точным совпадениям.
    """

    name = fields.TextField(
        analyzer="standard",
        search_analyzer="standard"
    )

    description = fields.TextField(
        analyzer="standard",
        search_analyzer="standard"
    )

    class Index:
        """Вложенный класс для определения имени и
        настроек индекса Elasticsearch.
        settings (dict): Настройки индекса, такие как количество шард и реплик!
        """
        name = "tasks"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        """
        Вложенный класс для связи с моделью Django и
        определения полей для индексации.
        """
        model = Task
        fields = []
