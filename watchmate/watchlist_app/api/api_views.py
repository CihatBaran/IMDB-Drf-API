from django.shortcuts import get_object_or_404

from watchlist_app.models import Reviews
from watchlist_app.models import StreamPlatform
from watchlist_app.models import WatchList
from watchlist_app.api.serializers import ReviewsSerializer
from watchlist_app.api.serializers import StreamPlatformSerializer
from watchlist_app.api.serializers import WatchListSerializer
from watchlist_app.api.permissions import AdminOrReadOnly
from watchlist_app.api.permissions import StaffAdminOrReadOnly
from watchlist_app.api.permissions import ReviewUserOrReadOnly


from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class WatchListAPI(ListCreateAPIView):
    """
    Watchlist Api view GET, POST
    """
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = (AdminOrReadOnly,)

    class CloneWatchlistSerializer(WatchListSerializer):
        platform = None

    def create(self, request, *args, **kwargs):
        serializer = self.CloneWatchlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # class WatchListAPI(APIView)
    #     def get(self, request):
    #         watchlists = WatchList.objects.all()

    #         serializer = WatchListSerializer(watchlists, many=True)
    #         return Response(serializer.data)

    #     def post(self, request):
    #         serializer = WatchListSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAPI(APIView):
    """
    Watchlist Detail Api view GET, PUT, DELETE
    """
    permission_classes = (AdminOrReadOnly,)

    def get_movie_object(self, id):
        try:
            return WatchList.objects.get(pk=id)
        except:
            return False

    def get(self, request, id):

        watchlist = self.get_movie_object(id)
        if not watchlist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, id):
        class CloneWatchlistSerializer(WatchListSerializer):
            platform = None

        watchlist = self.get_movie_object(id)
        if not watchlist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CloneWatchlistSerializer(
            instance=watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        watchlist = self.get_movie_object(id)
        if not watchlist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        watchlist.delete()
        return Response({"status": "deleted"}, status=status.HTTP_204_NO_CONTENT)


class WatchlistAPIVS(ModelViewSet):
    serializer_class = WatchListSerializer
    queryset = WatchList.objects.all()

    class GhostWatchlistSerializer(WatchListSerializer):
        platform = None

    def create(self, request, *args, **kwargs):
        serializer = self.GhostWatchlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StreamPlatformAPIVS(ViewSet):
    permission_classes = (AdminOrReadOnly,)

    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)


class StreamPlatformAPI(APIView):
    """
    Stream Platform Api view GET, POST
    """
    permission_classes = (AdminOrReadOnly,)

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Rewriting the APIView with generic
    """
    queryset = StreamPlatform.objects.all()
    lookup_field = 'id'
    serializer_class = StreamPlatformSerializer
    permission_classes = (AdminOrReadOnly,)


class ReviewsAPI(ListCreateAPIView):
    """
    Reviews api
    """
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthenticated,)

    class CloneReviewsSerializer(ReviewsSerializer):
        review_watchlist = None
        review_user = None

    def perform_create(self, serializer):

        user_reviewed_before = Reviews.objects.all().filter(
            review_watchlist=self.request.data.get('review_watchlist')).exists()
        watchlist = WatchList.objects.all().get(
            id=self.request.data.get('review_watchlist')).title

        if user_reviewed_before:
            raise ValidationError(
                {'message': f'you already added a review for this particular watchlist: {watchlist} as {self.request.user.username}'})

        serializer.save(review_user=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = self.CloneReviewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewsDetailAPI(RetrieveUpdateDestroyAPIView):
    """"
    Review Detail Api
    """
    lookup_field = 'id'
    serializer_class = ReviewsSerializer
    permission_classes = (ReviewUserOrReadOnly,)

    # clone serializer
    class CloneForUpdateReviewsSerializer(ReviewsSerializer):
        review_watchlist = None

    def perform_update(self, serializer):
        user = self.request.user

        cur_review = Reviews.objects.all().get(id=self.kwargs.get('id'))

        isPermitted = cur_review.review_user == self.request.user
        if not isPermitted:
            raise ValidationError(
                {'message': 'You cannot change others reviews'})
        serializer.save(review_user=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.CloneForUpdateReviewsSerializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_queryset(self):
        queryset = Reviews.objects.all()
        return Reviews.objects.all()


class WatchlistReviewsAPI(ListCreateAPIView):
    serializer_class = ReviewsSerializer
    # permission_classes = (IsAuthenticated,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # This  below is to not create review directly instead get the url param id and
    # based on that perform review creation and check the user has reviewed the current watchlist before
    def perform_create(self, serializer):

        id = self.kwargs.get('id')
        review_watchlist = WatchList.objects.get(id=id)

        review_user = self.request.user
        review_queryset = Reviews.objects.filter(
            review_watchlist=review_watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError(
                {'message': f"You can't make a review second time as {review_user} for the same movie"})

        serializer.save(review_watchlist=review_watchlist,
                        review_user=review_user)

    # we get the query set based on url param id, because of nested routes
    def get_queryset(self):

        id = self.kwargs.get('id')

        queryset = Reviews.objects.filter(review_watchlist=id)
        return queryset


class StreamlineReviewsAPI(ListAPIView):
    id = None
    lookup_url_kwarg = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        # queryset = Reviews.objects.filter(review_watchlist=id)

        queryset = Reviews.objects.all().filter(review_watchlist__platform=id)

        return queryset

    class CloneReviewSerializer(ReviewsSerializer):
        review_watchlist = None

        platform = serializers.SerializerMethodField()
        review_watchlist = serializers.StringRelatedField()

        class Meta:
            model = Reviews
            fields = "__all__"
            depth = 1

        def get_platform(self, obj):
            return obj.review_watchlist.platform.name

    serializer_class = CloneReviewSerializer


# class StreamPlatformDetailAPI(APIView):
#     """
#     Stream Platform Detail Api view GET, PUT, DELETE
#     """

#     def get_platform(self, primary_key):
#         try:
#             return StreamPlatform.objects.get(pk=primary_key)
#         except:
#             return False

#     def get(self, request, primary_key):
#         platform = self.get_platform(primary_key)
#         if not platform:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)

#     def put(self, request, primary_key):
#         platform = self.get_platform(primary_key)
#         if not platform:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         serializer = StreamPlatformSerializer(
#             instance=platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, primary_key):
#         platform = self.get_platform(primary_key)
#         if not platform:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         platform.delete()
#         return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)

# class ReviewsAPI(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

#     queryset = Reviews.objects.all()
#     serializer_class = ReviewsSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):

#         # if request.data.get('rating') < 2:
#         #     raise ValidationError({"message": "review cannot be less than 2"})

#         return self.create(request, *args, **kwargs)
