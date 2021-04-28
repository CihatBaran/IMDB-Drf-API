from django.contrib import admin
from watchlist_app.models import WatchList
from watchlist_app.models import StreamPlatform
from watchlist_app.models import Reviews

# Register your models here.


@admin.register(WatchList)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created", "platform")

    search_fields = ("title", "created")

    class Meta:
        model = WatchList


@admin.register(StreamPlatform)
class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')

    search_fields = ('name',)

    class Meta:
        model = StreamPlatform


@admin.register(Reviews)
class ReviewsModelAdmin(admin.ModelAdmin):
    def get_review_watchlist(self, obj):
        return obj.review_watchlist.title

    list_display = ('rating', 'get_review_watchlist')

    search_fields = ('rating', 'review_watchlist__title')

    class Meta:
        model = Reviews
