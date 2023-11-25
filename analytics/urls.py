from django.urls import path

from analytics.views import LikesAnalytics


urlpatterns = [
    path("", LikesAnalytics.as_view(), name="likes_analytics"),
]
