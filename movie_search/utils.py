import re

def title_format(query):
    
    exceptions = ["and", "or", "the", "a", "of", "in"]
    title = "a lesson in string splicing"

    lowercase_query = re.split(" ", query.lower())
    final_query = [lowercase_query[0].capitalize()]


    final_query += [word if word in exceptions else word.capitalize() for word in lowercase_query[1:]]

    final_query = " ".join(final_query)

    return final_query
