from movie_search import media_api
from .models import Movie, Video, Genre, Provider, Recommendation

def get_movie_id_from_query(movie, query):
    return {m.lower(): idx for m, idx in movie.items()}.get(query)

def get_person_id_from_name(person, query):
    return {p.lower(): idx for p, idx in person.items()}.get(query)

def get_movie_detail(movie_id):
    try:
        movie_detail = Movie.objects.get(movie_id=movie_id)
        movie_videos = Video.objects.filter(movie_id=movie_detail.id)
    except Movie.DoesNotExist:
        movie_from_api = media_api.get_data_from_endpoint(f"/movie/{movie_id}")
        genres = movie_from_api.get("genres")

        movie_detail, created = Movie.objects.get_or_create(
            movie_id=movie_id,
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
            movie_genres = get_movie_genres(genres)
            movie_detail.genres.add(*movie_genres)

        movie_videos = get_movie_videos(movie_detail)

        movie_recs = get_movie_recs(movie_id)
        movie_detail.recommendation.add(*movie_recs)

    context = {
        "movie_detail": movie_detail,
        "movie_videos": movie_videos,
    }

    return context

def get_movie_genres(genres):
    movie_genres = []

    for row in genres:
        genre, inserted = Genre.objects.get_or_create(
            name=row.get("name", ""),
            genre_id=row.get("id", 0),
        )
        movie_genres.append(genre)

    return movie_genres


def get_movie_videos(movie_obj):
    videos = media_api.get_data_from_endpoint(f"/movie/{movie_obj.movie_id}/videos")

    video_response = videos.get("results")

    for row in video_response:
        video, inserted = Video.objects.get_or_create(
            movie=movie_obj,
            name=row.get("name", ""),
            key=row.get("key", ""),
        )
    movie_videos = Video.objects.filter(movie_id=movie_obj.id)
    return movie_videos


def get_movie_recs(movie_id):
    recs = media_api.get_data_from_endpoint(f"/movie/{movie_id}/recommendations")
    movie_recs = []

    recs_response = recs.get("results")

    for row in recs_response:
        rec, inserted = Recommendation.objects.get_or_create(
            movie_id=row.get("id", 0),
            poster_path=row.get("poster_path", ""),
        )

        movie_recs.append(rec)

    return movie_recs

def get_genres_from_discover(genre_names):
    genres =  Genre.objects.filter(name__in=genre_names).values_list(
        "genre_id", flat=True
    )
    return genres

def get_providers_from_discover(watch_provider_names):
    providers = Provider.objects.filter(name__in=watch_provider_names).values_list(
        "provider_id", flat=True
    )
    return providers

def get_movie_discover_data(
     genres, person_id, sort_options, region, watch_region, providers, year
):
    return media_api.get_data_from_endpoint(
        "/discover/movie",
        region=region,
        primary_release_year=year,
        with_genres=list(genres),
        sort_by=sort_options,
        watch_region=watch_region,
        with_watch_providers=list(providers),
        with_people=person_id,
    )
