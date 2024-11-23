from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter

from django.db.models import Q
from games.models import Match

from .seiralizers import (
    RetrieveMatchDataSerializer
)

class MatchViewSet(viewsets.ViewSet):
    
    """
    A ViewSet for managing matches.
    """

    lookup_field = 'username'

##### READ #####
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='count',
                description='Retrieve user match history by username and count',
                required=False,
                type=int
            ),
        ],
        summary="Search user match history",
        description="Find match history based on username and count\n\
                    default is count=5",
        responses={
            200: OpenApiResponse(
                response=RetrieveMatchDataSerializer,
                description="Successfully retrieve match history"
            ),
            403: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Don't have permission to access the data",
                examples=[
                    OpenApiExample(
                        name="Not logged in",
                        value={ "error": "로그인 상태가 아닙니다" },
                        media_type='application/json'
                    )
                ]
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Not Found",
                examples=[
                    OpenApiExample(
                        name="User find fail",
                        value={ "error": "일치하는 유저가 없습니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["Match"]
    )
    def retrieve(self, request, username=None):
        try:
            matches = Match.objects.filter(
                (Q(match_username1=username) | Q(match_username2=username)) & ~Q(match_result='pending_result') & 
                (Q(match_username1__isnull=False) & Q(match_username2__isnull=False))
            )

            if not matches.exists():
                return Response({}, status=status.HTTP_200_OK)
            
            matches_data = {
                "matches": [
                    {
                        'user1_name': match.match_username1,
                        'user2_name': match.match_username2,
                        'match_result': match.match_result,
                        'match_start_time': match.match_start_time,
                        'match_end_time': match.match_end_time,
                        'user1_grade': match.username1_grade,
                        'user2_grade': match.username2_grade,
                        'match_type': match.match_type
                    } 
                    for match in matches.order_by('-match_end_time')[:5]
                ]
            }
            return Response(matches_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # username을 기반으로 match history를 찾는 API

    @extend_schema(
        summary="Search users match history",
        description="Find match history based on username",
        responses={
            200: OpenApiResponse(
                response=RetrieveMatchDataSerializer,
                description="Successfully retrieve match history"
            ),
            403: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Don't have permission to access the data",
                examples=[
                    OpenApiExample(
                        name="Not logged in",
                        value={ "error": "로그인 상태가 아닙니다" },
                        media_type='application/json'
                    )
                ]
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Not Found",
                examples=[
                    OpenApiExample(
                        name="User find fail",
                        value={ "error": "일치하는 유저가 없습니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["Match"]
    )
    @action(detail=False, methods=['post'], url_path='search')
    def search(self, request):
        try:
            friends_name = []
            for friend in request.data.get('friendList'):
                friends_name.append(friend['username'])

            if friends_name is []:
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            friends_match_data = { "matches": {} }
            for friend_name in friends_name:
                matches = Match.objects.filter(
                    (Q(match_username1=friend_name) | Q(match_username2=friend_name)) & ~Q(match_result='pending_result') & 
                    (Q(match_username1__isnull=False) & Q(match_username2__isnull=False))
                )
                friends_match_data["matches"][friend_name] = [
                            {
                                'user1_name': match.match_username1,
                                'user2_name': match.match_username2,
                                'match_result': match.match_result,
                                'match_start_time': match.match_start_time,
                                'match_end_time': match.match_end_time,
                                'user1_grade': match.username1_grade,
                                'user2_grade': match.username2_grade,
                                'match_type': match.match_type
                            } 
                            for match in matches.order_by('-match_end_time')[:5]
                        ]
            return Response(friends_match_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # username을 기반으로 match history를 찾는 API