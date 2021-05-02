from watchlist_app.models import Reviews
from watchlist_app.models import StreamPlatform
from watchlist_app.models import WatchList
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.db.models import (Avg, Count, Max, Min)
from django.db.models import Min
from django.db.models import Max
from django.db.models import Count
from django.db.models import Avg
<< << << < Updated upstream
== == == =
>>>>>> > Stashed changes


class PlatformListeningField(serializers.RelatedField):
    """
    Foreign Key field will be appearing on the watch list serializer, as return of to_representation func
    """

    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "about": value.about,
            "website": value.website
        }


class WatchListListeningField (serializers.RelatedField):
    """
    Foreign Key field will be appearing on the watch list serializer, as return of to_representation func
    """

    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title,
            "storyline": value.storyline,
            "active": value.active,
            "created": value.created,
            "platform": value.platform.name

        }


class ReviewsSerializer(serializers.ModelSerializer):
    """
    Review Serializer
    """
    review_watchlist = WatchListListeningField(read_only=True)
    review_user = serializers.StringRelatedField()

    class Meta:
        model = Reviews
        fields = "__all__"

    def rating_validation(self, rating):
        if rating < 2:
            raise ValidationError({
                'message': 'rating cannot be less than 2'
            })

    def create(self, validated_data):
        self.rating_validation(validated_data.get('rating'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.rating_validation(validated_data.get('rating'))
        return super().update(instance, validated_data)


class WatchListSerializer(serializers.ModelSerializer):
    """
    Watchlist serializer
    """
    # platform = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='about'
    # )
    platform = PlatformListeningField(read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"

    class CloneReviewsSerializer(ReviewsSerializer):
        review_watchlist = None

        class Meta:
            model = Reviews
            exclude = ('review_watchlist',)

    reviews = CloneReviewsSerializer(many=True, read_only=True)
    rating_average = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    reviews_max = serializers.SerializerMethodField()
    reviews_min = serializers.SerializerMethodField()

    def get_rating_average(self, obj):
        rating_average = obj.reviews.all().aggregate(Avg('rating')).get('rating__avg')

        if rating_average is not None:
            return round(rating_average, 2)

    def get_reviews_count(self, obj):
        count = obj.reviews.all().aggregate(Count('rating')).get('rating__count')
        if count is not None:
            return count

    def get_reviews_max(self, obj):
        max_review = obj.reviews.all().aggregate(Max('rating')).get('rating__max')
        if max_review is not None:
            return max_review

    def get_reviews_min(self, obj):
        max_review = obj.reviews.all().aggregate(Min('rating')).get('rating__min')
        if max_review is not None:
            return max_review


class StreamPlatformSerializer(serializers.ModelSerializer):
    """
    Stream Platform serializer
    """
    class Meta:
        model = StreamPlatform
        fields = ('id', 'name', 'about', 'website', 'watchlists')

    class CloneWatchListSerializer(WatchListSerializer):
        platform = serializers.StringRelatedField()

        class Meta:
            model = WatchList
            fields = ('id', 'title', 'storyline',
                      'active', 'platform', "rating_average")

    watchlists = CloneWatchListSerializer(many=True, read_only=True)
