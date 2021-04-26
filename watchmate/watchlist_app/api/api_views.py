from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from watchlist_app.api.serializers import MovieSerializer
from watchlist_app.models import Movie


class MovieListAPI(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieListDetailAPI(APIView):

    def get_movie_object(self, primary_key):
        try:
            return Movie.objects.get(pk=primary_key)
        except:
            return False

    def get(self, request, primary_key):

        movie = self.get_movie_object(primary_key)
        if not movie:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, primary_key):

        movie = self.get_movie_object(primary_key)
        if not movie:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, primary_key):
        movie = self.get_movie_object(primary_key)
        if not movie:
            return Response(status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response({status: "deleted"}, status=status.HTTP_204_NO_CONTENT)
