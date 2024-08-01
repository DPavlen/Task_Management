from django.urls import include, path
from rest_framework import routers

from task_managment.views import TaskViewSet, TaskDocumentViewSet


router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"task-documents", TaskDocumentViewSet, basename="task-documents")


urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    # path("search/", TaskDocumentViewSet.as_view({"get": "list"}), name="task-search"),
]