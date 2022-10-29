import requests
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint

from movie_search import media_api
from movie_search.models import Search

# Create your views here.
def home(request):

    trending = media_api.get_media_data("/trending/all/day")
    # pprint("TRENDING: ", trending)

    context = {"trending": trending}

    return render(request, "home.html", context)


def movies_popular(request):

    popular = media_api.get_media_data("/movie/popular")
    # pprint("POPULAR: ", popular)

    context = {
        "popular": popular,
    }

    return render(request, "movies_popular.html", context)


def movies_top_rated(request):

    top_rated = media_api.get_media_data("/movie/top_rated")
    # pprint("TOP RATED: ", top_rated)

    context = {
        "top_rated": top_rated,
    }

    return render(request, "movies_top_rated.html", context)


def movies_now_playing(request):

    now_playing = media_api.get_media_data("/movie/now_playing")
    # pprint("NOW PLAYING: ", now_playing)

    context = {
        "now_playing": now_playing,
    }

    return render(request, "movies_now_playing.html", context)


def movies_upcoming(request):

    upcoming = media_api.get_media_data("/movie/upcoming")
    # pprint("UPCOMING ", upcoming)

    context = {
        "upcoming": upcoming,
    }

    return render(request, "movies_upcoming.html", context)


def movies_trending_week(request):

    trending = media_api.get_media_data("/trending/movie/week")
    # pprint("TRENDING: ", trending)

    context = {
        "trending": trending,
    }

    return render(request, "movies_trending.html", context)


def discover(request):

    # Get a dictionary of available genres
    genres = media_api.get_genres("/genre/movie/list")

    genre_list = request.GET.getlist("genre")
    print("GENRE: ", genre_list)

    # Get genre ID/s
    genre_id = [genres.get(genre) for genre in genre_list]
    print("GENRE ID: ", genre_id)

    sort_option = request.GET.get("sort")
    print("SORT BY: ", sort_option)


    data = media_api.get_media_data("/discover/movie", genre_id=genre_id, sort_option=sort_option)

    context = {"data": data}

    return render(request, "discover.html", context)


def media_search(request):

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

        # Get a dictionary of media details based on text query
        media = media_api.get_media(f"/search/{type}", query, type, year=year)

        media = {media.lower(): idx for media, idx in media.items()}

        # Get media id based on selected media title
        media_id = media.get(query)

        data = media_api.get_media_data(f"/{type}/{media_id}/{choice}")
        # pprint("DATA: ", data)

        url_path = "movie_detail" if type == "movie" else "tv_detail"
        context = {"data": data, "type": type, "choice": choice, "url_path": url_path}

        return render(request, "media_search.html", context)


def movie_detail(request, obj_id):

    movie_detail = media_api.get_media_detail(f"/movie/{obj_id}")
    # pprint("MOVIE DETAIL: ", movie_detail)

    movie_videos = media_api.get_media_detail(f"/movie/{obj_id}/videos")

    context = {
        "movie_detail": movie_detail,
        "movie_videos": movie_videos,
        "type": "movie",
    }

    return render(request, "movie_detail.html", context)


def tv_popular(request):

    popular = media_api.get_media_data("/tv/popular")
    # pprint("POPULAR: ", popular)

    context = {
        "popular": popular,
    }

    return render(request, "tv_popular.html", context)


def tv_top_rated(request):

    top_rated = media_api.get_media_data("/tv/top_rated")
    # pprint("TOP RATED: ", top_rated)

    context = {
        "top_rated": top_rated,
    }

    return render(request, "tv_top_rated.html", context)


def tv_trending_week(request):

    trending = media_api.get_media_data("/trending/tv/week")
    # pprint("TRENDING: ", trending)

    context = {
        "trending": trending,
    }

    return render(request, "tv_trending.html", context)


def tv_air(request):

    tv_air = media_api.get_media_data("/tv/on_the_air")

    context = {
        "tv_air": tv_air,
    }

    return render(request, "tv_air.html", context)


def tv_air_today(request):

    tv_air_today = media_api.get_media_data("/tv/airing_today")

    context = {
        "tv_air_today": tv_air_today,
    }

    return render(request, "tv_air_today.html", context)


def tv_detail(request, obj_id):

    tv_detail = media_api.get_media_detail(f"/tv/{obj_id}")
    # pprint("TV DETAIL: ", tv_detail)

    tv_videos = media_api.get_media_detail(f"/tv/{obj_id}/videos")

    context = {
        "tv_detail": tv_detail,
        "tv_videos": tv_videos,
        "type": "tv",
    }

    return render(request, "tv_detail.html", context)
