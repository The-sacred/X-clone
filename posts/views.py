from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

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