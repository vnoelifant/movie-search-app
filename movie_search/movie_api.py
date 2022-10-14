import os
import json
from pprint import pprint
from functools import partial

import requests
import pycountry
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROJECT_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
COUNTRY_CODES = {country.name: country.alpha_2 for country in pycountry.countries}
LANG_ENG = "en-US"
REGION_US = COUNTRY_CODES.get("United States")


def get_media(endpoint: str, text_query: str, year: int = None) -> dict[str, int]:
    """This function returns a dictionary of movie details based on a text query"""
    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "query": text_query}

    if year is not None:
        params.update({"year": year})

    response = requests.get(url, params=params)

    print("Endpoint: ", endpoint)
    data = response.json()["results"]

    title_key = "original_title" if "movie" in endpoint else "original_name"

    media = {row[title_key]: row["id"] for row in data}

    return media


def get_movie_detail(endpoint, language=LANG_ENG):

    url = f"{BASE_URL}{endpoint}"

    params = {
        "api_key": API_KEY,
        "language": language,
    }

    response = requests.get(url, params=params)

    return response.json()


def get_movie_videos(endpoint, language=LANG_ENG):

    url = f"{BASE_URL}{endpoint}"

    params = {
        "api_key": API_KEY,
        "language": language,
    }

    response = requests.get(url, params=params)

    return response.json()


def get_genres(endpoint: str) -> dict[str, int]:
    """This function returns a dictionary of movie genres"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY}

    response = requests.get(url, params=params)

    genres = {row["name"]: row["id"] for row in response.json()["genres"]}

    return genres


def get_most_popular(endpoint, language=LANG_ENG, page=1):
    """This function returns a JSON object of the current most popular movies based on language"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "language": language, "page": page}
    response = requests.get(url, params=params)

    return response.json()


def get_top_rated(endpoint, region=REGION_US, page=1):
    """This function returns a a JSON object of the top rated movies by region"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "region": region, "page": page}
    response = requests.get(
        url,
        params=params,
    )

    return response.json()


def get_most_similar(endpoint, region=REGION_US):
    """This function returns a a JSON object of list of the most similar movies to movie ID based on region"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "region": region}
    response = requests.get(url, params=params)

    return response.json()


def get_media_data(endpoint, region=REGION_US):
    """This function returns a a JSON object of list of the most similar movies to movie ID based on region"""

    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "region": region}
    response = requests.get(url, params=params)

    return response.json()


def get_recently_released(
    endpoint,
    date_min,
    date_max,
    region=REGION_US,
):
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


def get_year_genre(endpoint, year, genre_id, region=REGION_US):
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
