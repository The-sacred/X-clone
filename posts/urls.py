from .views import PostListCreateView, PostDetailView, LikePostView, UnlikePostView
from django.urls import path

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    path('<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]