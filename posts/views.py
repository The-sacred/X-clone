from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post, Like
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_deleted=False, parent=None).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save() 


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, is_deleted=False)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"message": "Already liked"}, status=400)

        return Response({"message": "Post liked"}, status=201)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        try:
            like = Like.objects.get(user=request.user, post_id=post_id)
            like.delete()
            return Response({"message": "Post unliked"}, status=200)
        except Like.DoesNotExist:
            return Response({"error": "You haven't liked this post"}, status=400)

