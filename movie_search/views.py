import requests
from django.shortcuts import render
from django.http import HttpResponse

from movie_search import movie_api
from movie_search.models import Search

# Create your views here.
def home(request):
    return render(request, "home.html")


def movies_popular(request):

    popular = movie_api.get_most_popular("/movie/popular")

    context = {
        "popular": popular,
    }

    return render(request, "movies_popular.html", context)


def movies_top_rated(request):

    top_rated = movie_api.get_top_rated("/movie/top_rated")
    context = {
        "top_rated": top_rated,
    }

    return render(request, "movies_top_rated.html", context)


def movies_similar(request):

    query = request.GET.get("query")
    year = request.GET.get("year")

    if query:

        # Get a dictionary of movie details based on text query
        query = query.lower()

        movies = movie_api.get_movies("/search/movie", query, year=year)
        movies = {
            movie.lower(): idx for
            movie, idx in movies.items()
        }

        from pprint import pprint as pp
        pp(movies)

        # Get movie id based on selected movie title
        movie_id = movies.get(query)

        similar = movie_api.get_most_similar(f"/movie/{movie_id}/similar")
        context = {
            "similar": similar,
        }

    else:
        return render(request, "error.html")

    return render(request, "movies_similar.html", context)

def movie_detail(request, movie_id):

    movie_detail = movie_api.get_movie_detail(f"/movie/{movie_id}")
    movie_videos = movie_api.get_movie_videos(f"/movie/{movie_id}/videos")

    context = {
        "movie_detail": movie_detail,
        "movie_videos": movie_videos,
    }

    return render(request, "movie_detail.html", context)


