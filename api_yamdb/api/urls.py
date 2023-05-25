from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CategoryView, GenreView,
                    TitleView, UserView,
                    ReviewView, CommentView,
                    SignUpView, TokenView)


v1_router = DefaultRouter()
v1_router.register(r'categories', CategoryView, basename='category'),
v1_router.register(r'genres', GenreView, basename='genre'),
v1_router.register(r'titles', TitleView, basename='title'),
v1_router.register(r'users', UserView, basename='users'),

# Не пон почему-то в pytest стоит наименнование папки именно "reviews",
# хотя изначально хотел поставить 'review' без "s" на конце
# AssertionError: Не удалось импортировать модели из приложения reviews.
# Ошибка: No module named 'reviews'

v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewView,
                   basename='reviews'),

# Учитывая, что мы в комментах смотреть сразу отызывы, то
# пусть будет и ссылка на ревью
# И ещё в redoc указан эндпоинт на это

v1_router.register(r'titles/(?P<title_id>\d+)/reviews'
                   r'/(?P<review_id>\d+)/comments', CommentView,
                   basename='comments')


urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='get_token'),
    path('v1/auth/token/', TokenView.as_view(), name='signup')
]
