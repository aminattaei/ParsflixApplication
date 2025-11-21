from django.contrib import admin
from .models import (
    Genre,
    ProductionCompany,
    ProductionCountry,
    SpokenLanguage,
    Collection,
    Movie
)


# ============================
# GENRE ADMIN
# ============================
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "tmdb_id", "name")
    search_fields = ("name", "tmdb_id")
    ordering = ("name",)


# ============================
# PRODUCTION COMPANY ADMIN
# ============================
@admin.register(ProductionCompany)
class ProductionCompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "tmdb_id", "name", "origin_country")
    search_fields = ("name", "tmdb_id")
    list_filter = ("origin_country",)
    ordering = ("name",)


# ============================
# PRODUCTION COUNTRY ADMIN
# ============================
@admin.register(ProductionCountry)
class ProductionCountryAdmin(admin.ModelAdmin):
    list_display = ("id", "iso_code", "name")
    search_fields = ("name", "iso_code")
    ordering = ("iso_code",)


# ============================
# SPOKEN LANGUAGE ADMIN
# ============================
@admin.register(SpokenLanguage)
class SpokenLanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "iso_639_1", "english_name", "native_name")
    search_fields = ("english_name", "native_name", "iso_639_1")
    ordering = ("english_name",)


# ============================
# COLLECTION ADMIN
# ============================
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "tmdb_id", "name")
    search_fields = ("name", "tmdb_id")
    ordering = ("name",)


# ============================
# MOVIE ADMIN
# ============================
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "tmdb_id",
        "release_date",
        "vote_average",
        "popularity",
        "adult",
    )

    search_fields = (
        "title",
        "tmdb_id",
        "original_title",
    )

    list_filter = (
        "adult",
        "status",
        "release_date",
        "genres",
        "production_countries",
    )

    filter_horizontal = (
        "genres",
        "production_companies",
        "production_countries",
        "spoken_languages",
    )

    ordering = ("-popularity",)
