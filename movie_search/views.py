from pprint import pprint

import requests
from django.http import HttpResponse
from django.shortcuts import render

from movie_search import media_api
from movie_search.decorators import timing
from movie_search.models import Genre, Provider

from .models import Movie


# Create your views here.
def home(request):
    trending = media_api.get_media_data("/trending/all/day")
    # pprint("TRENDING: ", trending)

    context = {"trending": trending}

    return render(request, "home.html", context)


def _get_movie_or_tv_popular(request, type_):
    popular = media_api.get_media_data(f"/{type_}/popular")
    context = {
        "popular": popular,
    }
    return render(request, f"{type_}_popular.html", context)


def movies_popular(request):
    return _get_movie_or_tv_popular(request, "movie")


def movies_top_rated(request):
    return _get_movie_or_tv_top(request, "movie")


def _get_movie_or_tv_top(request, type_):
    top_rated = media_api.get_media_data(f"/{type_}/top_rated")

    context = {
        "top_rated": top_rated,
    }

    return render(request, f"{type_}_top_rated.html", context)


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
    return _get_movie_or_tv_trending(request, "movie")


def _get_movie_or_tv_trending(request, type_):
    trending = media_api.get_media_data(f"/trending/{type_}/week")

    context = {
        "trending": trending,
    }

    return render(request, f"{type_}_trending.html", context)


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

    print("PRIMARY RELEASE YEAR: ", primary_release_year, type(primary_release_year))

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


def get_search_general(type, media_id, url_path):
    # TODO: Cache this data to increase speed
    media_detail = media_api.get_media_data(f"/{type}/{media_id}")
    # print("MEDIA DETAIL: ", media_detail)

    media_videos = media_api.get_media_data(f"/{type}/{media_id}/videos")
    recommendations = media_api.get_media_data(f"/{type}/{media_id}/recommendations")

    return {
        f"{type}_detail": media_detail,
        f"{type}_videos": media_videos,
        "type": type,
        "url_path": url_path,
        "recommendations": recommendations,
    }


def get_search_sim_or_rec(type, media_id, choice, url_path):
    data = media_api.get_media_data(f"/{type}/{media_id}/{choice}")

    return {
        "data": data,
        "type": type,
        "choice": choice,
        "url_path": url_path,
    }


def get_search_media_response(request, type, query, year, choice):
    # Get a dictionary of media details based on text query
    media = media_api.get_media(f"/search/{type}", query, type, year=year)

    media = {media.lower(): idx for media, idx in media.items()}

    # Get media id based on selected media title
    media_id = media.get(query)
    print("MEDIA ID", media_id)

    url_path = "movie_detail" if type == "movie" else "tv_detail"

    if choice != "general":
        print("Getting Recommended/Similar Search Context")
        similar_or_rec_context = get_search_sim_or_rec(
            type, media_id, choice, url_path
        )

        return render(request, "media_search.html", similar_or_rec_context)

    print("Getting General Media Detail Search Context")
    general_context = get_search_general(type, media_id, url_path)
    return render(request, f"{type}_detail.html", general_context)


def search(request):
    query = request.GET.get("query")
    year = request.GET.get("year")
    type = request.GET.get("type")
    choice = request.GET.get("choice")

    if not query:
        return render(request, "error.html")

    print("TYPE: ", type)

    print("CHOICE: ", choice)

    query = query.lower()

    print("QUERY: ", query)

    if type != "person":
        search_media_response = get_search_media_response(
            request=request, type=type, query=query, year=year, choice=choice
        )

        return search_media_response

    search_person_response = get_search_person_response(
        request=request, type=type, query=query, choice=choice
    )

    return search_person_response


def get_search_person(type, query, choice):
    person = media_api.get_person(f"/search/{type}", query)
    person = {person.lower(): idx for person, idx in person.items()}
    print("Person Dictionary: ", person)
    # Get person id based on person query
    person_id = person.get(query)
    print("PERSON ID", person_id)

    data = media_api.get_media_data(f"/{type}/{person_id}/{choice}")

    url_path = "movie_detail" if choice == "movie_credits" else "tv_detail"

    return {
        "data": data,
        "type": type,
        "choice": choice,
        "url_path": url_path,
    }


def get_search_person_response(request, type, query, choice):
    print("Getting Person Search Context")
    person_context = get_search_person(type=type, query=query, choice=choice)
    return render(request, "person_search.html", person_context)


def get_movie_genres(movie):
    movie_genres = []

    genres = movie.get("genres")

    if genres is not None:
        for row in genres:
            genre = Genre(
                name=row.get("name", ""),
                genre_id=row.get("id", ""),
            )
            movie_genres.append(genre)
        Genre.objects.bulk_create(movie_genres)

    return movie_genres

def get_movie_videos(movie):
    movie_videos = []

    videos = movie.get("videos")

    #YouTubue's embed URL
    embed_url = "https://www.youtube.com/embed/"

    if videos is not None:
        for row in videos:
            video = Video(
                name=row.get("name", ""),
                key=row.get("id", ""),
            )

            final_video_url = embed_url + key
            final_video = f"<div class='embed-responsive embed-responsive-16by9'> <iframe class='embed-responsive-item' style='height: 400px; width:800px; margin-left:50px' src={final_video_url}></iframe> </div>"
            movie_videos.append(final_video)
        Video.objects.bulk_create(movie_videos)

    return movie_videos


def movie_detail(request, obj_id):
    try:
        movie_detail = Movie.objects.get(movie_id=obj_id)
        # TODO: upon retrieval cache you also need movie_videos and recommendations
        
        context = {
            "movie_detail": movie_detail,
        }

    except Movie.DoesNotExist:
        # call only happens if movie not in db
        movie_from_api = media_api.get_media_data(f"/movie/{obj_id}")
        print(movie_from_api)
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

        # Get matching themes from M2M relationship
        movie_genres = get_movie_genres(movie_from_api)

        movie_detail.genres.add(*movie_genres)

        movie_videos = media_api.get_media_data(f"/movie/{obj_id}/videos")

        # TODO: you could also cache those in a related Video model

        # Get matching videos from foreign key relationship to Video model
        # movie_videos = get_movie_videos(movie_from_api)

        # movie_detail.videos.add(*movie_videos)
        # movie_detail.videos = ','.join(get_movie_videos(movie_from_api))

        # TODO: Maybe cache recommended movies as well?
        recommendations = media_api.get_media_data(f"/movie/{obj_id}/recommendations")

        context = {
            "movie_detail": movie_detail,
            "movie_videos": movie_videos,
            "recommendations": recommendations,
            "type": "movie",
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
