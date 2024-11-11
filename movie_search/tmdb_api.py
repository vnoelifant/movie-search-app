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
        print("Parameters: ", params)
        response = requests.get(url, params=params)

        # Attempt to parse the response as JSON
        try:
            data = response.json()
            # print("TMDb API Response:", json.dumps(data, indent=4))  # Pretty-print the response
            return data
        except JSONDecodeError:
            # Handle JSON decoding error
            print(f"Failed to parse JSON response for URL: {url}")
            print(f"HTTP Status Code: {response.status_code}")
            print("Response Text:", response.text[:500])  # Print first 500 characters of the response
            error_message = f"Failed to parse JSON response for URL: {url} - Status Code: {response.status_code} - Response: {response.text[:500]}"
            print(error_message)
            # Optionally, raise an exception or return a default value
            raise JSONDecodeError(error_message)

    def get_data_by_query(self, endpoint, text_query, primary_release_year=None):
        response_json = self.get_data_from_endpoint(endpoint, query=text_query, primary_release_year=primary_release_year)
        results = response_json.get("results", [])
        # print("Parsed Results Data:", results)  # Shows the parsed "results" data
        if results:
            # Access the first result
            first_result = results[0]
            # Extract and return the ID of the first result
            entity_id = first_result.get("id")
            return entity_id
        
        print("No results found for query.")
        return None

    
    def main():
        from utils import dump_movie_data_to_json
        obj = TMDBApi()
        data = obj.get_data_from_endpoint("/genre/movie/list")
        print("Dumping data to json file")
        dump_movie_data_to_json("genres_data_test.json", data)

    if __name__ == 'main':
        main()



