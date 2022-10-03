from django.shortcuts import render
from django.http import HttpResponse

from movie_search import movie_api

# Create your views here.
def home(request):
    return render(request, "home.html")


def movies(request):

    popular = movie_api.get_most_popular("/movie/popular")
    top_rated = movie_api.get_top_rated("/movie/top_rated")
    context = {
        "popular": popular,
        "top_rated": top_rated,
    }

    return render(request, "movies.html", context)
