from pprint import pprint

import requests
from django.http import HttpResponse
from django.shortcuts import render

from movie_search import media_api
from movie_search.decorators import timing

from .models import Movie, Video, Genre, Provider, Recommendation


# Create your views here.
def home(request):
    trending = media_api.get_media_data("/trending/all/day")
    context = {"trending": trending}
    return render(request, "home.html", context)


def _get_movie_or_tv_popular(request, media_type_):
    popular = media_api.get_media_data(f"/{media_type_}/popular")
    context = {
        "popular": popular,
    }
    return render(request, f"{media_type_}_popular.html", context)


def movies_popular(request):
    return _get_movie_or_tv_popular(request, "movie")


def movies_top_rated(request):
    return _get_movie_or_tv_top(request, "movie")


def _get_movie_or_tv_top(request, media_type_):
    top_rated = media_api.get_media_data(f"/{media_type_}/top_rated")

    context = {
        "top_rated": top_rated,
    }

    return render(request, f"{media_type_}_top_rated.html", context)


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


def movies_trending_week(request):
    return _get_movie_or_tv_trending(request, "movie")


def _get_movie_or_tv_trending(request, media_type_):
    trending = media_api.get_media_data(f"/trending/{media_type_}/week")

    context = {
        "trending": trending,
    }

    return render(request, f"{media_type_}_trending.html", context)


def discover(request):
    genre_names = request.GET.getlist("genre")
    print("GENRE NAMES: ", genre_names)

    # Get genre IDs
    with_genres = Genre.objects.filter(name__in=genre_names).values_list(
        "genre_id", flat=True
    )
    print("WITH GENRES: ", with_genres)

    person_name = request.GET.get("personName")

    if person_name:
        person_name = person_name.lower()
        person = media_api.get_person("/search/person", person_name)
        print("Person: ", person)

        person = {person.lower(): idx for person, idx in person.items()}
        print("Person Dictionary: ", person)

        # Get person id based on person query
        with_people = person.get(person_name)
        print("PERSON ID", with_people)
    else:
        with_people = None

    sort_by = request.GET.getlist("sort")
    print("SORT BY: ", sort_by)

    region = request.GET.get("region")
    print("REGION: ", region)

    watch_region = request.GET.get("watch_region")
    print("WATCH REGION: ", region)

    watch_provider_names = request.GET.getlist("providers")
    print("WATCH PROVIDERS: ", watch_provider_names)

    # Get Watch Provider IDs
    with_watch_providers = Provider.objects.filter(
        name__in=watch_provider_names
    ).values_list("provider_id", flat=True)
    print("WITH WATCH PROVIDERS: ", with_watch_providers)

    primary_release_year = request.GET.get("year")

    if primary_release_year:
        primary_release_year = int(primary_release_year)

    # TODO: media_type is not defined
    # print(
    #    "PRIMARY RELEASE YEAR: ", primary_release_year, media_type(primary_release_year)
    # )

    print("REQUEST: ", request.GET)
    data = media_api.get_media_data(
        "/discover/movie",
        region=region,
        primary_release_year=primary_release_year,
        with_genres=list(with_genres),
        sort_by=sort_by,
        watch_region=watch_region,
        with_watch_providers=list(with_watch_providers),
        with_people=with_people,
    )

    context = {"data": data}

    return render(request, "discover.html", context)


def search(request):
    query = request.GET.get("query")
    year = request.GET.get("year")
    media_type = request.GET.get("type")
    choice = request.GET.get("choice")

    if not query:
        return render(request, "error.html")

    query = query.lower()

    if media_type == "person":
        return search_person(request, query, choice)

    return search_media(request, query, year, media_type, choice)


def search_person(request, query, choice):
    person = media_api.get_person(f"/search/person", query)
    person = {p.lower(): idx for p, idx in person.items()}
    person_id = person.get(query)
    url_path = "movie_detail" if choice == "movie_credits" else "tv_detail"
    data = media_api.get_media_data(f"/person/{person_id}/{choice}")
    context = {
        "data": data,
        "type": "person",
        "choice": choice,
        "url_path": url_path,
    }
    return render(request, "person_search.html", context)


def search_media(request, query, year, media_type, choice):
    media = media_api.get_media(f"/search/{media_type}", query, media_type, year=year)
    media = {m.lower(): idx for m, idx in media.items()}
    media_id = media.get(query)
    url_path = "movie_detail" if media_type == "movie" else "tv_detail"

    if choice == "general":
        return search_general(request, media_type, media_id, url_path)

    return search_sim_or_rec(request, media_type, media_id, choice, url_path)


