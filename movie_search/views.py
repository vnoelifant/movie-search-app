from pprint import pprint

import requests
from django.http import HttpResponse
from django.shortcuts import render

from movie_search import media_api
from movie_search import movies
from movie_search.decorators import timing

from .models import Movie, Video, Genre, Provider, Recommendation


# Create your views here.

def home(request):
    trending = media_api.get_data_from_endpoint("/trending/all/day")
    context = {"trending": trending}
    return render(request, "home.html", context)

def _get_media_list(request, media_type, media_list_type, template_name):
    data = media_api.get_data_from_endpoint(f"/{media_type}/{media_list_type}")
    context = {media_list_type: data}
    return render(request, template_name, context)

# Common Movie Views
def movies_popular(request):
    return _get_media_list(request, "movie", "popular", "movie_popular.html")

def movies_top_rated(request):
    return _get_media_list(request, "movie", "top_rated", "movie_top_rated.html")

def movies_now_playing(request):
    return _get_media_list(request, "movie", "now_playing", "movies_now_playing.html")

def movies_upcoming(request):
    return _get_media_list(request, "movie", "upcoming", "movies_upcoming.html")

def movies_trending_week(request):
    return _get_media_list(request, "movie", "trending/week", "movie_trending.html")

def movie_detail(request, movie_id):
    context = movies.get_movie_detail(movie_id)
    return render(request, "movie_detail.html", context)

# Common TV Views
def tv_popular(request):
    return _get_media_list(request, "tv", "popular", "tv_popular.html")

def tv_top_rated(request):
    return _get_media_list(request, "tv", "top_rated", "tv_top_rated.html")

def tv_trending_week(request):
    return _get_media_list(request, "tv", "trending/week", "tv_trending.html")

def tv_air(request):
    return _get_media_list(request, "tv", "on_the_air", "tv_air.html")

def tv_air_today(request):
    return _get_media_list(request, "tv", "airing_today", "tv_air_today.html")

def tv_detail(request, tv_id):
    tv_detail = media_api.get_data_from_endpoint(f"/tv/{tv_id}")
    tv_videos = media_api.get_data_from_endpoint(f"/tv/{tv_id}/videos")

    context = {
        "tv_detail": tv_detail,
        "tv_videos": tv_videos,
    }

    return render(request, "tv_detail.html", context)

# Discover Movie View
def discover(request):
    (
        genres,
        person_id,
        sort_options,
        region,
        watch_region,
        providers,
        year,
    ) =  process_movie_discover_request(request)

    data = movies.get_movie_discover_data(
        genres, person_id, sort_options, region, watch_region, providers, year
    )

    return render(request, "discover.html", {"data": data})


def process_movie_discover_request(request):
    # Process genres
    genre_names = request.GET.getlist("genre")
    genres = movies.get_genres_from_discover(genre_names)

    # Process person
    person_name = request.GET.get("personName")
    person = media_api.get_person("/search/person", person_name)
    person_id = movies.get_person_id_from_name(person, person_name) if person_name else None

    # Other parameters
    sort_options = request.GET.getlist("sort")
    region = request.GET.get("region")
    watch_region = request.GET.get("watch_region")
    watch_provider_names = request.GET.getlist("providers")
    providers = movies.get_providers_from_discover(watch_provider_names)

    # Process year
    year = request.GET.get("year")
    if year:
        year = int(year)

    return genres, person_id, sort_options, region, watch_region, providers, year


# Search Views
def search(request):
    query = request.GET.get("query")
    media_type = request.GET.get("type")
    choice = request.GET.get("choice")

    if not query:
        return render(request, "error.html")

    query = query.lower()

    if media_type == "person":
        return handle_person_search(request, query, choice)

    return handle_movie_search(request, query, choice)


def handle_person_search(request, query, choice):
    person = media_api.get_person(f"/search/person", query)
    person_id = movies.get_person_id_from_name(person, query)

    if choice == "movie_credits":
        return render_person_movie_credits(request, person_id)

    return render_person_tv_credits(request, person_id)


def render_person_movie_credits(request, person_id):
    person = media_api.get_data_from_endpoint(f"/person/{person_id}/movie_credits")
    return render(request, "movie_search_person.html", {"person": person})


def render_person_tv_credits(request, person_id):
    person = media_api.get_data_from_endpoint(f"/person/{person_id}/tv_credits")
    return render(request, "tv_search_person.html", {"person": person})


def handle_movie_search(request, query, choice):
    movie = media_api.get_movie(f"/search/movie", query)
    movie_id = movies.get_movie_id_from_query(movie, query)

    if choice == "general":
        return movie_detail(request, movie_id)

    return render_movie_sim_or_rec(request, movie_id, choice)


def render_movie_sim_or_rec(request, movie_id, choice):
    movie = media_api.get_data_from_endpoint(f"/movie/{movie_id}/{choice}")
    return render(
        request, "movie_search_sim_rec.html", {"movie": movie, "choice": choice}
    )
















