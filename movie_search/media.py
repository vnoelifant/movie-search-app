from movie_search import tmdb_api
from .models import Movie, MovieVideo, MovieGenre, MovieProvider, MovieRecommendation

tmdb_api_obj = tmdb_api.TMDBApi()

def fetch_data_from_api(endpoint, **kwargs):
    """A common method to fetch data from media API"""
    return tmdb_api_obj.get_data_from_endpoint(endpoint, **kwargs)

def fetch_api_data_by_query(endpoint, text_query, results_key):
    """A common method to fetch data by query from media API"""
    return tmdb_api_obj.get_data_by_query(endpoint, text_query, results_key)

def lookup_id_in_data_by_query(data_dict, query):
    """A common method to fetch media ID from data by query"""
    return {item.lower(): idx for item, idx in data_dict.items()}.get(query)


def fetch_and_store_movie_from_api(movie_id):
    movie_data = tmdb_api_obj.get_data_from_endpoint(f"/movie/{movie_id}")
    movie = store_movie_data(movie_data)
    videos = store_movie_videos(movie)
    return movie, videos

def store_movie_data(data):
    genres = data.get("genres")
    movie, created = Movie.objects.get_or_create(
        movie_id=data.get("id", 0),
        title=data.get("title", ""),
        backdrop_path=data.get("backdrop_path", ""),
        tagline=data.get("tagline", ""),
        vote_count=data.get("vote_count", 0),
        vote_average=data.get("vote_average", 0),
        popularity=data.get("popularity", 0),
        release_date=data.get("release_date", ""),
        runtime=data.get("runtime", 0),
        production_company=data.get("production_company", ""),
        overview=data.get("overview", ""),
        budget=data.get("budget", 0),
        revenue=data.get("revenue", 0),
        homepage=data.get("homepage", ""),
    )
    if genres is not None:
        movie_genres = store_movie_genres(genres)
    
    movie.genres.add(*movie_genres)
    
    movie_recommendations = store_movie_recommendations(movie.movie_id)
    movie.recommendation.add(*movie_recommendations)
    
    return movie 


def store_movie_genres(genres):
    movie_genres = []

    for row in genres:
        genre, created = MovieGenre.objects.get_or_create(
            name=row.get("name", ""),
            genre_id=row.get("id", 0),
        )
        movie_genres.append(genre)

    return movie_genres


def store_movie_videos(movie_obj):
    video_data = tmdb_api_obj.get_data_from_endpoint(f"/movie/{movie_obj.movie_id}/videos")
    for video_data in video_data.get("results", []):
        MovieVideo.objects.get_or_create(
            movie=movie_obj,
            name=video_data.get("name", ""),
            key=video_data.get("key", ""),
        )
    return MovieVideo.objects.filter(movie_id=movie_obj.id)
    
def store_movie_recommendations(movie_id):
    recommendations_data = tmdb_api_obj.get_data_from_endpoint(f"/movie/{movie_id}/recommendations")
    movie_recommendations = []

    for rec_data in recommendations_data.get("results",[]):
        recommendation, created = MovieRecommendation.objects.get_or_create(
            movie_id=rec_data.get("id", 0),
            poster_path=rec_data.get("poster_path", ""),
        )
        movie_recommendations.append(recommendation)
    return movie_recommendations

def get_genres_from_discover(genre_names):
    genres =  MovieGenre.objects.filter(name__in=genre_names).values_list(
        "genre_id", flat=True
    )
    return genres

def get_providers_from_discover(watch_provider_names):
    providers = MovieProvider.objects.filter(name__in=watch_provider_names).values_list(
        "provider_id", flat=True
    )
    return providers

def get_movie_discover_data(
     genres, person_id, sort_options, region, watch_region, providers, year
):
    return tmdb_api_obj.get_data_from_endpoint(
        "/discover/movie",
        region=region,
        primary_release_year=year,
        with_genres=list(genres),
        sort_by=sort_options,
        watch_region=watch_region,
        with_watch_providers=list(providers),
        with_people=person_id,
    )
