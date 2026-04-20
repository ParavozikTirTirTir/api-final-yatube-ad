from rest_framework import serializers
from posts.models import Post, Comment, Group, Follow
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('id', 'author', 'created', 'post')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        request = self.context.get('request')
        if request and value == request.user:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя"
            )
        if request and Follow.objects.filter(
            user=request.user, following=value
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя"
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)
