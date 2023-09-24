import json
import os
from functools import partial
from pprint import pprint

import pycountry
import requests
import json
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"
LANG_ENG = "en-US"


def get_data_from_endpoint(endpoint, **kwargs):
    """This function returns a JSON object of tmdb media data."""
    url = f"{BASE_URL}{endpoint}"
    params = {"api_key": settings.TMDB_API_KEY, "language": LANG_ENG}
    params.update(kwargs)

    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    return response.json()


def get_data_by_query(
    endpoint: str, text_query: str, result_key: str
) -> dict[str, int]:
    """Returns a dictionary of details based on a text query."""
    response_json = get_data_from_endpoint(endpoint, query=text_query)
    data = response_json["results"]
    return {row[result_key]: row["id"] for row in data}
