from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from bakersoft.trackings.views import ProjectViewSet, WorkViewSet
from bakersoft.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet)
router.register("works", WorkViewSet)


app_name = "api"
urlpatterns = router.urls
