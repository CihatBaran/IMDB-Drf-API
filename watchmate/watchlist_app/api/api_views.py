from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from watchlist_app.api.serializers import WatchListSerializer
from watchlist_app.api.serializers import StreamPlatformSerializer
from watchlist_app.api.serializers import ReviewsSerializer
from watchlist_app.models import WatchList
from watchlist_app.models import StreamPlatform
from watchlist_app.models import Reviews


class WatchListAPI(ListCreateAPIView):
    """
    Watchlist Api view GET, POST
    """
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
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

    def get_movie_object(self, primary_key):
        try:
            return WatchList.objects.get(pk=primary_key)
        except:
            return False

    def get(self, request, primary_key):

        watchlist = self.get_movie_object(primary_key)
        if not watchlist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, primary_key):

        watchlist = self.get_movie_object(primary_key)
        if not watchlist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(instance=watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, primary_key):
        watchlist = self.get_movie_object(primary_key)
        if not watchlist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        watchlist.delete()
        return Response({status: "deleted"}, status=status.HTTP_204_NO_CONTENT)


class StreamPlatformAPI(APIView):
    """
    Stream Platform Api view GET, POST
    """

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


class StreamPlatformDetailAPI(APIView):
    """
    Stream Platform Detail Api view GET, PUT, DELETE
    """

    def get_platform(self, primary_key):
        try:
            return StreamPlatform.objects.get(pk=primary_key)
        except:
            return False

    def get(self, request, primary_key):
        platform = self.get_platform(primary_key)
        if not platform:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, primary_key):
        platform = self.get_platform(primary_key)
        if not platform:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = StreamPlatformSerializer(
            instance=platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, primary_key):
        platform = self.get_platform(primary_key)
        if not platform:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        platform.delete()
        return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


class ReviewsAPI(ListCreateAPIView):
    """
    Reviews api
    """
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    # def get(self, request):
    #     reviews = Reviews.objects.all()
    #     serializer = ReviewsSerializer(reviews, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = ReviewsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsDetailAPI(RetrieveUpdateDestroyAPIView):

    queryset = Reviews.objects.all()
    lookup_field = 'id'
    serializer_class = ReviewsSerializer
