import requests
from django.shortcuts import render
from django.http import HttpResponse

from movie_search import movie_api
from movie_search.models import Search
from movie_search.utils import title_case

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

    query = title_case(request.GET.get("query"))

    if query:

        # Get a dictionary of movie details based on text query
        movies = movie_api.get_movies("/search/movie", query)

        # Get movie id based on selected movie title
        movie_id = movies.get(query)

        similar = movie_api.get_most_similar(f"/movie/{movie_id}/similar")
        context = {
            "similar": similar,
        }

    else:
        return render(request, "error.html")

    return render(request, "movies_similar.html", context)




