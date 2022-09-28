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


def get_movies(endpoint: str, text_query: str) -> dict[str, str]:
    """This function returns a dictionary of movie details based on a text query"""
    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "query": text_query}

    response = requests.get(url, params=params)

    movies = {row["original_title"]: row["id"] for row in response.json()["results"]}

    return movies


def get_genres(endpoint: str) -> dict[str, str]:
    """This function returns a dictionary of movie genres"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY}

    response = requests.get(url, params=params)

    genres = {row["name"]: row["id"] for row in response.json()["genres"]}

    return genres


def get_most_popular(endpoint, language, page=1):
    """This function returns a JSON object of the current most popular movies based on language"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "language": language, "page": page}
    response = requests.get(url, params=params)

    return response.json()


def get_top_rated(endpoint, region, page=1):
    """This function returns a a JSON object of the top rated movies by region"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "region": region, "page": page}
    response = requests.get(
        url,
        params=params,
    )

    return response.json()


def get_most_similar(endpoint, region):
    """This function returns a a JSON object of list of the most similar movies to movie ID based on region"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "region": region}
    response = requests.get(url, params=params)

    return response.json()


def get_recommended(endpoint, region):
    """This function returns a a JSON object of list of recommended movies to movie ID based on region"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "region": region}

    response = requests.get(url, params=params)

    return response.json()


def get_recently_released(endpoint, region, date_min, date_max):
    """This function returns a JSON object of movies based on a region within a recent date range"""

    url = f"{BASE_URL}{endpoint}"
    params = params = {
        "api_key": API_KEY,
        "region": region,
        "primary_release_date.gte": date_min,
        "primary_release_date.lte": date_max,
    }

    response = requests.get(
        url,
        params=params,
    )

    return response.json()


def get_year_genre(endpoint, region, year, genre_id):
    """This function returns a JSON object of movies based on region, primary release year, and genre"""

    url = f"{BASE_URL}{endpoint}"
    params = {
        "api_key": API_KEY,
        "region": region,
        "primary_release_year": year,
        "with_genres": genre_id,
    }

    response = requests.get(
        url,
        params=params,
    )

    return response.json()


def get_vote_sorted(endpoint, vote_count, year, sort_option, page=1):
    """This function returns a JSON object of movies greater than vote count by year, sorted by selected sort option"""

    url = f"{BASE_URL}{endpoint}"
    params = {
        "api_key": API_KEY,
        "vote_count_gte": vote_count,
        "year": year,
        "sort_by": sort_option,
        "page": page,
    }

    response = requests.get(
        url,
        params=params,
    )

    return response.json()


def main():

    # Get first page of most popular movies in English Language
    eng_lang = standardize_tag("eng_US")
    most_popular_english = get_most_popular("/movie/popular", eng_lang)
    pprint(most_popular_english)

    # Get first page of top rated movies abased on German region
    germ_region = COUNTRY_CODES.get("Germany")
    top_rated_german = get_top_rated("/movie/top_rated", germ_region)
    pprint(top_rated_german)

    # Get a dictionary of movie details based on text query
    movies = get_movies("/search/movie", "Lost in Translation")

    # Get movie id based on selected movie title
    movie_id = movies.get("Lost in Translation")

    # Get US region
    us_region = COUNTRY_CODES.get("United States")

    # Get most similar movies to movie with selected title based on US region
    most_similar = get_most_similar(f"/movie/{movie_id}/similar", us_region)
    pprint(most_similar)

    # Get recommended movies to movie ID based on US region
    recommended = get_recommended(f"/movie/{movie_id}/recommendations", us_region)
    pprint(recommended)

    # Get movies within a recent date range based on US region
    recently_released = get_recently_released(
        "/discover/movie", us_region, "2022-08-16", "2022-09-23"
    )

    pprint(recently_released)

    # Get a dictionary of available genres
    genres = get_genres("/genre/movie/list")

    # Get comedy genre ID
    com_genre_id = genres.get("Comedy")

    # Get movies released by year based on US region and comedy genre
    movie_year_genre = get_year_genre("/discover/movie", us_region, 1990, com_genre_id)

    pprint(movie_year_genre)

    # Get first page of movies with vote count greater than 2000 by year, sorted by ascending popularity
    movie_vote_popular = get_vote_sorted(
        "/discover/movie", 2000, 2008, "popularity_asc"
    )

    pprint(movie_vote_popular)


if __name__ == "__main__":
    main()
