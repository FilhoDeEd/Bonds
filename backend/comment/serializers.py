
from rest_framework import serializers
from comment.models import Comment, CommentLike
from forum.models import Forum

class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='get_creator_name', read_only=True)
    post_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    trust_rate = serializers.SerializerMethodField()
    forum_slug = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        source='forum'
    )

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
        ]
        read_only_fields = ['id', 'post_date', 'trust_rate', 'denunciations', 'creator', 'forum_slug']

    def get_trust_rate(self, obj):
        return obj.trust_rate()
    

class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        fields = [
            'id',
            'comment',
            'user_profile',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']