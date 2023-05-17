from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, Signup, GetToken

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='user')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', GetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', Signup.as_view(), name='signup'),
]