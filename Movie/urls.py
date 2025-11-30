from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    path('',views.HomeListView.as_view(),name="home_page"),
    path('movies/',views.MovieListView.as_view(),name="Movie_list"),
    path('movie/<int:pk>/',views.MovieDetailView.as_view(),name='Movie_detail'),
    path('register/', views.register, name='register'),
]
