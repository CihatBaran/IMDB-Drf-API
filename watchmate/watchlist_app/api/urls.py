from django.urls import path, include

from rest_framework.routers import DefaultRouter

from watchlist_app.api.api_views import WatchListAPI
from watchlist_app.api.api_views import WatchListDetailAPI
from watchlist_app.api.api_views import WatchlistAPIVS
from watchlist_app.api.api_views import StreamPlatformAPI
from watchlist_app.api.api_views import StreamPlatformDetailAPI
from watchlist_app.api.api_views import StreamPlatformAPIVS
from watchlist_app.api.api_views import ReviewsAPI
from watchlist_app.api.api_views import ReviewsDetailAPI
from watchlist_app.api.api_views import StreamlineReviewsAPI
from watchlist_app.api.api_views import WatchlistReviewsAPI

router = DefaultRouter()
router.register('stream', StreamPlatformAPIVS, basename="streamlineviewset")
router.register('watch', WatchlistAPIVS, basename="watchlistviewset")

urlpatterns = [
    path('', WatchListAPI.as_view(), name="wacthlist-api"),
    path('<int:id>', WatchListDetailAPI.as_view(), name="wacthlist-api"),

    path('streamline', StreamPlatformAPI.as_view(), name="wacthlist-api"),
    path('streamline/<int:id>',
         StreamPlatformDetailAPI.as_view(), name="wacthlist-api"),

    path('reviews', ReviewsAPI.as_view(), name="review-api"),
    path('reviews/<int:id>',
         ReviewsDetailAPI.as_view(), name="review_datail-api"),


    path('<int:id>/reviews', WatchlistReviewsAPI.as_view(),
         name='watchlist_review-api'),
    path('streamline/<int:id>/reviews',
         StreamlineReviewsAPI.as_view(), name="stream_review-api"),
    #     path('streamline/reviews/<int:id>',
    #          StramReviewsDetailAPI.as_view(), name="review-api"),

    path('', include(router.urls))
]
