from forum.models import Forum, Event, Review
from rest_framework import serializers
from user_profile.models import UserProfile
from forum.models import Subscriber

class ForumSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='get_creator_name', read_only=True)
    is_sub = serializers.SerializerMethodField()
    banner_image = serializers.SerializerMethodField()

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
            'creator',
            'is_sub',
            'banner_image'
        ]
        read_only_fields = ['id', 'slug', 'creation_date', 'update_date', 'subscribers_count', 'popularity', 'creator', 'is_sub', 'banner_image']

    def get_banner_image(self, obj):
        request = self.context.get('request')
        if obj.banner_image:
            return request.build_absolute_uri(obj.banner_image.url) if request else obj.banner_image.url
        return None

    def get_is_sub(self, obj):
        user = self.context['request'].user
        
        if not user.is_authenticated:
            return 0

        try:
            account = user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
            sub = Subscriber.objects.get(forum=obj, user_profile=user_profile)
            return 1 if sub.is_sub else -1
        except (UserProfile.DoesNotExist, Subscriber.DoesNotExist):
            return 0


class ForumListSerializer(serializers.ModelSerializer):
    forum_id = serializers.IntegerField(source='id', read_only=True)
    banner_image_low = serializers.SerializerMethodField()

    is_sub = serializers.SerializerMethodField()
    class Meta:
        model = Forum
        fields = [
            'forum_id',
            'title',
            'description',
            'slug',
            'popularity',
            'type',
            'is_sub',
            'banner_image_low'
        ]

    def get_banner_image_low(self, obj):
        request = self.context.get('request')
        if obj.banner_image_low:
            return request.build_absolute_uri(obj.banner_image_low.url) if request else obj.banner_image_low.url
        return None

    def get_is_sub(self, obj):
        user = self.context['request'].user
        
        if not user.is_authenticated:
            return 0

        try:
            account = user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
            sub = Subscriber.objects.get(forum=obj, user_profile=user_profile)
            return 1 if sub.is_sub else -1
        except (UserProfile.DoesNotExist, Subscriber.DoesNotExist):
            return 0

class ForumEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = [
            'title',
            'description'
        ]

class EventSerializer(serializers.ModelSerializer):
    is_sub = serializers.SerializerMethodField(method_name='get_is_sub')
    did_review = serializers.SerializerMethodField(method_name='get_did_review')


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
            'creator',
            'is_sub',
            'did_review'
        ]
        read_only_fields = [
            'id',
            'slug',
            'five_star_mean',
            'creation_date',
            'update_date',
            'creator',
            'is_sub'
        ]

    creator = serializers.CharField(source='get_creator_name', read_only=True)

    def get_is_sub(self, obj):
        user = self.context['request'].user
        
        if not user.is_authenticated:
            return 0

        try:
            account = user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
            sub = Subscriber.objects.get(forum=obj, user_profile=user_profile)
            return 1 if sub.is_sub else -1
        except (UserProfile.DoesNotExist, Subscriber.DoesNotExist):
            return 0
        
    def get_did_review(self, obj):
        user = self.context['request'].user

        if not user.is_authenticated:
            return 0

        try:
            account = user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
            
            # Tente buscar a review, e retorne o status dela se encontrada
            try:
                rev = Review.objects.get(event=obj, user_profile=user_profile)
                return 1 
            except Review.DoesNotExist:
                return 0  

        except UserProfile.DoesNotExist:
            return -1  
    


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
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    creator = serializers.CharField(source='get_creator_name', read_only=True)
    forum_slug = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        source='forum'
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'event',
            'forum_slug',
            'creator',
            'five_star',
            'review_date'
        ]
        read_only_fields = [
            'id',
            'forum_slug',
            'creator',
            'review_date'
        ]

