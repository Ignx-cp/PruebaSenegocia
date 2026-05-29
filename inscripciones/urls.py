from rest_framework.routers import DefaultRouter

from .views import InscripcionViewSet

router = DefaultRouter()
router.register(r"inscripciones", InscripcionViewSet, basename="inscripciones")

urlpatterns = router.urls