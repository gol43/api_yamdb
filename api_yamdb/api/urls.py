from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, Signup, GetToken

v1_router = DefaultRouter()
v1_router.register(r"users", UserViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup', Signup, name='signup'),
    path('v1/auth/token/', GetToken, name='get_token'),
]
