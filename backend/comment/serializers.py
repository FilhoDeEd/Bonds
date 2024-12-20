from comment.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='get_creator_name', read_only=True)


    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'post_date',
            'trust_rate',
            #'image',
            'denunciations',
            'forum',
            'creator'
        ]

        read_only_fields = ['id', 'post_date', 'trust_rate', 'denunciations', 'creator']