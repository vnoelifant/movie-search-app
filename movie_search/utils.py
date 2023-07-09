import json

def dump_movie_data_to_json(output_file, data):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)