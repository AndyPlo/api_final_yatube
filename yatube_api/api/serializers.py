from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post, Group, Follow, User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True,
                            default=serializers.CurrentUserDefault())
    following = serializers.SlugField()

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        following = get_object_or_404(User, username=data['following'])
        if Follow.objects.filter(user=self.context['request'].user,
                                 following=following).exists():
            raise serializers.ValidationError(
                'You have already followed this user!'
            )
        if self.context['request'].user == following:
            raise serializers.ValidationError(
                'You cannot follow youself!'
            )
        return data

    def create(self, validated_data):
        following = get_object_or_404(
            User,
            username=validated_data['following']
        )
        return Follow.objects.create(
            user=self.context['request'].user,
            following=following
        )
