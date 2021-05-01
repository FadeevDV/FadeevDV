from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateToken, CustomUserCreateViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'auth/email', CustomUserCreateViewSet)

urlpatterns = [
    path('v1/auth/token/', CreateToken.as_view()),
    path('v1/', include(router.urls)),
]
