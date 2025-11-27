from django.db import models
from django.urls import reverse

# ============================
# 1) GENRE
# ============================
class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ============================
# 2) PRODUCTION COMPANY
# ============================
class ProductionCompany(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    logo_path = models.CharField(max_length=500, null=True, blank=True)
    origin_country = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.name


# ============================
# 3) COUNTRIES
# ============================
class ProductionCountry(models.Model):
    iso_code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ============================
# 4) LANGUAGES
# ============================
class SpokenLanguage(models.Model):
    iso_639_1 = models.CharField(max_length=5, unique=True)
    english_name = models.CharField(max_length=255)
    native_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.english_name


# ============================
# 5) COLLECTIONS
# ============================
class Collection(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=500, null=True, blank=True)
    backdrop_path = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)

    poster_path = models.CharField(max_length=500, null=True, blank=True)
    backdrop_path = models.CharField(max_length=500, null=True, blank=True)

    cover = models.ImageField(upload_to='Movies/Covers', height_field=None, width_field=None, max_length=None)
    
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0)

    adult = models.BooleanField(default=False)
    homepage = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    
    original_language = models.ForeignKey(
        SpokenLanguage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movies_with_original_language"   
    )

    spoken_languages = models.ManyToManyField(
        SpokenLanguage,
        blank=True,
        related_name="movies_with_spoken_language" 
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    genres = models.ManyToManyField(Genre, blank=True)
    production_companies = models.ManyToManyField(ProductionCompany, blank=True)
    production_countries = models.ManyToManyField(ProductionCountry, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("Movie_detail", kwargs={"pk": self.pk})
    

