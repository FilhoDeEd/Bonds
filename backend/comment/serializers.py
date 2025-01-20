
from rest_framework import serializers
from comment.models import Comment, Like, Report, Pool, Option
from forum.models import Forum
from user_profile.models import UserProfile

class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='get_creator_name', read_only=True)
    post_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    trust_rate = serializers.SerializerMethodField()
    forum_slug = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        source='forum'
    )
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'post_date',
            'trust_rate',
            'denunciations',
            'forum',
            'forum_slug',
            'creator',
            'has_liked',
            'type'
        ]
        read_only_fields = ['id', 'post_date', 'trust_rate', 'denunciations', 'creator', 'forum_slug', 'has_liked']

    def get_trust_rate(self, obj):
        return obj.trust_rate()

    def get_has_liked(self, obj):
        user = self.context['request'].user
        
        if not user.is_authenticated:
            return 0

        try:
            account = user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
            comment_like = Like.objects.get(comment=obj, user_profile=user_profile)
            return 1 if comment_like.is_like else -1
        except (UserProfile.DoesNotExist, Like.DoesNotExist):
            return 0

    

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = [
            'id',
            'comment',
            'user_profile',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='get_creator_name', read_only=True)
    post_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    trust_rate = serializers.SerializerMethodField()
    forum_slug = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        source='forum'
    )
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'content',
            'title',
            'tag',
            'location',
            'date',
            'solved',
            'post_date',
            'trust_rate',
            'denunciations',
            'forum',
            'forum_slug',
            'creator',
            'has_liked',
            'type'
        ]
        read_only_fields = ['id', 'post_date', 'trust_rate', 'denunciations', 'creator', 'forum_slug', 'has_liked']

    def get_trust_rate(self, obj):
        return obj.trust_rate()

    def get_has_liked(self, obj):
        user = self.context['request'].user
        
        if not user.is_authenticated:
            return 0

        try:
            account = user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
            comment_like = Like.objects.get(comment=obj, user_profile=user_profile)
            return 1 if comment_like.is_like else -1
        except (UserProfile.DoesNotExist, Like.DoesNotExist):
            return 0


class OptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Option
        fields = [
            'id',
            'option_text',
            'votes'
        ]
        read_only_fields = [
            'id',
            'votes'
        ]


class PoolSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='get_creator_name', read_only=True)
    post_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    forum_slug = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        source='forum'
    )

    options = OptionSerializer(many=True, read_only=True)  # Exibe as opções associadas na resposta

    class Meta:
        model = Pool
        fields = [
            'id',
            'title',
            'content',
            'deadline',
            'post_date',
            'forum',
            'forum_slug',
            'creator',
            'options',  # Incluindo 'options' para leitura
        ]
        read_only_fields = [
            'id',
            'post_date',
            'creator',
            'forum_slug',
        ]

    def create(self, validated_data):
        # Pega as opções do request
        options_data = validated_data.pop('options', [])

        # Cria o objeto Pool
        pool = Pool.objects.create(**validated_data)

        # Cria as opções associadas à Pool
        for option_data in options_data:
            Option.objects.create(pool=pool, **option_data)

        return pool


class PoolEditSerializer(serializers.ModelSerializer):
    """
    Serializer para editar apenas os campos title, content e deadline de uma Pool.
    """
    class Meta:
        model = Pool
        fields = ['title', 'content', 'deadline']