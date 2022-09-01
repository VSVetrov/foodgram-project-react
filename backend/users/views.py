from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.pagination import CustomPageNumberPagination
from api.permissions import IsAuthorOrAdminOrReadOnly

from .models import Follow
from .serializers import SubscriptionSerializer, UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            following__user=self.request.user
        )
        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = SubscriptionSerializer(
                page,
                context={'request': request},
                many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionSerializer(
            subscriptions,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if request.method == "POST":
            if_already_exists = Follow.objects.filter(
                user=request.user,
                author=author
            ).exists()
            if if_already_exists or request.user == author:
                return Response(
                    {'errors': ('Вы уже подписаны или пытаетесь '
                                'подписаться на самого себя')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(user=request.user, author=author)
            serializer = SubscriptionSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                Follow,
                user=request.user,
                author=author
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
