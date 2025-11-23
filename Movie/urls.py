from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    # صفحه اصلی
    path('', views.HomeTemplateView.as_view(), name='home'),

    # لیست فیلم‌ها
    path('movies/', views.movie_list, name='movie_list'),

    # جزئیات هر فیلم
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),

    # تست اتصال TMDB API
    path('test-tmdb/', views.test_tmdb_api, name='test_tmdb_api'),
]
