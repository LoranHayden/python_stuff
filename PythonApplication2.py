import municipality_list
import json
import requests
import math
import app_utilities
#import arcpy
#def get_fields(url):
#    x = requests.get(url, timeout = 15)
#    if int(x.status_code) == 200:
#        json_response = x.json()
#        fields_json = json_response["fields"]
#        # prettyprint it
#        #print(json.dumps(fields_json, indent = 4))
#        fields = []
#        if len(fields_json) > 0:
#            for field in fields_json:
#                #print(field["name"])
#                if field["name"].upper() == "OBJECTID" or field["name"].upper() == "SHAPE" :
#                    continue
#                fields.append(field["name"])
#        #print(sorted(fields))
#        return sorted(fields)
#    else:
#        print("Error obtaining required field names from " + url + ".\nAborting upload.")
#        return None
#print(app_utilities.get_array('point_feature_fields.json')['outputFields_Point'])
#print('*******************************************************************************')
#print('*******************************************************************************')
#print(app_utilities.get_array('waste_water_treatment_facility.json')['outputFields_Table_WWCTF'])
#print('*******************************************************************************')
#print('*******************************************************************************')
#print(app_utilities.get_array('waste_water_lift_pump_station.json')['outputFields_Table_LPS'])
#print('*******************************************************************************')
#print('*******************************************************************************')
#print(app_utilities.get_array('water_supply_booster_station.json')['outputFields_Table_BST'])
#print('*******************************************************************************')
#print('*******************************************************************************')
#print(app_utilities.get_array('water_supply_treatment_facility.json')['outputFields_Table_WSTF'])
#print('*******************************************************************************')
#print('*******************************************************************************')
#print(app_utilities.get_array('line_feature_fields.json')['outputFields_Line'])

#print(get_fields('https://gis.energy.gov.ab.ca/arcgis/rest/services/Geoview/ERCB_Ext_PROD/MapServer/0?f=pjson'))
#print(app_utilities.get_object_dictionary('municipalities.json')['CB'])
#print(app_utilities.get_object_dictionary('municipalities.json')['CB']['munFolder'])
#muns = app_utilities.get_object_dictionary('municipalities.json')
#asset_fields = app_utilities.get_array('asset_fields.json', 'asset_fields')
#for mun in muns:
#    current_municipality = app_utilities.get_object_dictionary('municipalities.json')[mun]
#    munFolder = current_municipality['munFolder']
#    munName = current_municipality['munName']
#    munFullName = current_municipality['munFullName']
#    munID = current_municipality['munID']
#    shpMunID = current_municipality['shpMunID']

#    print(munFolder)
#    print(munName)
#    print(munFullName)
#    print(munID)
#    print(shpMunID)

#    print('************************************************')
print(app_utilities.get_array('feature_codes.json', 'fcodes'))