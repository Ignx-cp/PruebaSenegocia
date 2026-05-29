from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

from usuarios.token_views import (
    LoginThrottleTokenObtainPairView,
    RefreshThrottleTokenView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    path("api/token/", LoginThrottleTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", RefreshThrottleTokenView.as_view(), name="token_refresh"),

    path("api/", include("usuarios.urls")),
    path("api/", include("cursos.urls")),
    path("api/", include("inscripciones.urls")),
    path("api/", include("evaluaciones.urls")),
    path("api/", include("reportes.urls")),
]