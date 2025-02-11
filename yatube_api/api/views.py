from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Group
from .serializers import (PostSerializers, GroupSerializers,
                          CommentSerializers, FollowSerializers)


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


class FollowViewSet(BaseViewSet):
    serializer_class = FollowSerializers

    def get_queryset(self):
        return self.request.user.followers.all()
