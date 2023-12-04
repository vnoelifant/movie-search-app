from abc import ABC, abstractmethod
from .models import (
    Movie,
    MovieVideo,
    MovieGenre,
    MovieProvider,
    MovieRecommendation,
    TVSeries,
    TVSeriesGenre,
    TVSeriesProvuder,
    TVSeriesRecommendation,
)
from .tmdb_api import TMDBApi

tmdb_api_obj = TMDBApi()


# standalone functions for general fetching of data
def fetch_data_from_api(endpoint, **kwargs):
    """A common method to fetch data from media API"""
    return tmdb_api_obj.get_data_from_endpoint(endpoint, **kwargs)


def fetch_api_data_by_query(endpoint, text_query, results_key):
    """A common method to fetch data by query from media API"""
    return tmdb_api_obj.get_data_by_query(endpoint, text_query, results_key)


def lookup_id_in_data_by_query(data_dict, query):
    """A common method to fetch media ID from data by query"""
    return {item.lower(): idx for item, idx in data_dict.items()}.get(query)


class MediaService(ABC):
    @abstractmethod
    def fetch_from_api(self, tmdb_id):
        pass

    @abstractmethod
    def store_data(self, data):
        pass

    @abstractmethod
    def get_discover_data(self, **kwargs):
        pass


# Context class to utilize the strategies
class MediaContext:
    def __init__(self, service: MediaService):
        self._service = service

    def process_media(self, tmdb_id):
        data = self._service.fetch_from_api(tmdb_id)
        return self._service.store_data(data)


class MovieStrategy(MediaService):
    def fetch_from_api(self, tmdb_id):
        return tmdb_api_obj.get_data_from_endpoint(f"/movie/{tmdb_id}")

    def store_data(self, data):
        # Store movie data
        genres = data.get("genres")
        movie, created = Movie.objects.get_or_create(
            tmdb_id=data.get("id", 0),
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
            movie_genres = self.store_genres(genres)

        movie.genres.add(*movie_genres)

        movie_recommendations = self.store_recommendations(movie.tmdb_id)
        movie.recommendation.add(*movie_recommendations)

        videos = self.store_videos(movie)

        return movie, videos

    def store_genres(self, genres):
        movie_genres = []
        for row in genres:
            genre, created = MovieGenre.objects.get_or_create(
                name=row.get("name", ""),
                genre_id=row.get("id", 0),
            )
            movie_genres.append(genre)

        return movie_genres

    def store_videos(self, movie_obj):
        video_data = tmdb_api_obj.get_data_from_endpoint(
            f"/movie/{movie_obj.tmdb_id}/videos"
        )
        for video_data in video_data.get("results", []):
            MovieVideo.objects.get_or_create(
                movie=movie_obj,
                name=video_data.get("name", ""),
                key=video_data.get("key", ""),
            )
        return MovieVideo.objects.filter(movie_id=movie_obj.id)

    def store_recommendations(self, tmdb_id):
        recommendations_data = tmdb_api_obj.get_data_from_endpoint(
            f"/movie/{tmdb_id}/recommendations"
        )
        movie_recommendations = []

        for rec_data in recommendations_data.get("results", []):
            recommendation, created = MovieRecommendation.objects.get_or_create(
                tmdb_id=rec_data.get("id", 0),
                poster_path=rec_data.get("poster_path", ""),
            )
            movie_recommendations.append(recommendation)
        return movie_recommendations

    def get_genres_from_discover(self, genre_names):
        genres = MovieGenre.objects.filter(name__in=genre_names).values_list(
            "genre_id", flat=True
        )
        return genres

    def get_providers_from_discover(self, watch_provider_names):
        providers = MovieProvider.objects.filter(
            name__in=watch_provider_names
        ).values_list("provider_id", flat=True)
        return providers

    def get_discover_data(
        self, genres, person_id, sort_options, region, watch_region, providers, year
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


class TVSeriesStrategy(MediaService):
    def fetch_from_api(self, tmdb_id):
        return tmdb_api_obj.get_data_from_endpoint(f"/tv/{tmdb_id}")

    def store_data(self, data):
        # Store TV series data
        pass  # Implementation similar to the previous TVSeries class

    def store_data(data):
        genres = data.get("genres")
        tv, created = TVSeries.objects.get_or_create(
            tmdb_api_obj_id=data.get("id", 0),
            name=data.get("name", ""),
            backdrop_path=data.get("backdrop_path", ""),
            tagline=data.get("tagline", ""),
            vote_count=data.get("vote_count", 0),
            vote_average=data.get("vote_average", 0),
            popularity=data.get("popularity", 0),
            first_air_date=data.get("first_air_date", ""),
            number_of_episodes=data.get("number_of_episodes", 0),
            number_of_seasons=data.get("number_of_seasons", 0),
            production_company=data.get("production_company", ""),
            overview=data.get("overview", ""),
            homepage=data.get("homepage", ""),
        )
        if genres is not None:
            tv_genres = store_genres(genres)

        tv.genres.add(*tv_genres)

        tv_recommendations = store_recommendations(tv.tmdb_id)
        tv.recommendation.add(*tv_recommendations)

        videos = self.store_videos(tc)

        return tv, videos

    def store_genres(self, genres):
        tv_genres = []

        for row in genres:
            genre, created = TVSeriesGenre.objects.get_or_create(
                name=row.get("name", ""),
                genre_id=row.get("id", 0),
            )
            tv_genres.append(genre)

        return tv_genres

    def store_videos(self, tv_obj):
        video_data = tmdb_api_obj.get_data_from_endpoint(f"/tv/{tv_obj.tmdb_id}/videos")
        for video_data in video_data.get("results", []):
            TVSeriesVideo.objects.get_or_create(
                tv=movie_obj,
                name=video_data.get("name", ""),
                key=video_data.get("key", ""),
            )
        return TVSeriesVideo.objects.filter(tv_id=tv_obj.id)

    def store_recommendations(self, tmdb_id):
        recommendations_data = tmdb_api_obj.get_data_from_endpoint(
            f"/tv/{tmdb_id}/recommendations"
        )
        tv_recommendations = []

        for rec_data in recommendations_data.get("results", []):
            recommendation, created = TVSeriesRecommendation.objects.get_or_create(
                tmdb_id=rec_data.get("id", 0),
                poster_path=rec_data.get("poster_path", ""),
            )
            movie_recommendations.append(recommendation)
        return movie_recommendations

    def get_genres_from_discover(self, genre_names):
        genres = TVSeriesGenre.objects.filter(name__in=genre_names).values_list(
            "genre_id", flat=True
        )
        return genres

    def get_providers_from_discover(self, watch_provider_names):
        providers = TVSeriesProvider.objects.filter(
            name__in=watch_provider_names
        ).values_list("provider_id", flat=True)
        return providers

    def get_discover_data(
        self,
        language,
        year,
        genres,
        sort_options,
        providers,
    ):
        return tmdb_api_obj.get_data_from_endpoint(
            "/discover/movie",
            language=language,
            first_air_date_year=year,
            with_genres=list(genres),
            sort_by=sort_options,
            with_watch_providers=list(providers),
        )
