from rest_framework import serializers

from watchlist_app.models import WatchList
from watchlist_app.models import StreamPlatform
from watchlist_app.models import Reviews


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
    review_watchlist_id = serializers.IntegerField(write_only=True)

    # review_watchlist = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='title'
    # )

    class Meta:
        model = Reviews
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    """
    Watchlist serializer
    """
    # platform = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='about'
    # )
    platform = PlatformListeningField(read_only=True)
    platform_id = serializers.IntegerField(write_only=True)

    class GhostReviewsSerializer(ReviewsSerializer):
        review_watchlist = None

        class Meta:
            model = Reviews
            exclude = ('review_watchlist',)

    reviews = GhostReviewsSerializer(many=True, read_only=True)
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = WatchList
        fields = ('id', 'title', 'storyline',
                  'active', 'created', 'platform', "rating_average", 'reviews', "platform_id")

    def get_rating_average(self, obj):

        result = obj.reviews.all().values()
        list_result = [entry for entry in result]
        total_rating = 0

        for review in list_result:
            total_rating += review.get('rating')
        if len(list_result) == 0:
            return "No Rating Found"
        average_rating = total_rating / len(list_result)

        return round(average_rating, 2)


class StreamPlatformSerializer(serializers.ModelSerializer):
    """
    Stream Platform serializer
    """
    class Meta:
        model = StreamPlatform
        fields = ('id', 'name', 'about', 'website', 'watchlists')

    class GhostWatchListSerializer(WatchListSerializer):
        platform = serializers.StringRelatedField()

        class Meta:
            model = WatchList
            fields = ('id', 'title', 'storyline',
                      'active', 'platform', "rating_average")

    watchlists = GhostWatchListSerializer(many=True, read_only=True)
