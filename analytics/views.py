from datetime import datetime

from django.utils import timezone
from django.db.models import F, Count
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "date_from",
                description="Start date to use for filtering. Format: YYYY-MM-DD",
                type={"type": "date"},
            ),
            OpenApiParameter(
                "date_to",
                description="End date to use for filtering (inclusive). Format: YYYY-MM-DD",
                type={"type": "date"},
            ),
        ],
        responses={
            200: inline_serializer(
                name="LikesAnalyticsResponse",
                fields={
                    "date": serializers.DateField(),
                    "likes_count": serializers.IntegerField(),
                },
            ),
            400: OpenApiResponse(
                description="Date format is incorrect. Has to be in format YYYY-MM-DD"
            ),
        },
    )
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

    @extend_schema(
        responses={
            200: inline_serializer(
                name="UserAnalyticsResponse",
                fields={
                    "last_login": serializers.CharField(),
                    "last_active": serializers.CharField(),
                },
            )
        },
        examples=[
            OpenApiExample(
                name="Example",
                value={
                    "last_login": "2023-01-01 12:00:00",
                    "last_active": "2023-01-01 12:00:00",
                },
            )
        ],
    )
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
