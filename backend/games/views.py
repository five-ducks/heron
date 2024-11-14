from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter
from friends.models import Friend

from django.db.models import Q
from games.models import Match

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
            user = request.user
            matches = Match.objects.filter((Q(match_username1=user) | Q(match_username2=user)) & ~Q(match_result='pending_result'))
            matches_data = {
                "matches": [
                    {
                        'user1_name': match.match_username1.username,
                        'user2_name': match.match_username2.username,
                        'user1_profile_img': match.match_username1.profile_img,
                        'user2_profile_img': match.match_username2.profile_img,
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
            user = request.user
            friends = Friend.objects.filter(username=user)
            if not friends.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            friends_data = []
            for friend in friends:
                friend_user = friend.friendname
                matches = Match.objects.filter((Q(match_username1=friend_user) | Q(match_username2=friend_user)) & ~Q(match_result='pending_result'))
                friends_data.append(
                    {
                        "username": friend_user.username,
                        "status_msg": friend_user.status_msg,
                        "status": friend_user.status,
                        "exp": friend_user.exp,
                        "win_cnt": friend_user.win_cnt,
                        "lose_cnt": friend_user.lose_cnt,
                        "profile_img": friend_user.profile_img,
                        "matches": [
                            {
                                'user1_name': match.match_username1.username,
                                'user2_name': match.match_username2.username,
                                'user1_profile_img': match.match_username1.profile_img,
                                'user2_profile_img': match.match_username2.profile_img,
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
                )
            return Response(friends_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # username을 기반으로 match history를 찾는 API