from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from friends.models import Friend
from games.models import Match
from django.contrib.sessions.models import Session
from drf_spectacular.utils import extend_schema_field


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)
    force_login = serializers.BooleanField(default=False)
    
    def to_internal_value(self, data):
        for fieldname in ['username', 'password']:
            if fieldname not in data:
                raise serializers.ValidationError(
                    {
                        "error_code": [400],
                        "detail": ["필드 이름이 잘못되었습니다"]
                    }
                )
        ## requset의 fieldname이 잘못된 경우
        
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )
        ## request의 fieldvalue가 비어있는 경우
        
        return super().to_internal_value(data)
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "존재하지 않는 username 또는 password 입니다"
                }
            )
        ## request와 일치하는 유저정보가 없는 경우
        
        request = self.context['request']
        if request.user.is_authenticated:
            if request.user.username != user.username:
                raise serializers.ValidationError(
                    {
                        "error_code": 400,
                        "detail": "세션 정보가 일치하지 않습니다"
                    }
                )
        ## 이미 로그인된 상태에서 다른 유저로 로그인 시도하는 경우

        if user.status == User.STATUS_MAP['온라인']:
            if data['force_login'] == True:
                sessions = Session.objects.all()
                current_session_key = request.session.session_key

                for session in sessions:
                    session_data = session.get_decoded()
                    if session_data.get('_auth_user_id') == str(user.id):
                        if session.session_key != current_session_key:
                            session.delete()  # 사용자의 기존 세션을 삭제
            else:
                raise serializers.ValidationError(
                    {
                        "error_code": 409,
                        "detail": "다른 기기에서 이미 로그인되어 있습니다"
                    }
                )
        ## 중복 로그인을 시도하는 경우
        
        return {'user': user}
    def save(self):
        user = self.validated_data['user']
        user.status = User.STATUS_MAP['온라인']
        user.save()
        return user

class JoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'profile_img']
        extra_kwargs = {
            'profile_img': {'required': True}
        }
        
    def to_internal_value(self, data):
        for fieldname in ["username", "password", "profile_img"]:
            if fieldname not in data:
                raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## 잘못된 필드이름 확인
        
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )
        ## request의 fieldvalue가 비어있는 경우

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["사용중인 username 입니다"]
                }
            )
        ## 중복된 유저이름 확인
        return super().to_internal_value(data)
    def save(self):
        user = User.objects.create_user(
            username = self.validated_data['username'],
            password = self.validated_data['password'],
            profile_img = self.validated_data['profile_img'],
        )
        user.save()
        return user
    # database에 user객체를 생성합니다.

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['status_msg', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']
        
    def to_internal_value(self, data):
        for fieldname in data:
            if fieldname not in ['status_msg', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']:
                raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## 잘못된 필드이름 확인
        
        return super().to_internal_value(data)
    def save(self):
        user = self.instance
        for fieldname, fieldvalue in self.validated_data.items():
            if fieldvalue == '':
                fieldvalue = '텍스트를 입력하세요'
            setattr(user, fieldname, fieldvalue)
        user.save()
        return user
class RetrieveSearchUserSerializer(serializers.Serializer):
    search = serializers.CharField()

    def validate(self, data):
        user = self.instance
        if user.is_anonymous:
            raise serializers.ValidationError(
                {
                    "error_code": 403,
                    "detail": "로그인 상태가 아닙니다"
                }
            )
        ## 로그인 하지 않은 경우

        username = data.get('search')
        if not username:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "유저 이름을 입력해주세요"
                }
            )
        ## 파라미터가 비어있는 경우

        users = User.objects.filter(username__icontains=username).exclude(username=user.username)
        if not users:
            raise serializers.ValidationError(
                {
                    "error_code": 404,
                    "detail": "일치하는 유저가 없습니다"
                }
            )
        ## username이 들어간 user들을 찾지 못한 경우
        
        return {'users': users}
class RetrieveSearchUserResponseSerializer(serializers.ModelSerializer):
    is_friend = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'status_msg', 'profile_img', 'is_friend']

class CreateFriendshipSerializer(serializers.Serializer):
    friendname = serializers.CharField()

    def to_internal_value(self, data):
        if 'friendname' not in data:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## 잘못된 필드이름 확인
        
        friendname = data.get('friendname')
        if not friendname:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )
        ## request의 fieldvalue가 비어있는 경우

        return super().to_internal_value(data)
    def validate(self, data):
        friendname = data.get('friendname')
        friend = User.objects.filter(username=friendname).first()
        if friend is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "존재하지 않는 friendname입니다"
                }
            )
        ## user테이블에 존재하지 않는 friendname인 경우
        
        user = self.instance
        if user == friend:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "유저 본인을 친구추가 할 수 없습니다"
                }
            )
        ## 본인을 친구추가 하는 경우
        
        old_friendship = Friend.objects.filter(username=user, friendname=friend).first()
        if old_friendship:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "이미 친구상태 입니다"
                }
            )
        ## 이미 친구추가 되어있는 경우
        
        return {'friend': friend}
    def save(self):
        new_friendship = Friend(
            username = self.instance,
            friendname = self.validated_data['friend']
        )
        new_friendship.save()
        return new_friendship
class DeleteFriendshipSerializer(serializers.Serializer):
    friendname = serializers.CharField()

    def validate(self, data):
        friendname = data.get('friendname')
        friend = User.objects.filter(username=friendname).first()
        if friend is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "존재하지 않는 friendname입니다"
                }
            )
        ## user테이블에 존재하지 않는 friendname인 경우
        
        old_friendship = Friend.objects.filter(username=self.instance, friendname=friend).first()
        if old_friendship is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "이미 친구상태가 아닙니다"
                }
            )
        ## 이미 친구해제 되어있는 경우
        
        return {'old_friendship': old_friendship}
    def save(self):
        old_friendship = self.validated_data['old_friendship']
        old_friendship.delete()
        return old_friendship

class MatchResponseSerializer(serializers.ModelSerializer):
    user1_name = serializers.ReadOnlyField(source='match_username1.username')
    user2_name = serializers.ReadOnlyField(source='match_username2.username')
    user1_profile_img = serializers.ReadOnlyField(source='match_username1.profile_img')
    user2_profile_img = serializers.ReadOnlyField(source='match_username2.profile_img')

    class Meta:
        model = Match
        fields = ['user1_name', 'user2_name', 'user1_profile_img', 'user2_profile_img', 'match_result', 'match_start_time', 'match_end_time', 'username1_grade', 'username2_grade', 'match_type']

class MacroTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']

class RetrieveFriendSerializer(serializers.ModelSerializer):
    matches = MatchResponseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'status_msg', 'status', 'exp', 'win_cnt', 'lose_cnt', 'profile_img', 'matches']

class RetrieveUserSerializer(serializers.ModelSerializer):
    matches = MatchResponseSerializer(many=True, read_only=True)
    macrotext = MacroTextSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['exp', 'profile_img', 'win_cnt', 'lose_cnt', 'status_msg', 'macrotext', 'matches']