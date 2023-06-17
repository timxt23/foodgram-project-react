from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Subscription

User = get_user_model()


class CustomCreateUserSerializer(UserCreateSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'password', 'first_name', 'last_name'
        )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class CustomUserSerializer(UserSerializer):
    """Проверка на уже существуюшую подписку юзера."""
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'is_following',
        )
        read_only_fields = 'is_following',

    def get_is_following(self, obj):
        cheking_user = self.context.get('request').user
        if not cheking_user.is_anonymous:
            return Subscription.objects.filter(
                user=cheking_user,
                author=obj.id
            ).exists()
        return False
