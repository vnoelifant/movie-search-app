from django.shortcuts import render
from django.http import HttpResponse

from movie_search import movie_api
from movie_search.models import Movie

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
