import municipality_list
import json
import requests
import math
import app_utilities
import xlrd
import csv
import os
import shutil
import pandas as pd

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def rmdirContents(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def writeError(logfile, errorfield, recordassetcode, errorcount, munfullname):
    logfile.write(str(errorcount) + "." + "Check the '" + errorfield + "' value for the " + recordassetcode + " Asset_Code record in the " + munfullname + " spreadsheet (XLSM).\n\n")

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
#print(app_utilities.get_array('feature_codes.json', 'fcodes'))
#x = ''
#if x == '': print(not x)
#shapefilesExist = False
#wb = xlrd.open_workbook('Copy of LO-20180514.xlsm')
#sheet = wb.sheet_by_name("GENERAL ASSET INFORMATION")
#csvGenAssetInfo = open("GenAssetInfo.csv", "wb")
#wr = csv.writer(csvGenAssetInfo, quoting=csv.QUOTE_ALL)

## Write rows with data (including header row)
#for rownum in xrange(sheet.nrows):
#    # Skip the first two rows
#    if rownum == 0 or rownum == 1:
#        continue
#    # Write other row values to CSV
#    wr.writerow(sheet.row_values(rownum))
## Close the spreadsheet and CSV
#wb.release_resources()
#del wb
#csvGenAssetInfo.close()
##            # List of all fields that should exist in the spreadsheet (in this
##            order)
#fieldsGenAssetInfoCSV = get_array('asset_fields.json', 'asset_fields')
##            # Check if all the necessary fields are in the spreadsheet CSV
##            file
#fieldsCSV = []
#csvGenAssetInfo = open("GenAssetInfo.csv", "rb")
#reader = csv.reader(csvGenAssetInfo)
## read the header
#i = reader.next()
## load the stripped field names into an array
#for field in i:
#    fieldsCSV.append(field.strip())
#for field in fieldsGenAssetInfoCSV:
#    field = field.strip()
#    if "Rplmt" in field:
#        print(field)
#    if field not in fieldsCSV:
#        if field == "GIS Link":
#            if shapefilesExist == True:
#                errorCounter += 1
#                errorLogFile.write(str(errorCounter) + "." + "The " + field + " cannot be found in the " + munFullName + " spreadsheet (.XLSM) file." + "\n\n")
#        else:
#            errorCounter += 1
#            errorLogFile.write(str(errorCounter) + "." + "The " + field + " cannot be found in the " + munFullName + " spreadsheet (.XLSM) file." + "\n\n")

## Close the spreadsheet CSV
#csvGenAssetInfo.close()

#f = pd.read_csv("GenAssetInfo.csv")
#if shapefilesExist == False:
#    keep_col = get_array('required_asset_fields.json', 'required_asset_fields')
#    keep_col.remove('GIS Link')
#else:
#    keep_col = get_array('required_asset_fields.json', 'required_asset_fields')
##new_f = f[keep_col]
##new_f.to_csv("GenAssetInfo.csv", index=False)

##            # Will create a DBF in the municipality folder
#dbfGenAssetInfo = "GenAssetInfo.dbf"
fieldsShapefile = get_array("shapefile_fields.json", "shapefile_fields")
def stupid1():
    global a
    a = 3
def stupid2():
    a = 4
stupid1()
stupid2()
print(str(a))
print('erk')