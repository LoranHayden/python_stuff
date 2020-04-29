import municipality_list
import json
import requests

def get_fields(url):
    x = requests.get(url, timeout = 15)
    if int(x.status_code) == 200:
        json_response = x.json()
        fields_json = json_response["fields"]
        # prettyprint it
        #print(json.dumps(fields_json, indent = 4))
        fields = []
        if len(fields_json) > 0:
            for field in fields_json:
                #print(field["name"])
                if field["name"].upper() == "OBJECTID" or field["name"].upper() == "SHAPE" :
                    continue
                fields.append(field["name"])
        print(sorted(fields))
        return sorted(fields)
    else:
        print("Error obtaining required field names from " + url + ".\nAborting upload.")
        return None

get_fields('https://gis.energy.gov.ab.ca/arcgis/rest/services/Geoview/ERCB_Ext_PROD/MapServer/0?f=pjson')

#d = municipality_list.Municipality_List()
#d.to_json()
#def sort_fields(filename, arrayname):
#    fhandle = open(filename)
#    pff_obj = json.load(fhandle)
#    fhandle.close()
#    fields = pff_obj[arrayname]
#    field_dict = {
#        arrayname:sorted(fields)
#        }
#    with open(filename, 'w') as json_file:
#        json.dump(field_dict, json_file, indent=3)
#        json_file.close()
#sort_fields("waste_water_treatment_facility.json", "outputFields_Table_WWCTF")
##fhandle = open("point_feature_fields.json", "w")
#    #json.dump(field_dict, fhandle)
#    #fhandle.close();

## replace hardcoded array with call to this method
#def get_point_fields():
#    fhandle = open('point_feature_fields.json')
#    fields = json.load(fhandle)
#    fhandle.close()
#    return fields
