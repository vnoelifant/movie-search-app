from abc import ABC, abstractmethod
from .models import (
    Movie,
    MovieVideo,
    MovieGenre,
    MovieProvider,
    MovieRecommendation,
    MovieProductionCompany,
    TVSeries,
    TVSeriesVideo,
    TVSeriesGenre,
    TVSeriesProvider,
    TVSeriesRecommendation,
    TVSeriesProductionCompany,
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
    
    def fetch_media_details_from_api(self, media_type, tmdb_id):
        media_data = tmdb_api_obj.get_data_from_endpoint(f"/{media_type}/{tmdb_id}")
        videos_data = tmdb_api_obj.get_data_from_endpoint(f"/{media_type}/{tmdb_id}/videos")
        return media_data, videos_data

    def store_genres(self, genres_data, GenreModel):
        genres = []
        for genre_data in genres_data:
            genre, created = GenreModel.objects.get_or_create(
                name=genre_data.get("name", ""),
                genre_id=genre_data.get("id", 0),
            )
            genres.append(genre)
        return genres

    def store_production_companies(
        self, production_companies_data, ProductionCompanyModel
    ):
        production_companies = []
        for production_company_data in production_companies_data:
            production_company, created = ProductionCompanyModel.objects.get_or_create(
                name=production_company_data.get("name", ""),
                genre_id=production_company_data.get("id", 0),
            )
            production_companies.append(production_company)
        return production_companies


    def store_recommendations(self, media_type, tmdb_id, RecommendationModel):
        recommendations_data = tmdb_api_obj.get_data_from_endpoint(
            f"{media_type}{tmdb_id}/recommendations"
        )
        recommendations = []
        for rec_data in recommendations_data.get("results", []):
            recommendation, created = RecommendationModel.objects.get_or_create(
                tmdb_id=rec_data.get("id", 0),
                poster_path=rec_data.get("poster_path", ""),
            )
            recommendations.append(recommendation)
        return recommendations

    def get_genres_from_discover(self, genre_names, GenreModel):
        genres = GenreModel.objects.filter(name__in=genre_names).values_list(
            "genre_id", flat=True
        )
        return genres

    def get_providers_from_discover(self, watch_provider_names, ProviderModel):
        providers = ProviderModel.objects.filter(
            name__in=watch_provider_names
        ).values_list("provider_id", flat=True)
        return providers

    def get_discover_data(self, endpoint, **kwargs):
        return tmdb_api_obj.get_data_from_endpoint(endpoint, **kwargs)

    @abstractmethod
    def store_data(self, data):
        pass

    @abstractmethod
    def store_videos(self, data):
        pass

class MovieService(MediaService):
    def fetch_movie_data_from_api(self, tmdb_id):
        movie_data, videos_data = self.fetch_media_details_from_api("movie", tmdb_id)
        return movie_data, videos_data

    def store_data(self, data):
        movie_data, videos_data = data
        genres = movie_data.get("genres")
        production_companies = movie_data.get("production_companies")
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
            overview=movie_data.get("overview", ""),
            budget=movie_data.get("budget", 0),
            revenue=movie_data.get("revenue", 0),
            homepage=movie_data.get("homepage", ""),
        )
        if genres is not None:
            movie_genres = self.store_genres(genres, MovieGenre)

        movie.genres.add(*movie_genres)

        if production_companies is not None:
            movie_production_companies = self.store_production_companies(
                production_companies, MovieProductionCompany
            )

        movie.production_companies.add(*movie_production_companies)

        movie_recommendations = self.store_recommendations("movie",
            movie.tmdb_id,
            MovieRecommendation,
        )
        movie.recommendation.add(*movie_recommendations)

        videos = self.store_videos(movie, videos_data)

        return movie, videos
    
    def store_videos(self, movie_obj, videos_data):
        for video_data in videos_data.get("results", []):
            MovieVideo.objects.get_or_create(
                movie=movie_obj,
                name=video_data.get("name", ""),
                key=video_data.get("key", ""),
            )
        return MovieVideo.objects.filter(movie_id=movie_obj.id)

    def get_movie_discover_data(self, **kwargs):
        # Process genres
        genre_names = kwargs.get("genre_names", [])
        genres = self.get_genres_from_discover(genre_names, MovieGenre)

        # Process person
        person_name = kwargs.get("person_name")
        person_id = None
        if person_name:
            person_service = PersonService()
            person_data = person_service.fetch_person_data(person_name)
            person_id = person_service.get_person_id(person_data, person_name)

        # Process providers
        watch_provider_names = kwargs.get("watch_provider_names", [])
        providers = self.get_providers_from_discover(
            watch_provider_names, MovieProvider
        )

        # Update kwargs with processed data
        kwargs.update(
            {
                "with_genres": ",".join(map(str, genres)),
                "with_watch_providers": ",".join(map(str, providers)),
                "with_people": person_id,
            }
        )

        # Remove None values from kwargs
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        return self.get_discover_data("/discover/movie", **kwargs)


class TVSeriesService(MediaService):
    def fetch_tv_data_from_api(self, tmdb_id):
        tv_data, videos_data = self.fetch_media_details_from_api("tvseries", tmdb_id)
        return tv_data, videos_data

    def store_data(self, data):
        tv_data, videos_data = data
        genres = tv_data.get("genres")
        production_companies = tv_data.get("production_companies")
        tvseries, created = TVSeries.objects.get_or_create(
            tmdb_id=tv_data.get("id", 0),
            name=tv_data.get("name", ""),
            backdrop_path=tv_data.get("backdrop_path", ""),
            tagline=tv_data.get("tagline", ""),
            vote_count=tv_data.get("vote_count", 0),
            vote_average=tv_data.get("vote_average", 0),
            popularity=tv_data.get("popularity", 0),
            first_air_date=tv_data.get("first_air_date", ""),
            number_of_episodes=tv_data.get("number_of_episodes", 0),
            number_of_seasons=tv_data.get("number_of_seasons", 0),
            overview=tv_data.get("overview", ""),
            homepage=tv_data.get("homepage", ""),
        )
        if genres is not None:
            tv_genres = self.store_genres(genres, TVSeriesGenre)

        tvseries.genres.add(*tv_genres)

        if production_companies is not None:
            tv_production_companies = self.store_production_companies(production_companies, TVSeriesProductionCompany)

        tvseries.production_companies.add(*tv_production_companies)

        tv_recommendations = self.store_recommendations("tvseries",
            tvseries.tmdb_id,
            TVSeriesRecommendation,
        )
        tvseries.recommendation.add(*tv_recommendations)

        videos = self.store_videos(tvseries, videos_data)

        return tvseries, videos
    
    def store_videos(self, tv_obj, videos_data):
        for video_data in videos_data.get("results", []):
            TVSeriesVideo.objects.get_or_create(
                tvseries=tv_obj,
                name=video_data.get("name", ""),
                key=video_data.get("key", ""),
            )
        return TVSeriesVideo.objects.filter(tvseries_id=tv_obj.id)


class PersonService:
    def fetch_person_data(self, person_name):
        return fetch_api_data_by_query("/search/person", person_name, "name")

    def get_person_id(self, person_data, person_name):
        return lookup_id_in_data_by_query(person_data, person_name)
