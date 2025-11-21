from django.shortcuts import render
from django.views import generic
import tmdbsimple as tmdb

from .models import Movie

tmdb.API_KEY = '42941c2a27179fe453d890aa899494d5'
tmdb.REQUESTS_TIMEOUT = (2, 5)

class HomeTemplateView(generic.TemplateView):
    template_name = "index.html"


def movie_list(request):
    movies_api = tmdb.Movies()

    # Popular movies
    popular = movies_api.popular()
    popular_results = popular.get('results', [])

    # Top rated movies
    top_rated = movies_api.top_rated()
    top_rated_results = top_rated.get('results', [])

    context = {
        'popular': popular_results,
        'top_rated': top_rated_results,
    }

    return render(request, "movie-category.html", context)

    

class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = "movie-details.html"
