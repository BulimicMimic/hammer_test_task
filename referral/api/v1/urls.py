from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .auth.views import SignUpView, TokenView
from api.views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

auth_urls = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', TokenView.as_view(), name='auth_token'),
]
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls)),
]
