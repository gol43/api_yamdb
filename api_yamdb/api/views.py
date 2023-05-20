from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from .check import check_confirmation_code

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from .permissions import AdminOnlyPermission
from .serializers import UserSerializer, UserEditSerializer, SignupSerializer, TokenSerializer



class UserViewSet(viewsets.ModelViewSet):
    '''API для работы с пользователями'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, AdminOnlyPermission)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(permissions.IsAuthenticated,), url_path='me')
    def get_current_user_info(self, request):
        user = request.user
        if request.method == 'PATCH':
            if user.is_admin:
                serializer = UserSerializer(request.user, data=request.data, partial=True)
            else:
                serializer = UserEditSerializer(request.user, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        else:
            serializer = UserSerializer(user)
        return Response(serializer.data)


class Signup(APIView):
    '''API для регистрации пользователей'''
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(username__iexact=username, email__iexact=email)
        except ObjectDoesNotExist:
            user_serializer = SignupSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        confirmation = default_token_generator.make_token(user)
        message_code = 'Ваш код для получения API токена'
        message = f'Код подтверждения - {confirmation}'
        send_mail(message_code, message, settings.DEFAULT_FROM_EMAIL, (email,))
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class GetToken(TokenRefreshView):
    ''' Получение JWT-токена за место username и confirmation_code. '''
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if check_confirmation_code(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': ['Код не действителен!']},
            status=status.HTTP_400_BAD_REQUEST
        )
