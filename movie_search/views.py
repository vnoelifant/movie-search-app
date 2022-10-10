import requests
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint

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


def media_similar(request):

    query = request.GET.get("query")
    year = request.GET.get("year")

    if query:

        query = query.lower()

        print("QUERY: ", request.GET.get("query"))

        print("TYPE: ", request.GET.get("type"))
        # Get a dictionary of movie details based on text query
        media = movie_api.get_media(
            f"/search/{request.GET.get('type')}", query, year=year
        )

        media = {media.lower(): idx for media, idx in media.items()}

        # Get media id based on selected media title
        media_id = media.get(query)

        similar = movie_api.get_most_similar(
            f"/{request.GET.get('type')}/{media_id}/similar"
        )
        context = {"similar": similar, "type": request.GET.get("type")}

    else:
        return render(request, "error.html")

    return render(request, "media_similar.html", context)


def movie_detail(request, movie_id):

    movie_detail = movie_api.get_movie_detail(f"/movie/{movie_id}")
    # print("MOVIE DETAIL: ", movie_detail)
    
    movie_videos = movie_api.get_movie_videos(f"/movie/{movie_id}/videos")

    context = {
        "movie_detail": movie_detail,
        "movie_videos": movie_videos,
    }

    return render(request, "movie_detail.html", context)
