import os
import json
from pprint import pprint

import requests
import pycountry
from dotenv import load_dotenv
from langcodes import standardize_tag

load_dotenv()

API_KEY = os.getenv("PROJECT_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
COUNTRY_CODES = {country.name: country.alpha_2 for country in pycountry.countries}


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


def main():
    # Get most popular movies in English Language
    most_popular_english = get_most_popular("/movie/popular", standardize_tag("eng_US"))
    pprint(most_popular_english)

    # Get first page of top rated movies abased on German region
    top_rated_german = get_top_rated("/movie/top_rated", COUNTRY_CODES["Germany"], 1)
    pprint(top_rated_german)

    # Get most similar movies to movie ID
    movie_id = 153
    most_similar = get_most_similar(f"/movie/{movie_id}/similar")
    pprint(most_similar)

    # Get recommended movies to movie ID
    recommended = get_recommended(f"/movie/{movie_id}/similar")
    pprint(recommended)


if __name__ == "__main__":
    main()
