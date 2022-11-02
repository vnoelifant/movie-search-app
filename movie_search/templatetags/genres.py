import json
from django import template
from movie_search.models import Genre

register = template.Library()


@register.simple_tag
def get_genres():
    # Get list of available genres
    genre = Genre()
    list_to_store = [
        "Action",
        "Adventure",
        "Animation",
        "Comedy",
        "Crime",
        "Documentary",
        "Drama",
        "Family",
        "Fantasy",
        "Horror",
        "Music",
        "Mystery",
        "Romance",
        "Science Fiction",
        "TV Movie",
        "Thriller",
        "War",
        "Western",
    ]
    genre.genres = json.dumps(list_to_store)
    genre.save()

    json_dec = json.decoder.JSONDecoder()
    genre_list = json_dec.decode(genre.genres)

    print("Genre List: ", genre_list)

    return genre_list
