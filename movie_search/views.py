from pprint import pprint

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from movie_search import media
from movie_search.decorators import timing
from movie_search.media import (
    MovieStrategy,
    TVSeriesStrategy,
    PersonStrategy,
    MediaContext,
)

from .models import (
    Movie,
    MovieVideo,
    MovieGenre,
    MovieProvider,
    MovieRecommendation,
    MovieWatchList,
    TVSeries,
    TVSeriesVideo,
    TVSeriesGenre,
    TVSeriesProvider,
    TVSeriesRecommendation,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to a homepage or dashboard
        else:
            # Return an 'invalid login' error message.
            return render(
                request, "login.html", {"error": "Invalid username or password."}
            )
    else:
        # User is accessing the login page via GET request.
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))  # Redirect to home page after logout


def home(request):
    trending = media.fetch_data_from_api("/trending/all/day")
    context = {"trending": trending}
    return render(request, "home.html", context)


@login_required
def add_to_watch_list(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    WatchList.objects.get_or_create(user=request.user, movie=movie)
    messages.success(
        request, f"Successfully added movie {movie.title} to your watch list"
    )
    return redirect("watch_list")


@login_required
def remove_from_watch_list(request, movie_id):
    movie_in_watchlist = get_object_or_404(
        WatchList, user=request.user, movie_id=movie_id
    )
    movie_in_watchlist.delete()
    return redirect("watch_list")


@login_required
def watch_list(request):
    watch_list = MovieWatchList.objects.filter(user=request.user).select_related(
        "movie"
    )
    return render(request, "watch_list.htmld", {"watch_list": watch_list})


def get_movie_from_db_or_api(tmdb_id, media_context):
    # Check if the movie exists in the database
    try:
        movie = Movie.objects.get(tmdb_id=tmdb_id)
        # If the movie exists, fetch related objects
        videos = MovieVideo.objects.filter(movie=movie)
    except Movie.DoesNotExist:
        # If the movie does not exist, use context class to fetch and store data based on concrete class
        movie, videos = media_context.process_media(tmdb_id)
    return movie, videos


def get_tv_from_db_or_api(tmdb_id, media_context):
    # Check if the tv exists in the database
    try:
        tv = TVSeries.objects.get(tmdb_id=tmdb_id)
        # If the movie exists, fetch related objects
        videos = TVSeriesVideo.objects.filter(movie=movie)
    except TVSeries.DoesNotExist:
        # If the movie does not exist, use media.py to fetch from the API and store in the database
        tv, videos = media_context.process_media(tmdb_id)
    return tv, videos


def _get_media_list(request, media_type, media_list_type, template_name):
    data = media.fetch_data_from_api(f"/{media_type}/{media_list_type}")
    context = {media_list_type: data}

    return render(request, template_name, context)


# Common Movie Views
def movies_popular(request):
    return _get_media_list(request, "movie", "popular", "movie_popular.html")


def movies_top_rated(request):
    return _get_media_list(request, "movie", "top_rated", "movie_top_rated.html")


def movies_now_playing(request):
    return _get_media_list(request, "movie", "now_playing", "movie_now_playing.html")


def movies_upcoming(request):
    return _get_media_list(request, "movie", "upcoming", "movie_upcoming.html")


def movies_trending_week(request):
    return _get_media_list(request, "trending/movie", "week", "movie_trending.html")


def movie(request, tmdb_id):
    movie_strategy = MovieStrategy()
    media_context = MediaContext(movie_strategy)
    movie, videos = get_movie_from_db_or_api(tmdb_id, media_context)
    context = {
        "movie": movie,
        "videos": videos,
    }
    return render(request, "movie.html", context)


def tv(request, tmdb_id):
    tv_strategy = TVSeriesStrategy()
    media_context = MediaContext(tv_strategy)
    tv, videos = get_tv_from_db_or_api(tmdb_id, media_context)
    context = {
        "tv": tv,
        "videos": videos,
    }
    return render(request, "tv.html", context)


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

# Discover Movie View
def movie_discover(request):
    movie_strategy = MovieStrategy()
    media_context = MediaContext(movie_strategy)

    (
        genres,
        person_id,
        sort_options,
        region,
        watch_region,
        providers,
        year,
    ) = process_movie_discover_request(request, media_context)

    data = media_context.get_discover_data(
        genres, person_id, sort_options, region, watch_region, providers, year
    )

    return render(request, "discover.html", {"data": data})


def process_movie_discover_request(request, media_context):
    # Process genres
    genre_names = request.GET.getlist("genre")
    genres = media_context.get_genres_from_discover(genre_names)

    # Process person
    if person_name:
        person_strategy = PersonStrategy()
        person_data = person_strategy.fetch_person_data(person_name)
        person_id = person_strategy.get_person_id(person_data, person_name)
    else:
        person_id = None

    # Other parameters
    sort_options = request.GET.getlist("sort")
    region = request.GET.get("region")
    watch_region = request.GET.get("watch_region")
    watch_provider_names = request.GET.getlist("providers")
    providers = media_context.get_providers_from_discover(watch_provider_names)

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

    elif media_type == "movie":
        return handle_movie_search(request, query, choice)

    return handle_tv_search(request, query, choice)


def handle_person_search(request, query, choice):
    person = media.fetch_api_data_by_query(f"/search/person", query, "name")
    person_id = media.lookup_id_in_data_by_query(person, query)

    if choice == "movie_credits":
        return render_person_movie_credits(request, person_id)

    return render_person_tv_credits(request, person_id)


def render_person_movie_credits(request, person_id):
    person = media.fetch_data_from_api(f"/person/{person_id}/movie_credits")
    if not person:
        context = {"message": "No data available"}
    else:
        context = {"person": person}
    return render(request, "movie_search_person.html", context)


def render_person_tv_credits(request, person_id):
    person = media.fetch_data_from_api(f"/person/{person_id}/tv_credits")
    if not person:
        context = {"message": "No data available"}
    else:
        context = {"person": person}
    return render(request, "tv_search_person.html", context)


def handle_movie_search(request, query, choice):
    movie = media.fetch_api_data_by_query(f"/search/movie", query, "original_title")
    tmdb_id = media.lookup_id_in_data_by_query(movie, query)
    if choice == "general":
        return render_movie(request, tmdb_id)
    return render_movie_sim_or_rec(request, tmdb_id, choice)


def render_movie(request, tmdb_id):
    movie_strategy = MovieStrategy()
    media_context = MediaContext(movie_strategy)
    movie, videos = get_movie_from_db_or_api(tmdb_id, media_context)
    context = {
        "movie": movie,
        "videos": videos,
    }
    return render(request, "movie.html", context)


def render_movie_sim_or_rec(request, tmdb_id, choice):
    movie = media.fetch_data_from_api(f"/movie/{tmdb_id}/{choice}")
    return render(
        request, "movie_search_sim_rec.html", {"movie": movie, "choice": choice}
    )


def handle_tv_search(request, query, choice):
    tv = media.fetch_api_data_by_query(f"/search/tv", query, "original_name")
    tv_id = media.lookup_id_in_data_by_query(tv, query)

    if choice == "general":
        return render_tv_detail(request, tv_id)

    return render_tv_sim_or_rec(request, tv_id, choice)


def render_tv(request, tv_id):
    movie_strategy = MovieStrategy()
    media_context = MediaContext(movie_strategy)
    tv, videos = get_tv_from_db_or_api(tmdb_id, media_context)
    context = {
        "tv": tv,
        "videos": videos,
    }
    
    return render(request, "tv.html", context)


def render_tv_sim_or_rec(request, tv_id, choice):
    tv = media.fetch_data_from_api(f"/tv/{tv_id}/{choice}")
    return render(request, "tv_search_sim_rec.html", {"tv": tv, "choice": choice})
