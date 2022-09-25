import os
import json
from pprint import pprint
from functools import partial

import requests
import pycountry
from dotenv import load_dotenv
from langcodes import standardize_tag

load_dotenv()

API_KEY = os.getenv("PROJECT_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
COUNTRY_CODES = {country.name: country.alpha_2 for country in pycountry.countries}


def get_movie_dict(search_key, text_query):

    response = requests.get(
        f"{BASE_URL}{search_key}", params={"api_key": API_KEY, "query": text_query}
    )

    return response.json()


def get_movie_id(movie_dict, movie_name):
    for movie in movie_dict["results"]:
        if movie["original_title"] == movie_name:
            return movie["id"]


def get_genre_dict(search_key):

    response = requests.get(f"{BASE_URL}{search_key}", params={"api_key": API_KEY})

    return response.json()


def get_genre_id(genre_dict, genre_name):
    for genre in genre_dict["genres"]:
        if genre["name"] == genre_name:
            return genre["id"]


def get_most_popular(search_key, language):
    """This function returns a JSON object of list of the current most popular movies"""

    response = requests.get(
        f"{BASE_URL}{search_key}", params={"api_key": API_KEY, "language": language}
    )

    return response.json()


def get_top_rated(search_key, region, page):
    """This function returns a a JSON object of list of the top rated movies"""
    response = requests.get(
        f"{BASE_URL}{search_key}",
        params={"api_key": API_KEY, "page": page, "region": region},
    )

    return response.json()


def get_most_similar(search_key):
    """This function returns a a JSON object of list of the most similar movies to movie ID"""
    response = requests.get(f"{BASE_URL}{search_key}", params={"api_key": API_KEY})

    return response.json()


def get_recommended(search_key):
    """This function returns a a JSON object of list of recommended movies to movie ID"""
    response = requests.get(f"{BASE_URL}{search_key}", params={"api_key": API_KEY})

    return response.json()


def get_recently_released(search_key, date_min, date_max):

    response = requests.get(
        f"{BASE_URL}{search_key}",
        params={
            "api_key": API_KEY,
            "release_date.gte": date_min,
            "release_date.lte": date_max,
        },
    )

    return response.json()


def get_year_genre(search_key, year, genre_id):
    response = requests.get(
        f"{BASE_URL}{search_key}",
        params={
            "api_key": API_KEY,
            "primary_release_year": year,
            "with_genres": genre_id,
        },
    )


def main():
    # Get most popular movies in English Language
    most_popular_english = get_most_popular("/movie/popular", standardize_tag("eng_US"))
    # pprint(most_popular_english)

    # Get first page of top rated movies abased on German region
    top_rated_german = get_top_rated("/movie/top_rated", COUNTRY_CODES["Germany"], 1)
    # pprint(top_rated_german)

    # Get most similar movies to movie with selected title
    # Search for movies with text query
    movie_dict = get_movie_dict("/search/movie", "Lost in Translation")

    # Match the original movie title with movie ID
    movie_id = get_movie_id(movie_dict, "Lost in Translation")
    most_similar = get_most_similar(f"/movie/{movie_id}/similar")
    # pprint(most_similar)

    # Get recommended movies to movie ID
    recommended = get_recommended(f"/movie/{movie_id}/recommendations")
    # pprint(recommended)

    # Get movies within a recent date range

    recently_released = get_recently_released(
        "/discover/movie", "2022-08-16", "2022-09-23"
    )

    # pprint(recently_released)

    # Get movies of from primary release year based on genre
    genre_dict = get_genre_dict("/genre/movie/list")
    genre_id = get_genre_id(genre_dict, "Comedy")

    movie_year_genre = get_year_genre("/discover/movie", 1990, genre_id)
    pprint(movie_year_genre)


if __name__ == "__main__":
    main()
