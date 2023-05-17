from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import default_token_generator
from reviews.models import User
from django.conf import settings
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from .permissions import AdminOrReadOnlyPermission, AdminOnlyPermission, IsAdminModeratorOwnerOrReadOnly
from .serializers import UserSerializer, UserEditSerializer, SignupSerializer, TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, AdminOnlyPermission)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET', 'PATCH'], detail=False, permission_classes=(permissions.IsAuthenticated,), url_path='me')
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
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({'username': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
