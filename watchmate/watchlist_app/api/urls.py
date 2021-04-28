from django.urls import path

from watchlist_app.api.api_views import WatchListAPI
from watchlist_app.api.api_views import WatchListDetailAPI
from watchlist_app.api.api_views import StreamPlatformAPI
from watchlist_app.api.api_views import StreamPlatformDetailAPI
from watchlist_app.api.api_views import ReviewsAPI
from watchlist_app.api.api_views import ReviewsDetailAPI


urlpatterns = [
    path('', WatchListAPI.as_view(), name="wacthlist-api"),
    path('<int:primary_key>', WatchListDetailAPI.as_view(), name="wacthlist-api"),
    path('streamline', StreamPlatformAPI.as_view(), name="wacthlist-api"),
    path('streamline/<int:primary_key>',
         StreamPlatformDetailAPI.as_view(), name="wacthlist-api"),
    path('reviews', ReviewsAPI.as_view(), name="review-api"),
    path('reviews/<int:id>',
         ReviewsDetailAPI.as_view(), name="review_datail-api")
]