def search_general(request, media_type, media_id, url_path):
    media_detail = media_api.get_media_data(f"/{media_type}/{media_id}")
    media_videos = media_api.get_media_data(f"/{media_type}/{media_id}/videos")
    recommendations = media_api.get_media_data(
        f"/{media_type}/{media_id}/recommendations"
    )
    context = {
        f"{media_type}_detail": media_detail,
        f"{media_type}_videos": media_videos,
        "type": media_type,
        "url_path": url_path,
        "recommendations": recommendations,
    }
    return render(request, f"{media_type}_detail.html", context)


def search_sim_or_rec(request, media_type, media_id, choice, url_path):
    data = media_api.get_media_data(f"/{media_type}/{media_id}/{choice}")
    context = {
        "data": data,
        "type": media_type,
        "choice": choice,
        "url_path": url_path,
    }
    return render(request, "media_search.html", context)


def get_movie_genres(genres):
    movie_genres = []

    for row in genres:
        genre, inserted = Genre.objects.get_or_create(
            name=row.get("name", ""),
            genre_id=row.get("id", 0),
        )
        movie_genres.append(genre)

    return movie_genres


def get_movie_videos(obj_id):
    videos = media_api.get_media_data(f"/movie/{obj_id}/videos")
    movie_videos = []

    video_response = videos.get("results")

    for row in video_response:
        video, inserted = Video.objects.get_or_create(
            name=row.get("name", ""),
            key=row.get("key",""),
        )

        movie_videos.append(video)

    return movie_videos

def get_movie_recs(obj_id):
    recs = media_api.get_media_data(f"/movie/{obj_id}/recommendations")
    movie_recs = []

    recs_response = recs.get("results")

    for row in recs_response:
        rec, inserted = Recommendation.objects.get_or_create(
            movie_id=row.get("id", 0),
            poster_path=row.get("poster_path",""),
        )

        movie_recs.append(rec)

    return movie_recs


def movie_detail(request, obj_id):
    try:
        print("movie exists in DB")
        movie_detail = Movie.objects.get(movie_id=obj_id)

        context = {
            "movie_detail": movie_detail,
        }

    except Movie.DoesNotExist:
        # call only happens if movie not in db
        print("movie not in DB")
        movie_from_api = media_api.get_media_data(f"/movie/{obj_id}")
        genres = movie_from_api.get("genres")

        movie_detail, created = Movie.objects.get_or_create(
            movie_id=obj_id,
            title=movie_from_api.get("title", ""),
            backdrop_path=movie_from_api.get("backdrop_path", ""),
            tagline=movie_from_api.get("tagline", ""),
            vote_count=movie_from_api.get("vote_count", 0),
            vote_average=movie_from_api.get("vote_average", 0),
            popularity=movie_from_api.get("popularity", 0),
            release_date=movie_from_api.get("release_data", ""),
            runtime=movie_from_api.get("runtime", 0),
            production_company=movie_from_api.get("production_company", ""),
            overview=movie_from_api.get("overview", ""),
            budget=movie_from_api.get("budget", 0),
            revenue=movie_from_api.get("revenue", 0),
            homepage=movie_from_api.get("homepage", ""),
        )

        if genres is not None:
            # Get matching themes from M2M relationship
            movie_genres =  get_movie_genres(genres)
            movie_detail.genres.add(*movie_genres)

        movie_videos = get_movie_videos(obj_id)
        movie_detail.video.add(*movie_videos)
    
        movie_recs = get_movie_recs(obj_id)
        movie_detail.recommendation.add(*movie_recs)

        context = {
            "movie_detail": movie_detail,
        }

    return render(request, "movie_detail.html", context)


def tv_popular(request):
    return _get_movie_or_tv_popular(request, "tv")


def tv_top_rated(request):
    top_rated = media_api.get_media_data("/tv/top_rated")

    return _get_movie_or_tv_top(request, "tv")


def tv_trending_week(request):
    return _get_movie_or_tv_trending(request, "tv")


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
    tv_detail = media_api.get_media_data(f"/tv/{obj_id}")
    # pprint("TV DETAIL: ", tv_detail)

    tv_videos = media_api.get_media_data(f"/tv/{obj_id}/videos")

    context = {
        "tv_detail": tv_detail,
        "tv_videos": tv_videos,
        "type": "tv",
    }

    return render(request, "tv_detail.html", context)
