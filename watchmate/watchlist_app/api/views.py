from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
from django.http import HttpResponse, JsonResponse

from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer


@api_view(('GET', 'POST'))
def movie_list(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(('GET', 'PUT', 'DELETE'))
def movie_list_detail(request, primary_key):

    try:
        movie = Movie.objects.get(pk=primary_key)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == "PUT":

        serializer = MovieSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    elif request.method == 'DELETE':

        movie.delete()
        return Response('Deleted', status=status.HTTP_204_NO_CONTENT)
