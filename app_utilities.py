### Utility functions specific to the application
### Author: Loran Hayden
import json
def get_array(path, array_field):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data[array_field]
def get_object_dictionary(path):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data
def empty_string(text):
    return text == '' or text == ' '