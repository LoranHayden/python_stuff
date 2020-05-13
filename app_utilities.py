### Utility functions specific to the application
### Author: Loran Hayden
import json
def get_array(path):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close(path)
        return data
def get_object_dictionary(path):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data