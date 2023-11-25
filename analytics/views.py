from datetime import datetime

from django.utils import timezone
from django.db.models import F, Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import status

from social_app.models import Like


def is_date_correct(date_str: str) -> bool:
    try:
        return bool(datetime.strptime(date_str, "%Y-%m-%d"))
    except ValueError:
        return False


class LikesAnalytics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        date_from = request.query_params.get(
            "date_from", str(timezone.now().date())
        )
        date_to = request.query_params.get(
            "date_to", str(timezone.now().date())
        )

        if not (is_date_correct(date_from) and is_date_correct(date_to)):
            return Response(
                {
                    "message": "Date format is incorrect. Has to be in format YYYY-MM-DD"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = (
            Like.objects.filter(created_at__date__range=[date_from, date_to])
            .values(date=F("created_at__date"))
            .order_by("-date")
            .annotate(likes_count=Count("id"))
        )
        return Response(list(data), status=status.HTTP_200_OK)


class UserAnalytics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        data = {
            "last_login": request.user.last_login.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "last_active": request.user.last_active.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        return Response(data, status=status.HTTP_200_OK)
