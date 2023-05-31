from reviews.models import Title, Category, Genre, User, Review, Comment
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, TitleObjectsSerializer,
                          UserSerializer, OwnerSerializer,
                          ReviewSerializer, CommentSerializer,
                          SignUpSerializer, TokenSerializer)
from .permissions import (AdminPermission, AdminAndRead,
                          ForAllAndRead)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.db.models import Avg
from .filters import TitleFilter
from .mixins import MixinVeiew
from rest_framework import filters, generics, status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

# https://www.django-rest-framework.org/api-guide/generic-views/
# Михины взял из документации
# Используется для конечных точек для удаления и
# чтения для представления экземпляров модели


class CategoryView(MixinVeiew):
    """Get list of Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminAndRead, )

    # lookup нужен для запроса DELETE

    filter_backends = (filters.SearchFilter, )
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreView(MixinVeiew):
    """Get list of Genre"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminAndRead, )
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleView(viewsets.ModelViewSet):
    """Get list of Title"""

    # Из pytest и redoc понял, что для
    # поля rating нужно получить среднее значение

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-id')
    serializer_class = TitleSerializer
    permission_classes = (AdminAndRead, )

    # фильтры для правильной работы genre в эндпоинтах(для slug)

    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    # Может быть переопределен для обеспечения динамического поведения,
    # например использования разных сериализаторов для операций чтения и
    # записи или предоставления разных
    # сериализаторов разным типам пользователей.
    # https://www.django-rest-framework.org/api-guide/generic-views/

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleObjectsSerializer
        return TitleSerializer


class UserView(viewsets.ModelViewSet):
    """Get list of User"""
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = (AdminPermission, )
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'username'
    search_fields = ('=username',)

    # Провекра данных для эндпоинта

    http_method_names = ['get',
                         'post',
                         'patch',
                         'delete']

    # https://www.django-rest-framework.org/api-guide/viewsets/
    # @action для мушратизации доп действий, которые доступны
    # только для auth

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='me')
    def edit_profile(self, request):
        """Edit for user-author"""
        if request.method == 'PATCH':
            serializer = OwnerSerializer(
                self.request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = OwnerSerializer(self.request.user)
        return Response(serializer.data)


class ReviewView(viewsets.ModelViewSet):
    """Get list of Reviews"""
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          ForAllAndRead, )

    def get_queryset(self):
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return title.reviews.all()

    # https://stackoverflow.com/questions/
    # 17813919/django-error-matching-query-does-not-exist

    def perform_create(self, serializer):
        try:
            title = get_object_or_404(Title,
                                      id=self.kwargs.get('title_id'))
        except Title.DoesNotExist:
            title = None
        return serializer.save(author=self.request.user, title=title)


class CommentView(viewsets.ModelViewSet):
    """Get list of Comments"""
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = (ForAllAndRead,
                          IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        review = Review.objects.get(pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        try:
            review = get_object_or_404(Review,
                                       title__id=self.kwargs.get('title_id'),
                                       id=self.kwargs.get('review_id'))
        except Review.DoesNotExist:
            review = None
        serializer.save(author=self.request.user, review=review)


class SignUpView(generics.CreateAPIView):
    """Signup new user with nick and mail"""
    queryset = User.objects.all().order_by('-id')
    serializer_class = SignUpSerializer

    # Каждый может зарегаться у нас

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        # if not serializer.is_valid():
        #     raise ValidationError(serializer.errors)
        # Пытались реализовать этот типичный метод проверки сериализатора
        # Но что-то было сложно его впихнуть

        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email)

        # https://docs.djangoproject.com/en/4.2/topics/email/

        send_mail(
            subject='Get ur code for confrimation',
            message='Look ur code for confirmation',
            from_email=settings.EMAIL_ADMIN,
            recipient_list=[user.email],
            fail_silently=False,
            auth_user=None,
            auth_password=None,
            connection=None,
            html_message=None)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(generics.CreateAPIView):
    """Get token of user"""
    queryset = User.objects.all().order_by('-id')
    serializer_class = TokenSerializer

    # Также каждый может получить токен

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        # та же самая история про сериализатор

        serializer.is_valid(raise_exception=True)

        # Проверьте, что POST-запрос
        # с корректным `username` и невалидным `confirmation_code`

        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirm')

        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user)
            return Response({'token': f'{token}'},
                            status.HTTP_200_OK)
        return Response({'subject': 'Smth went wrong with token'},
                        status.HTTP_400_BAD_REQUEST)
