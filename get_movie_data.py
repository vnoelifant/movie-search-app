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


def get_movies(endpoint, text_query):
    """This function returns a dictionary of movie details based on a text query"""
    params = {"api_key": API_KEY, "query": text_query}
    response = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return response.json()


def get_movie_id(movie_dict, movie_name):
    """This function returns the movie ID for a specific movie title"""
    for movie in movie_dict["results"]:
        if movie["original_title"] == movie_name:
            return movie["id"]


def get_genres(endpoint) -> dict[str, int]:
    """This function returns a dictionary of movie genres"""
    response = requests.get(f"{BASE_URL}{endpoint}", params={"api_key": API_KEY})
    # return response.json()
    ret = {row["name"]: row["id"] for row in response.json()["genres"]}
    return ret


def get_genre_id(genre_dict, genre_name):
    """This function returns the genre ID in list form for a specific genre name"""
    for genre in genre_dict["genres"]:
        if genre["name"] == genre_name:
            return genre["id"]


def get_most_popular(endpoint, language, page):
    """This function returns a JSON object of the current most popular movies based on language"""

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        params={"api_key": API_KEY, "language": language, "page": page},
    )

    return response.json()


def get_top_rated(endpoint, region, page):
    """This function returns a a JSON object of the first page of the top rated movies by region"""
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        params={"api_key": API_KEY, "region": region, "page": page},
    )

    return response.json()


def get_most_similar(endpoint, region):
    """This function returns a a JSON object of list of the most similar movies to movie ID based on region"""
    response = requests.get(
        f"{BASE_URL}{endpoint}", params={"api_key": API_KEY, "region": region}
    )

    return response.json()


def get_recommended(endpoint, region):
    """This function returns a a JSON object of list of recommended movies to movie ID based on region"""
    response = requests.get(
        f"{BASE_URL}{endpoint}", params={"api_key": API_KEY, "region": region}
    )

    return response.json()


def get_recently_released(endpoint, region, date_min, date_max):
    """This function returns a JSON object of movies based on a region within a recent date range"""
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        params={
            "api_key": API_KEY,
            "region": region,
            "primary_release_date.gte": date_min,
            "primary_release_date.lte": date_max,
        },
    )

    return response.json()


def get_year_genre(endpoint, region, year, genre_id):
    """This function returns a JSON object of movies based on region, primary release year, and genre"""
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        params={
            "api_key": API_KEY,
            "region": region,
            "primary_release_year": year,
            "with_genres": genre_id,
        },
    )
    return response.json()


def get_vote_popular(endpoint, year, vote_count, page):
    """This function returns a JSON object of movies greater than vote count, sorted by popularity"""
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        params={
            "api_key": API_KEY,
            "primary_release_year": year,
            "vote_count_gte": vote_count,
            "page": page,
        },
    )
    return response.json()


def main():
    # Get most popular movies in English Language
    most_popular_english = get_most_popular(
        "/movie/popular", standardize_tag("eng_US"), 1
    )
    pprint(most_popular_english)

    # Get first page of top rated movies abased on German region
    top_rated_german = get_top_rated("/movie/top_rated", COUNTRY_CODES["Germany"], 1)
    pprint(top_rated_german)

    # Get a dictionary of movie details based on text query
    movie_dict = get_movies("/search/movie", "Lost in Translation")

    # Get movie idea based on selected movie title
    movie_id = get_movie_id(movie_dict, "Lost in Translation")

    # Get most similar movies to movie with selected title based on US region
    most_similar = get_most_similar(
        f"/movie/{movie_id}/similar", COUNTRY_CODES["United States"]
    )
    pprint(most_similar)

    # Get recommended movies to movie ID based on US region
    recommended = get_recommended(
        f"/movie/{movie_id}/recommendations", COUNTRY_CODES["United States"]
    )
    pprint(recommended)

    # Get movies within a recent date range based on US region
    recently_released = get_recently_released(
        "/discover/movie", COUNTRY_CODES["United States"], "2022-08-16", "2022-09-23"
    )

    pprint(recently_released)

    # Get a dictionary of available genres
    genre_dict = get_genres("/genre/movie/list")

    # Get a genre ID based on selected genre name
    genre_id = get_genre_id(genre_dict, "Comedy")
    # print(genre_id) # This prints an int 35

    # Get movies released by year based on US region and genre
    movie_year_genre = get_year_genre(
        "/discover/movie", COUNTRY_CODES["United States"], 1990, str(genre_id)
    )

    pprint(movie_year_genre)

    # Get movies with vote count greater than 2000 by year, sorted by popularity
    movie_vote_popular = get_vote_popular("/discover/movie", 2021, 2000, 1)

    pprint(movie_vote_popular)


if __name__ == "__main__":
    main()
