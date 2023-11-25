from django.urls import path

from analytics.views import LikesAnalytics, UserAnalytics


urlpatterns = [
    path("", LikesAnalytics.as_view(), name="likes_analytics"),
    path("user/", UserAnalytics.as_view(), name="user_analytics"),
]
