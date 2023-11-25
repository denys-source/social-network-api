from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import status

from social_app.models import Like, Post
from social_app.permissions import IsOwnerOrAdminElseReadOnly
from social_app.serializers import (
    PostDetailSerializer,
    PostListSerializer,
    PostSerializer,
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrAdminElseReadOnly]

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related("user")

        if self.action in ("list", "retrieve"):
            queryset = queryset.annotate(likes_count=Count("likes"))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
def like_post(request: Request, pk: int) -> Response:
    post = get_object_or_404(Post, pk=pk)
    _, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def unlike_post(request: Request, pk: int) -> Response:
    post = get_object_or_404(Post, pk=pk)
    Like.objects.filter(user=request.user, post=post).delete()
    return Response(status=status.HTTP_200_OK)
