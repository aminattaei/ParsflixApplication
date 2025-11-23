import requests
import tmdbsimple as tmdb

# API Key
tmdb.API_KEY = "42941c2a27179fe453d890aa899494d5"

# Timeout
tmdb.REQUESTS_TIMEOUT = (2, 5)

# Create session with proxy
session = requests.Session()
session.proxies = {
    "http":  "http://144.91.118.176:3128",
    "https": "http://144.91.118.176:3128",
}

tmdb.REQUESTS_SESSION = session

# Export movies client
movies_api = tmdb.Movies()
