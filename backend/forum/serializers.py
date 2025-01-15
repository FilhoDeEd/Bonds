from forum.models import Forum, Event
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
            'popularity'
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
            'creation_date',
            'update_date',
            'creator'
        ]
        read_only_fields = [
            'id',
            'slug',
            'creation_date',
            'update_date',
            'creator'
        ]


class EventListSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Event
        fields = [
            'event_id',
            'title',
            'description',
            'location',
            'slug',
            'date',
        ]


class EventEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'date',
        ]