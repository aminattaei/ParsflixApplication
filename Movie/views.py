from django.shortcuts import render
from django.views import generic
from django.views import View
import tmdbsimple as tmdb

from .models import Movie

tmdb.API_KEY = '42941c2a27179fe453d890aa899494d5'
tmdb.REQUESTS_TIMEOUT = (2, 5)


class HomeListView(generic.ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["popular_movies"] = Movie.objects.all()[:20]
        context["top_rated_movies"] = Movie.objects.all()[20:40]
        return context
    

class MovieListView(generic.ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = "movie-category.html"

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["popular_movies"] = Movie.objects.all()[:20]
        context["top_rated_movies"] = Movie.objects.all()[20:40]
        return context



class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = "movie-details.html"
