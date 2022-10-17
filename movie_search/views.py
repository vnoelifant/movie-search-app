import requests
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint

from movie_search import media_api
from movie_search.models import Search

# Create your views here.
def home(request):
    return render(request, "home.html")


def movies_popular(request):

    popular = media_api.get_media_data("/movie/popular")

    context = {
        "popular": popular,
    }

    return render(request, "movies_popular.html", context)


def movies_top_rated(request):

    top_rated = media_api.get_media_data("/movie/top_rated")
    context = {
        "top_rated": top_rated,
    }

    return render(request, "movies_top_rated.html", context)


def movies_now_playing(request):

    now_playing = media_api.get_media_data("/movie/now_playing")

    context = {
        "now_playing": now_playing,
    }

    return render(request, "movies_now_playing.html", context)


def movies_upcoming(request):

    upcoming = media_api.get_media_data("/movie/upcoming")

    context = {
        "upcoming": upcoming,
    }

    return render(request, "movies_upcoming.html", context)


def movies_trending(request):

    trending = media_api.get_media_data("/trending/movie/week")

    context = {
        "trending": trending,
    }

    return render(request, "movies_trending.html", context)


def media_similar(request):

    query = request.GET.get("query")
    year = request.GET.get("year")
    type = request.GET.get("type")
    choice = request.GET.get("choice")

    if not query:

        return render(request, "error.html")

    else:

        print("TYPE: ", type)

        print("CHOICE: ", choice)

        query = query.lower()

        print("QUERY: ", query)

        # Get a dictionary of movie details based on text query
        media = media_api.get_media(f"/search/{type}", query, year=year)

        media = {media.lower(): idx for media, idx in media.items()}

        # Get media id based on selected media title
        media_id = media.get(query)

        data = media_api.get_media_data(f"/{type}/{media_id}/{choice}")

        context = {"data": data, "type": type, "choice": choice}

        return render(request, "media_similar.html", context)


def movie_detail(request, movie_id):

    movie_detail = media_api.get_movie_detail(f"/movie/{movie_id}")
    # print("MOVIE DETAIL: ", movie_detail)

    movie_videos = media_api.get_movie_videos(f"/movie/{movie_id}/videos")

    context = {
        "movie_detail": movie_detail,
        "movie_videos": movie_videos,
    }

    return render(request, "movie_detail.html", context)
