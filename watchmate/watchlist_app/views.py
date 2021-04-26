# from django.shortcuts import render
# from watchlist_app.models import Movie
# # Create your views here.
# from django.http import JsonResponse


# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {'movies': list(movies.values())}

#     return JsonResponse(data)


# def movie_list_detail(request, primary_key):
#     movie = Movie.objects.filter(id=primary_key)
#     data = {'movie': list(movie.values())}

#     return JsonResponse(data)
