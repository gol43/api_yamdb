from rest_framework import serializers
from reviews.validators import validate_username
from rest_framework.validators import UniqueValidator

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())],
        required=True,
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            validate_username
        ]
    )
    email = serializers.EmailField(
        validators=[
            validate_username
        ]
    )

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']
        ordering = ['username']
