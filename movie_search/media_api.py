import json
import os
from functools import partial
from pprint import pprint

import pycountry
import requests
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"
LANG_ENG = "en-US"

def get_data_from_endpoint(endpoint, **kwargs):
    """This function returns a JSON object of tmdb media data"""
    url = f"{BASE_URL}{endpoint}"

    params = {"api_key": settings.TMDB_API_KEY, "language": LANG_ENG}
    params.update(kwargs)

    response = requests.get(url, params=params)
    return response.json()

def get_movie(endpoint: str, text_query: str) -> dict[str, int]:
    """"Returns a dictionary of media details based on a text query"""
    response_json = get_data_from_endpoint(endpoint, query=text_query)
    data = response_json["results"]
    return {row["original_title"]: row["id"] for row in data}

def get_person(endpoint, text_query):
    """Returns a dictionary of person details based on a text query"""
    response_json = get_data_from_endpoint(endpoint, query=text_query)
    data = response_json["results"]
    return {row["name"]: row["id"] for row in data}

