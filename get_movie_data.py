import json
import requests
import os
import pycountry
from pprint import pprint
from dotenv import load_dotenv
from langcodes import *

load_dotenv()

api_key = os.getenv('PROJECT_API_KEY')
base_url = "https://api.themoviedb.org/3"

def get_country_code(country_name):
    
    countries = {}
    
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2
    
    country_code = countries.get(country_name, 'Unknown code') 
    
    return country_code

def get_popular_movies(search_key, language):
    """This function returns a JSON object of list of the current most popular movies"""

    response = requests.get(f"{base_url}{search_key}", 
                                params={'api_key':api_key,
                                         'language':language})

    return response

def get_top_rated(search_key, region, page):
    """This function returns a a JSON object of list of the top rated movies"""
    response = requests.get(f"{base_url}{search_key}", 
                                params={'api_key':api_key,
                                        'page':page,
                                        'region': region})

    return response

def get_most_similar(search_key):
    """This function returns a a JSON object of list of the most similar movies to movie ID"""
    response = requests.get(f"{base_url}{search_key}", 
                                params={'api_key':api_key})

    return response

def get_recommended(search_key):
    """This function returns a a JSON object of list of recommended movies to movie ID"""
    response = requests.get(f"{base_url}{search_key}", 
                                params={'api_key':api_key})

    return response



def main():
    # Get most popular movies in English Language
    most_popular_english = get_popular_movies("/movie/popular", standardize_tag('eng_US'))
    pprint(most_popular_english.json())
    
     # Get first page of top rated movies abased on German region
    top_rated_german = get_top_rated("/movie/top_rated", get_country_code('Germany'), 1)
    pprint(top_rated_german.json())

    # Get most similar movies to movie ID
    movie_id = 153
    most_similar = get_most_similar(f"/movie/{movie_id}/similar")
    pprint(most_similar.json())

    # Get recommended movies to movie ID
    recommended = get_recommended(f"/movie/{movie_id}/similar")
    pprint(recommended.json())

if __name__ == '__main__':
    main()