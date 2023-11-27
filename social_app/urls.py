from django.urls import include, path
from rest_framework.routers import DefaultRouter

from social_app.views import (
    LikePostView,
    PostViewSet,
    UnlikePostView,
)


router = DefaultRouter()
router.register("", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/like/", LikePostView.as_view(), name="like_post"),
    path("<int:pk>/unlike/", UnlikePostView.as_view(), name="unlike_post"),
]

app_name = "social_app"
