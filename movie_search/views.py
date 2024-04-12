from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from movie_search import media
from movie_search.decorators import timing
from movie_search.media import (
    MovieService,
    TVSeriesService,
    PersonService,
)

from .models import (
    Movie,
    MovieVideo,
    MovieWatchList,
    TVSeries,
    TVSeriesVideo,
)
from .tmdb_api import TMDBApi
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

tmdb_api = TMDBApi()


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
    trending = tmdb_api.get_data_from_endpoint("/trending/all/day")
    context = {"trending": trending}
    return render(request, "home.html", context)


@login_required
def add_movie_to_watch_list(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    MovieWatchList.objects.get_or_create(user=request.user, movie=movie)
    messages.success(
        request, f"Successfully added movie {movie.title} to your watch list"
    )
    return redirect("watch_list")


@login_required
def remove_movie_from_watch_list(request, movie_id):
    movie_in_watchlist = get_object_or_404(
        MovieWatchList, user=request.user, pk=movie_id
    )
    movie_in_watchlist.delete()
    return redirect("watch_list")


@login_required
def movie_watch_list(request):
    movie_watch_list = MovieWatchList.objects.filter(user=request.user).select_related(
        "movie"
    )
    return render(
        request, "movie_watch_list.html", {"movie_watch_list": movie_watch_list}
    )


def get_movie_from_db_or_api(request, movie_id):
    # Check if the movie exists in the database
    movie_service = MovieService(request.tmdb_api)
    try:
        movie = Movie.objects.get(movie_id=movie_id)
        # If the movie exists, fetch related objects
        videos = MovieVideo.objects.filter(movie=movie)
    except Movie.DoesNotExist:
        # Fetch movie and video data from the API if the movie doesn't exist in the DB
        movie_data, video_data = movie_service.fetch_movie_data_from_api(movie_id)
        movie, videos = movie_service.store_media_data((movie_data, video_data))
    return movie, videos


def get_tv_from_db_or_api(request, series_id):
    # Check if the tv exists in the database
    tv_service = TVSeriesService(request.tmdb_api)
    try:
        tvseries = TVSeries.objects.get(series_id=series_id)
        videos = TVSeriesVideo.objects.filter(tvseries=tvseries)
    except TVSeries.DoesNotExist:
        tv_data, videos_data = tv_service.fetch_tv_data_from_api(series_id)
        tvseries, videos = tv_service.store_media_data((tv_data, videos_data))
    return tvseries, videos


def _get_media_list(request, media_type, media_list_type, template_name):
    data = request.get_data_from_endpoint(f"/{media_type}/{media_list_type}")
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


def movie(request, movie_id):
    movie, videos = get_movie_from_db_or_api(request, movie_id)
    print("Movie: ", movie)
    # print("MovieVideos: ", videos)
    print("MovieRecommendations: ", movie.recommendation.all())
    context = {
        "movie": movie,
        "videos": videos,
    }
    return render(request, "movie.html", context)


def tv(request, series_id):
    tvseries, videos = get_tv_from_db_or_api(request, series_id)
    print("TV Series: ", tvseries)
    print("TV Videos: ", videos)
    context = {
        "tv": tvseries,
        "videos": videos,
    }
    return render(request, "tv.html", context)


# Common TV Views
def tv_popular(request):
    return _get_media_list(request, "tv", "popular", "tv_popular.html")


def tv_top_rated(request):
    return _get_media_list(request, "tv", "top_rated", "tv_top_rated.html")


def tv_trending_week(request):
    return _get_media_list(request, "trending/tv", "week", "tv_trending.html")


def tv_air(request):
    return _get_media_list(request, "tv", "on_the_air", "tv_air.html")


def tv_air_today(request):
    return _get_media_list(request, "tv", "airing_today", "tv_air_today.html")


# Discover Movie View
def movie_discover(request):
    movie_service = MovieService(request.tmdb_api)

    # Extract parameters from request and construct kwargs
    discover_params = {
        "with_genres": request.GET.getlist("genre"),
        "person_name": request.GET.get("personName"),
        "sort_options": request.GET.getlist("sort"),
        "region": request.GET.get("region"),
        "watch_region": request.GET.get("watch_region"),
        "watch_provider_names": request.GET.getlist("providers"),
        "year": request.GET.get("year"),
    }

    # Clean up discover_params to remove None values AND any empty lists or strings
    discover_params = {k: v for k, v in discover_params.items() if v}

    # Pass parameters as kwargs to the service layer
    movie_discover_data = movie_service.get_movie_discover_data(**discover_params)

    return render(
        request, "movie_discover.html", {"movie_discover_data": movie_discover_data}
    )


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
    person = request.tmdb_api.get_data_by_query(f"/search/person", query, "name")
    person_id = request.tmdb_api.lookup_id_in_data_by_query(person, query)

    if choice == "movie_credits":
        return render_person_movie_credits(request, person_id)

    return render_person_tv_credits(request, person_id)


def render_person_movie_credits(request, person_id):
    person = request.tmdb_api.get_data_from_endpoint(f"/person/{person_id}/movie_credits")
    if not person:
        context = {"message": "No data available"}
    else:
        context = {"person": person}
    return render(request, "movie_search_person.html", context)


def render_person_tv_credits(request, person_id):
    person = request.tmdb_api.get_data_from_endpoint(f"/person/{person_id}/tv_credits")
    if not person:
        context = {"message": "No data available"}
    else:
        context = {"person": person}
    return render(request, "tv_search_person.html", context)


def handle_movie_search(request, query, choice):
    movie = request.tmdb_api.get_data_by_query(f"/search/movie", query, "original_title")
    movie_id = request.tmdb_api.lookup_id_in_data_by_query(movie, query)
    if choice == "general":
        return render_movie(request, movie_id)
    return render_movie_sim_or_rec(request, movie_id, choice)


def render_movie(request, movie_id):
    movie, videos = get_movie_from_db_or_api(request, movie_id)
    context = {
        "movie": movie,
        "videos": videos,
    }
    return render(request, "movie.html", context)


def render_movie_sim_or_rec(request, movie_id, choice):
    movie = request.tmdb_api.get_data_from_endpoint(f"/movie/{movie_id}/{choice}")
    return render(
        request, "movie_search_sim_rec.html", {"movie": movie, "choice": choice}
    )


def handle_tv_search(request, query, choice):
    tv = request.tmdb_api.get_data_by_query(f"/search/tv", query, "original_name")
    series_id = request.tmdb_api.lookup_id_in_data_by_query(tv, query)

    if choice == "general":
        return render_tv(request, series_id)

    return render_tv_sim_or_rec(request, series_id, choice)


def render_tv(request, series_id):
    tvseries, videos = get_tv_from_db_or_api(request, series_id)
    context = {
        "tv": tvseries,
        "videos": videos,
    }

    return render(request, "tv.html", context)


def render_tv_sim_or_rec(request, series_id, choice):
    tvseries = request.tmdb_api.get_data_from_endpoint(f"/tv/{series_id}/{choice}")
    return render(request, "tv_search_sim_rec.html", {"tv": tvseries, "choice": choice})