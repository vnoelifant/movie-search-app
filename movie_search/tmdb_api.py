import json
import os
from functools import partial
from pprint import pprint

import pycountry
import requests
import json
from django.conf import settings
from requests.exceptions import JSONDecodeError


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

            # Attempt to parse the response as JSON
            try:
                return response.json()
            except JSONDecodeError:
                # Handle JSON decoding error
                print(f"Failed to parse JSON response for URL: {url}")
                print(f"HTTP Status Code: {response.status_code}")
                print("Response Text:", response.text[:500])  # Print first 500 characters of the response
                # Optionally, raise an exception or return a default value
                raise JSONDecodeError("Invalid JSON response received from the API")

    def get_data_by_query(self, endpoint, text_query, result_key):
        response_json = self.get_data_from_endpoint(endpoint, query=text_query)
        data = response_json["results"]
        return {row[result_key]: row["id"] for row in data}
    

    def main():
        from utils import dump_movie_data_to_json
        obj = TMDBApi()
        data = obj.get_data_from_endpoint("/genre/movie/list")
        print("Dumping data to json file")
        dump_movie_data_to_json("genres_data_test.json", data)

    if __name__ == 'main':
        main()



