from rest_framework import serializers
from .models import Post
from users.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'created_at', 'updated_at', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return PostSerializer(obj.replies.filter(is_deleted=False), many=True).data
        return [] 




