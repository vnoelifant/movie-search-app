import requests
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint

from movie_search.models import Genre, Provider
from movie_search import media_api
from .models import Movie


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

    genre_names = request.GET.getlist("genre")
    print("GENRE NAMES: ", genre_names)

    # Get genre IDs
    with_genres = Genre.objects.filter(name__in=genre_names).values_list("tmdb_id", flat=True)
    print("WITH GENRES: ", with_genres)

    person_name = request.GET.get("personName")

    if person_name:
        person_name =  person_name.lower()
        person = media_api.get_person("/search/person", person_name)
        print("Person: ",person)

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
    with_watch_providers= Provider.objects.filter(
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
        with_people=with_people
    )

    context = {"data": data}

    return render(request, "discover.html", context)


def search(request):

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

        if type == "person":
            print("Choosing person")
            person = media_api.get_person(f"/search/{type}", query)
            person = {person.lower(): idx for person, idx in person.items()}
            print("Person Dictionary: ", person)
            # Get person id based on person query
            person_id = person.get(query)
            print("PERSON ID", person_id)

            url_path = "movie_detail" if choice == "movie_credits" else "tv_detail"

            data = media_api.get_media_data(f"/{type}/{person_id}/{choice}")

            context = {
                "data": data,
                "type": type,
                "choice": choice,
                "url_path": url_path,
            }

            return render(request, "person_search.html", context)


        else:

            # Get a dictionary of media details based on text query
            media = media_api.get_media(f"/search/{type}", query, type, year=year)

            media = {media.lower(): idx for media, idx in media.items()}

            # Get media id based on selected media title
            media_id = media.get(query)
            print("MEDIA ID", media_id)

            url_path = "movie_detail" if type == "movie" else "tv_detail"


            if choice == "general":
                print("Selected General")


                # TODO: Cache this data to increase speed
                media_detail = media_api.get_media_data(f"/{type}/{media_id}")
                # print("MEDIA DETAIL: ", media_detail)

                media_videos = media_api.get_media_data(f"/{type}/{media_id}/videos")
                recommendations = media_api.get_media_data(f"/{type}/{media_id}/recommendations")

                context = {
                    f"{type}_detail": media_detail,
                    f"{type}_videos": media_videos,
                    "type": type,
                    "url_path": url_path,
                    "recommendations": recommendations,
                }
                return render(request, f"{type}_detail.html", context)

            data = media_api.get_media_data(f"/{type}/{media_id}/{choice}")

            print("Selected Recommended/Similar")
            context = {
                "data": data,
                "type": type,
                "choice": choice,
                "url_path": url_path,
            }

        return render(request, "media_search.html", context)


"""
(Pdb) pp movie_detail
{'adult': False,
 'backdrop_path': '/8sMmAmN2x7mBiNKEX2o0aOTozEB.jpg',
 'belongs_to_collection': {'backdrop_path': '/1Jj7Frjjbewb6Q6dl6YXhL3kuvL.jpg',
                           'id': 529892,
                           'name': 'Black Panther Collection',
                           'poster_path': '/uVnN6KnfDuHiC8rsVsSc7kk0WRD.jpg'},
 'budget': 250000000,
 'genres': [{'id': 28, 'name': 'Action'},
            {'id': 12, 'name': 'Adventure'},
            {'id': 878, 'name': 'Science Fiction'}],
 'homepage': 'https://wakandaforevertickets.com',
 'id': 505642,
 'imdb_id': 'tt9114286',
 'original_language': 'en',
 'original_title': 'Black Panther: Wakanda Forever',
 'overview': 'Queen Ramonda, Shuri, M’Baku, Okoye and the Dora Milaje fight to '
             'protect their nation from intervening world powers in the wake '
             'of King T’Challa’s death. As the Wakandans strive to embrace '
             'their next chapter, the heroes must band together with the help '
             'of War Dog Nakia and Everett Ross and forge a new path for the '
             'kingdom of Wakanda.',
 'popularity': 1674.481,
 'poster_path': '/sv1xJUazXeYqALzczSZ3O6nkH75.jpg',
 'production_companies': [{'id': 420,
                           'logo_path': '/hUzeosd33nzE5MCNsZxCGEKTXaQ.png',
                           'name': 'Marvel Studios',
                           'origin_country': 'US'},
                          {'id': 176762,
                           'logo_path': None,
                           'name': 'Kevin Feige Productions',
                           'origin_country': 'US'}],
 'production_countries': [{'iso_3166_1': 'US',
                           'name': 'United States of America'}],
 'release_date': '2022-11-09',
 'revenue': 0,
 'runtime': 162,
 'spoken_languages': [{'english_name': 'English',
                       'iso_639_1': 'en',
                       'name': 'English'}],
 'status': 'Released',
 'tagline': 'Forever.',
 'title': 'Black Panther: Wakanda Forever',
 'video': False,
 'vote_average': 7.648,
 'vote_count': 172}
 """

def movie_detail(request, obj_id):
    try:
        movie_detail = Movie.objects.get(tmdb_id=obj_id)
    except Movie.DoesNotExist:
        # call only happens if movie not in db
        movie_from_api = media_api.get_media_detail(f"/movie/{obj_id}")
        genres = [
            row["name"] for row in movie_from_api["genres"]
        ]
        movie_detail = Movie.objects.create(
            tmdb_id=obj_id,
            title=movie_from_api["title"],
            genre=", ".join(genres),
            tagline=...,
            # all columns (yet to be added)
        )

    # TODO: you could also cache those in
    # a related Video model
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
