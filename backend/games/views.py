from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Match, Tournament

from .serializers import (
    MatchCreationRequestSerializer,
    MatchResponseSerializer,
    TournamentCreationRequestSerializer,
    TournamentResponseSerializer,
    TournamentRankingResponseSerializer
)

class MatchViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing matches.
    """

    @extend_schema(
        summary="Create a new match",
        description="Create a new match by providing necessary details.",
        request=MatchCreationRequestSerializer,
        responses={
            201: MatchResponseSerializer,
            400: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Match"]
    )
    def create(self, request):
        return Response({"message": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Retrieve matches with filters",
        description="Retrieve a list of matches, with optional filters, sorting, and pagination.",
        parameters=[
            OpenApiParameter(name='user_id', description="Filter matches by user ID", required=False, type=int),
            OpenApiParameter(name='rival_id', description="Filter matches by rival user ID", required=False, type=int),
            OpenApiParameter(name='result', description="Filter matches by result (win or lose)", required=False, type=str, enum=['win', 'lose']),
            OpenApiParameter(name='match_type', description="Filter matches by match type (single or tournament)", required=False, type=str, enum=['single', 'tournament']),
            OpenApiParameter(name='start_date', description="Filter matches that started after this date", required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='end_date', description="Filter matches that ended before this date", required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='page', description="Page number for pagination", required=False, type=int, default=1),
            OpenApiParameter(name='limit', description="Number of results per page", required=False, type=int, default=10),
            OpenApiParameter(name='sort_by', description="Sort matches by a specific field (start_time, end_time, or grade)", required=False, type=str, enum=['start_time', 'end_time', 'grade'], default='start_time'),
            OpenApiParameter(name='order', description="Order of sorting (ascending or descending)", required=False, type=str, enum=['asc', 'desc'], default='desc'),
        ],
        responses={
            200: MatchResponseSerializer(many=True),
            400: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Match"]
    )
    def list(self, request):
        # You would add filtering, sorting, and pagination here
        pass

    @extend_schema(
        summary="Retrieve a specific match",
        description="Retrieve a specific match by its ID.",
        parameters=[
            OpenApiParameter(name='match_id', description="ID of the match to retrieve", required=True, type=int),
        ],
        responses={
            200: MatchResponseSerializer,
            404: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Match"]
    )
    def retrieve(self, request, pk=None):
        return Response({"message": "Match not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Update a match",
        description="Update a match by providing the match ID and the updated data.",
        parameters=[
            OpenApiParameter(name='match_id', description="ID of the match to update", required=True, type=int),
        ],
        request=MatchCreationRequestSerializer,
        responses={
            200: MatchResponseSerializer,
            400: OpenApiTypes.OBJECT,  # Return an object with an error message
            404: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Match"]
    )
    def update(self, request, pk=None):
        return Response({"message": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Match not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Delete a match",
        description="Delete a match by its ID.",
        parameters=[
            OpenApiParameter(name='match_id', description="ID of the match to delete", required=True, type=int),
        ],
        responses={
            204: None,
            404: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Match"]
    )
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Match not found"}, status=status.HTTP_404_NOT_FOUND)
    
class TournamentViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing tournaments.
    """

    @extend_schema(
        summary="Create a new tournament",
        description="Create a new tournament by providing necessary details.",
        request=TournamentCreationRequestSerializer,
        responses={
            201: TournamentResponseSerializer,
            400: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Tournament"]
    )
    def create(self, request):
        return Response({"message": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Retrieve tournaments with filters",
        description="Retrieve a list of tournaments, with optional filters, sorting, and pagination.",
        parameters=[
            OpenApiParameter(name='start_date', description="Filter tournaments that started after this date", required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='end_date', description="Filter tournaments that ended before this date", required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='page', description="Page number for pagination", required=False, type=int, default=1),
            OpenApiParameter(name='limit', description="Number of results per page", required=False, type=int, default=10),
            OpenApiParameter(name='sort_by', description="Sort tournaments by a specific field (start_time or end_time)", required=False, type=str, enum=['start_time', 'end_time'], default='start_time'),
            OpenApiParameter(name='order', description="Order of sorting (ascending or descending)", required=False, type=str, enum=['asc', 'desc'], default='desc'),
        ],
        responses={
            200: TournamentResponseSerializer(many=True),
            400: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Tournament"]
    )
    def list(self, request):
        # You would add filtering, sorting, and pagination here
        pass

    @extend_schema(
        summary="Retrieve a specific tournament",
        description="Retrieve a specific tournament by its ID.",
        parameters=[
            OpenApiParameter(name='tournament_id', description="ID of the tournament to retrieve", required=True, type=int),
        ],
        responses={
            200: TournamentResponseSerializer,
            404: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Tournament"]
    )
    def retrieve(self, request, pk=None):
        return Response({"message": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Update a tournament",
        description="Update a tournament by providing the tournament ID and the updated data.",
        parameters=[
            OpenApiParameter(name='tournament_id', description="ID of the tournament to update", required=True, type=int),
        ],
        request=TournamentCreationRequestSerializer,
        responses={
            200: TournamentResponseSerializer,
            400: OpenApiTypes.OBJECT,  # Return an object with an error message
            404: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Tournament"]
    )
    def update(self, request, pk=None):
        return Response({"message": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Delete a tournament",
        description="Delete a tournament by its ID.",
        parameters=[
            OpenApiParameter(name='tournament_id', description="ID of the tournament to delete", required=True, type=int),
        ],
        responses={
            204: None,
            404: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Tournament"]
    )
    def destroy(self, request, pk=None):
        return Response({"message": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Get user rankings for a specific tournament",
        description="Retrieve user rankings for a specific tournament by its ID.",
        parameters=[
            OpenApiParameter(name='tournament_id', description="ID of the tournament", required=True, type=int),
        ],
        responses={
            200: TournamentRankingResponseSerializer(many=True),
            404: OpenApiTypes.OBJECT,  # Return an object with an error message
        },
        tags=["Tournament"]
    )
    @action(detail=True, methods=['get'], url_path='rankings')
    def rankings(self, request, pk=None):
        # Example logic for getting rankings, you need to implement actual ranking logic
        pass