from abc import ABC, abstractmethod
from .models import (
    Movie,
    MovieVideo,
    MovieGenre,
    MovieProvider,
    MovieRecommendation,
    TVSeries,
    TVSeriesVideo,
    TVSeriesGenre,
    TVSeriesProvider,
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


class MovieService(MediaService):
    def fetch_from_api(self, tmdb_id):
        movie_data = tmdb_api_obj.get_data_from_endpoint(f"/movie/{tmdb_id}")
        video_data = tmdb_api_obj.get_data_from_endpoint(f"/movie/{tmdb_id}/videos")
        return movie_data, video_data

    def store_data(self, data):
        movie_data, video_data = data
        # Store movie data
        genres = movie_data.get("genres")
        movie, created = Movie.objects.get_or_create(
            tmdb_id=movie_data.get("id", 0),
            title=movie_data.get("title", ""),
            backdrop_path=movie_data.get("backdrop_path", ""),
            tagline=movie_data.get("tagline", ""),
            vote_count=movie_data.get("vote_count", 0),
            vote_average=movie_data.get("vote_average", 0),
            popularity=movie_data.get("popularity", 0),
            release_date=movie_data.get("release_date", ""),
            runtime=movie_data.get("runtime", 0),
            production_company=movie_data.get("production_company", ""),
            overview=movie_data.get("overview", ""),
            budget=movie_data.get("budget", 0),
            revenue=movie_data.get("revenue", 0),
            homepage=movie_data.get("homepage", ""),
        )
        if genres is not None:
            movie_genres = self.store_genres(genres)

        movie.genres.add(*movie_genres)

        movie_recommendations = self.store_recommendations(movie.tmdb_id)
        movie.recommendation.add(*movie_recommendations)

        videos = self.store_videos(movie, video_data)

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

    def store_videos(self, movie_obj, video_data):
        for video in video_data.get("results", []):
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


class TVSeriesService(MediaService):
    def fetch_from_api(self, tmdb_id):
        movie_data = tmdb_api_obj.get_data_from_endpoint(f"/tv/{tmdb_id}")
        video_data = tmdb_api_obj.get_data_from_endpoint(f"/tv/{tmdb_id}/videos")

    def store_data(self, data):
        tv_data, video_data = data
        # Store TV series data
        genres = data.get("genres")
        tv, created = TVSeries.objects.get_or_create(
            tmdb_api_obj_id=tv_data.get("id", 0),
            name=tv_data.get("name", ""),
            backdrop_path=tv_data.get("backdrop_path", ""),
            tagline=tv_data.get("tagline", ""),
            vote_count=tv_data.get("vote_count", 0),
            vote_average=tv_data.get("vote_average", 0),
            popularity=tv_data.get("popularity", 0),
            first_air_date=tv_data.get("first_air_date", ""),
            number_of_episodes=tv_data.get("number_of_episodes", 0),
            number_of_seasons=tv_data.get("number_of_seasons", 0),
            production_company=tv_data.get("production_company", ""),
            overview=tv_data.get("overview", ""),
            homepage=tv_data.get("homepage", ""),
        )
        if genres is not None:
            tv_genres = self.store_genres(genres)

        tv.genres.add(*tv_genres)

        tv_recommendations = self.store_recommendations(tv.tmdb_id)
        tv.recommendation.add(*tv_recommendations)

        videos = self.store_videos(tv, video_data)

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

    def store_videos(self, tv_obj, video_data):
        for video in video_data.get("results", []):
            TVSeriesVideo.objects.get_or_create(
                tv=tv_obj,
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
            tv_recommendations.append(recommendation)
        return tv_recommendations

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

class PersonService:
    def fetch_person_data(self, person_name):
        return fetch_api_data_by_query("/search/person", person_name, "name")

    def get_person_id(self, person_data, person_name):
        return lookup_id_in_data_by_query(person_data, person_name)