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
    with_crew=None,
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
    
    if with_crew is not None:
        params.update({"with_crew": with_crew})

    print("Params: ", params)

    response = requests.get(url, params=params)

    return response.json()


# Discover endpoint functions

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

# Test Queries

#pprint(get_media_data("/watch/providers/movie"))

#with open("providers.json", "w") as provider_data:
#    json.dump(get_media_data("/watch/providers/movie"), provider_data, indent=4, sort_keys=True)

text_query = "Stanley Kubrick"
text_query = text_query.lower()

person = get_person("/search/person", text_query)

print("Person: ",person)

person = {person.lower(): idx for person, idx in person.items()}
print("Person Dictionary: ", person)

# Get person id based on person query
person_id = person.get(text_query)
print("PERSON ID", person_id)

# person_credits = get_media_detail(f"/person/{person_id}/movie_credits")

# with open("person_credits.json", "w") as person_data:
#    json.dump(person_credits, person_data, indent=4, sort_keys=True)

discover_name = get_media_data("/discover/movie",with_people=person_id)
print("Discover by Name: ", discover_name)

with open("discover.json", "w") as data:
    json.dump(discover_name, data, indent=4, sort_keys=True)