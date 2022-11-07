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


def get_media(
    endpoint: str, text_query: str, type: str, year: int = None
) -> dict[str, int]:
    """This function returns a dictionary of media details based on a text query"""
    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "query": text_query}

    if year is not None:
        params.update({"year": year})

    response = requests.get(url, params=params)

    print("Search endpoint: ", endpoint)
    data = response.json()["results"]

    title_key = "original_title" if type == "movie" else "original_name"

    media = {row[title_key]: row["id"] for row in data}

    return media

def get_person(endpoint, text_query):
    """This function returns a dictionary of person details based on a text query"""
    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": API_KEY, "query": text_query}


    response = requests.get(url, params=params)

    print("Search endpoint: ", endpoint)
    data = response.json()["results"]

    person = {row["name"]: row["id"] for row in data}

    return person


def get_media_detail(endpoint, language=LANG_ENG):

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


def get_media_data(
    endpoint,
    language=LANG_ENG,
    region=REGION_US,
    primary_release_year=None,
    with_genres=None,
    sort_by=None,
    watch_region=None,
    with_watch_providers=None,
    with_people=None,
):
    """This function returns a JSON object of tmdb media data"""
    print("Inside get_media_data functon!!!!!!!!!!!!")
    url = f"{BASE_URL}{endpoint}"

    print("URL: ", url)

    params = {"api_key": API_KEY, "language": language, "region": region}

    if with_genres is not None:
        params.update({"with_genres": with_genres})

    if sort_by is not None:
        params.update({"sort_by": sort_by})

    if watch_region is not None:
        params.update({"watch_region": watch_region})

    if with_watch_providers is not None:
        params.update({"with_watch_providers": with_watch_providers})

    if primary_release_year is not None:
        params.update({"primary_release_year": primary_release_year})

    if with_people is not None:
        params.update({"with_people": with_people})

    print("Params: ", params)

    response = requests.get(url, params=params)

    return response.json()













#
