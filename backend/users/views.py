from api.pagination_limit import LimitPageNumberPagination
from api.serializers import FollowSerializer
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет обработки подписки юзеров."""
    pagination_class = LimitPageNumberPagination

    @action(
        permission_classes=[IsAuthenticated],
        detail=True,
        methods=['post']
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            responce_data = {
                'errors': 'Нельзя подписаться на сомого себя!',
            }
            return Response(
                data=responce_data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Subscription.objects.filter(user=user, author=author).exists():
            responce_data = {
                'errors': 'Вы уже подписаны на этого автора!'
            }
            return Response(
                data=responce_data,
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = Subscription.objects.create(user=user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(permission_classes=[IsAuthenticated], detail=False)
    def subscriptions(self, request):
        user = request.user
        query = Subscription.objects.filter(user=user)
        num_pages = self.paginate_queryset(query)
        serializer = FollowSerializer(
            num_pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @subscribe.mapping.delete
    def unfollow(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            responce_data = {
                'errors': 'Нельзя отписаться от себя'
            }
            return Response(
                data=responce_data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subscription = Subscription.objects.get(user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            responce_data = {
                'errors': 'Подписка не найдена'
            }
            return Response(
                data=responce_data,
                status=status.HTTP_404_NOT_FOUND,
            )
