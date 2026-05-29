from rest_framework.routers import DefaultRouter
from evaluaciones.views import EvaluacionViewSet

router = DefaultRouter()

router.register(
    r"evaluaciones",
    EvaluacionViewSet,
    basename="evaluaciones"
)

urlpatterns = router.urls