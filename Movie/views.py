import os
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Movie
from django.views import View
import tmdbsimple as tmdb
import json
import asyncio
from nats.aio.client import Client as NATS
from django.http import JsonResponse


# Initialize TMDB API
tmdb.API_KEY = os.getenv('TMDB_API_KEY')



# ===========================
# UTILS: FETCH & CACHE MOVIES
# ===========================
def fetch_and_cache_movies(category="popular", count=20):
    
    movies_api = tmdb.Movies()
    if category == "popular":
        data = movies_api.popular().get('results', [])
    elif category == "top_rated":
        data = movies_api.top_rated().get('results', [])
    else:
        data = []

    movies = []
    for m in data[:count]:
        movie_obj, created = Movie.objects.update_or_create(
            tmdb_id=m['id'],
            defaults={
                'title': m.get('title'),
                'overview': m.get('overview'),
                'release_date': m.get('release_date'),
                'poster_path': m.get('poster_path'),
                'vote_average': m.get('vote_average', 0),
                'vote_count': m.get('vote_count', 0),
                'popularity': m.get('popularity', 0)
            }
        )
        movies.append(movie_obj)
    return movies


# ===========================
# MOVIE LIST
# ===========================
def movie_list(request):
    
    popular_movies = Movie.objects.filter(popularity__gt=0).order_by('-popularity')[:20]
    top_rated_movies = Movie.objects.filter(vote_average__gt=0).order_by('-vote_average')[:20]

    
    if not popular_movies.exists():
        popular_movies = fetch_and_cache_movies("popular")
    if not top_rated_movies.exists():
        top_rated_movies = fetch_and_cache_movies("top_rated")

    context = {
        'popular': popular_movies,
        'top_rated': top_rated_movies,
    }
    return render(request, "movie-category.html", context)


# ===========================
# MOVIE DETAIL
# ===========================
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



async def publish_event(data):
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4222"])

    #JetStream
    js = nc.jetstream()
    
    await js.publish(
        "user.registered",
        json.dumps(data).encode(),
    )

    await nc.close()
    


def register(request):
    data = {
        'user':'amin',
        'email':'aminattaei2000@gmail.com'
    }

    asyncio.run(publish_event(data))

    return JsonResponse({'status':'user registered'})