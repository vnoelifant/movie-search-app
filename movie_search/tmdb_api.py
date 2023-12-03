import json
import os
from functools import partial
from pprint import pprint

import pycountry
import requests
import json
from django.conf import settings


class TMDBApi:

    def __init__(self, language = None):
        self.base_url = settings.TMDB_API_URL
        self.api_key = settings.TMDB_API_KEY
        self.language = language or settings.TMDB_API_LANG

    def get_data_from_endpoint(self, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        params = {"api_key": self.api_key, "language": self.language}
        params.update(kwargs)
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_data_by_query(self, endpoint, text_query, result_key):
        response_json = self.get_data_from_endpoint(endpoint, query=text_query)
        data = response_json["results"]
        return {row[result_key]: row["id"] for row in data}


