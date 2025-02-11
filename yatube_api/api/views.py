from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post, User
from .serializers import (CommentSerializers, FollowSerializers,
                          GroupSerializers, PostSerializers)


class BaseViewSet(viewsets.ModelViewSet):
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(instance)


class PostViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializers


class CommentViewSet(BaseViewSet):
    serializer_class = CommentSerializers

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializers
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.following.all()

    def perform_create(self, serializer):
        following_user = get_object_or_404(
            User, username=self.request.data['following'])
        if self.request.user == following_user:
            raise ValidationError(
                {'error': 'Нельзя подписаться на самого себя!'})
        if self.request.user.following.filter(
                following=following_user).exists():
            raise ValidationError(
                {'error': 'Вы уже подписаны на этого пользователя!'})
        serializer.save(user=self.request.user, following=following_user)
