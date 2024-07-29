from django.urls import include, path
from rest_framework import routers

from task_managment.views import TaskViewSet

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]