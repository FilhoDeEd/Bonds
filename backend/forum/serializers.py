from forum.models import Forum, Event, Review
from rest_framework import serializers


class ForumSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='get_creator_name', read_only=True)

    class Meta:
        model = Forum
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'subscribers_count',
            'popularity',
            'creation_date',
            'update_date',
            'creator'
        ]
        read_only_fields = ['id', 'slug', 'creation_date', 'update_date', 'subscribers_count', 'popularity', 'creator']


class ForumListSerializer(serializers.ModelSerializer):
    forum_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Forum
        fields = [
            'forum_id',
            'title',
            'description',
            'slug',
            'popularity',
            'type'
        ]

class ForumEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = [
            'title',
            'description'
        ]

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='get_creator_name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'date',
            'location',
            'cancelled',
            'five_star_mean',
            'creation_date',
            'update_date',
            'creator'
        ]
        read_only_fields = [
            'id',
            'slug',
            'five_star_mean',
            'creation_date',
            'update_date',
            'creator'
        ]


class EventEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'cancelled',
            'date',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    forum = serializers.CharField(source='forum.title', read_only=True)
    event = serializers.CharField(source='event.title', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'event',
            'user',
            'five_star',
            'location',
            'review_date'
        ]
        read_only_fields = [
            'id',
            'event',
            'user',
            'review_date'
        ]
        
class ReviewEditSerializer(serializers.ModelSerializer):
    forum = serializers.CharField(source='forum.title', read_only=True)
    event = serializers.CharField(source='event.title', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'five_star',
            'location',
        ]