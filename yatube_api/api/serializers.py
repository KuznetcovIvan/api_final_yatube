from rest_framework import serializers

from posts.models import Post, Group, Comment, Follow


class PostSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'following',)
        read_only_fields = ('user',)
