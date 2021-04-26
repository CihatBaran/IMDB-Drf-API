from watchlist_app.api.views import movie_list, movie_list_detail
from watchlist_app.api.api_views import MovieListAPI, MovieListDetailAPI
from django.urls import path

urlpatterns = [
    # path('list/', movie_list, name="movie-list"),
    # path('list/<int:primary_key>', movie_list_detail, name='movie')
    path('list/', MovieListAPI.as_view(), name="movie-list"),
    path('list/<int:primary_key>',
         MovieListDetailAPI.as_view(), name='movie')
]
