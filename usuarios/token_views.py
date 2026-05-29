from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class LoginThrottleTokenObtainPairView(TokenObtainPairView):
    throttle_scope = "login"


class RefreshThrottleTokenView(TokenRefreshView):
    throttle_scope = "token_refresh"