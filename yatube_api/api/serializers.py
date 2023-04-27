from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField,
    CurrentUserDefault, PrimaryKeyRelatedField,
    ValidationError
)

from posts.models import User, Post, Group, Comment, Follow


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault())
    post = PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=CurrentUserDefault())
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Вы уже подписаны на данного автора')
            ),
        )

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise ValidationError(
                'Вы не можете подписаться на самого себя,'
                'даже если очень хочется'
            )
        return data
