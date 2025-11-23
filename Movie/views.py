import os
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Movie
import tmdbsimple as tmdb

# ===========================
# TMDB CONFIG
# ===========================
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise Exception("TMDB_API_KEY is not set in environment variables!")

tmdb.API_KEY = TMDB_API_KEY
tmdb.REQUESTS_TIMEOUT = (2, 5)


# ===========================
# HOME PAGE
# ===========================
class HomeTemplateView(generic.TemplateView):
    template_name = "index.html"


# ===========================
# UTILS: FETCH & CACHE MOVIES
# ===========================
def fetch_and_cache_movies(category="popular", count=20):
    """
    دریافت لیست فیلم‌ها از TMDB و ذخیره در دیتابیس
    category: popular | top_rated
    """
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
    """
    صفحه نمایش لیست فیلم‌ها
    ابتدا تلاش برای گرفتن از دیتابیس
    اگر دیتابیس خالی بود، از TMDB API دریافت و ذخیره می‌کنیم
    """
    popular_movies = Movie.objects.filter(popularity__gt=0).order_by('-popularity')[:20]
    top_rated_movies = Movie.objects.filter(vote_average__gt=0).order_by('-vote_average')[:20]

    # کش اگر دیتابیس خالی بود
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
class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = "movie-details.html"


# ===========================
# OPTIONAL: TEST API CONNECTION
# ===========================
from django.http import JsonResponse
import requests

def test_tmdb_api(request):
    try:
        res = requests.get("https://api.themoviedb.org/3/movie/popular", params={"api_key": TMDB_API_KEY}, timeout=5)
        return JsonResponse({"ok": True, "status_code": res.status_code})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})
