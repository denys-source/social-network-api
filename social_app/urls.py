from django.urls import include, path
from rest_framework.routers import DefaultRouter

from social_app.views import PostViewSet, like_post, unlike_post


router = DefaultRouter()
router.register("", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/like/", like_post, name="like_post"),
    path("<int:pk>/unlike/", unlike_post, name="unlike_post"),
]
