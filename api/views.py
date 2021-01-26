from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from .serializers import CommentSerializer, PostSerializer, FollowerSerializer, GroupSerializer
from .models import Post, Follow, Group, Comment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    filterset_fields = ('group',)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['following']
    search_fields = ['following__username', 'user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)


class GroupViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Group.objects.all()
    search_fields = ['user__username']
    http_method_names = ['get', 'post']
