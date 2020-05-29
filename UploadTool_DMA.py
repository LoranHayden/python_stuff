## ###################################################################################
##         Client : NS Department of Municipal Affairs
##        Purpose : Infrastructure Registry for Municipal Assets Upload Tool
##         Author : Bluejack Consulting Inc.
##  Last modified : 03/09/2018
## Python Version : 2.7
## #####################################################################################
import os
import sys
import glob
import shutil
import string
import numbers
import datetime
from datetime import timedelta
import copy
import shutil
import arcpy
import xlrd
import csv
import pandas as pd
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import zipfile

## Script name
scriptName = "UploadTool_DMA.py"

## Start Time...
starttime = datetime.datetime.now()

## Coordinate system of pilot municipality shapefiles (NAD83 UTM20)
srNAD83_UTM20 = arcpy.SpatialReference(26920)
## Coordinate system of GDB feature classes (NAD83 CSRS UTM20)
## Datum transformation between the two
gt = "NAD_1983_To_WGS_1984_1 + NAD_1983_CSRS_To_WGS_1984_2"

edit = None

outputFields_Point = get_array('point_feature_fields.json','outputFields_Point')
outputFields_Line = get_array('line_feature_fields.json','outputFields_Line')
outputFields_Table_WWCTF = get_array('waste_water_treatment_facility.json','outputFields_Table_WWCTF')
outputFields_Table_LPS = get_array('waste_water_lift_pump_station.json','outputFields_Table_LPS')
outputFields_Table_BST = get_array('water_supply_booster_station.json','outputFields_Table_BST')
outputFields_Table_WSTF = get_array('water_supply_treatment_facility.json','outputFields_Table_WSTF')

def main():
    Validate()

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
    errorcount += 1
    logfile.write(str(errorcount) + "." + "Check the '" + errorfield + "' value for the " + recordassetcode + " Asset_Code record in the " + munfullname + " spreadsheet (XLSM).\n\n")
    return errorcount

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

def get_object_value(path, object_name):
    with open(path) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data[object_name]

def empty_string(text):
    return text == '' or text == ' '

def writeShapeFolderError(logfile,errorCount,folder):
    logfile.write(str(errorCounter) + ". ", "Unable to find folder '" + folder + "'.\n\n")

def writeShapeFileError(logfile,errorCount,shapefile):
    logfile.write(str(errorCounter) + ".", "Unable to find shapefile '" + shapefile + "'.\n\n")

def writeMissingFieldError(logfile, fieldname, errorCount, shapefile):
    logfile.write(str(errorCount) + ". The field '" + fieldname + "' field is missing in the '" + shapefile + "' shapefile.\n\n")

def writeSpatialReferenceError(logfile, errorCount, shapefile):
    logfile.write(str(errorCount) + ". The shapefile '" + shapefile + "' has an invalid spatial reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'.\n\n")

def set_output_fc(_gdb, _gdbOwner, _infClass, _infType):
    return _gdb + "/" + _gdbOwner + _infClass + "/" + _gdbOwner + _infType

def validateFiles(logfile, errorCount, shpFolder, shapefullpath, fieldsShapefile):
    if not os.path.exists(shpFolder):
        errorCount += 1
        writeShapeFolderError(logfile, errorCount, shpFolder)
    else:
        if not arcpy.Exists(shapefullpath):
            errorCounter += 1
            writeShapeFileError(logfile, errorCount, shapefullpath)
        else:
            # Make sure its spatial reference is NAD83 UTM20
            if arcpy.Describe(shapefullpath).spatialReference.factoryCode == 26920 or arcpy.Describe(shapefullpath).spatialReference.factoryCode == 2961:
                # Check that it has all the correct fields
                fieldsShpNames = arcpy.ListFields(shpfullpath)
                # Check fields against mandatory shapefile fields
                # Only Shape, Elevation, Width and GIS_Link are taken from the
                # shapefiles; others come from the spreadsheet CSV
                if ("Elev" not in fieldsShpNames) and ("Elevation" not in fieldsShpNames) and ("ELEVATION" not in fieldsShpNames):
                    errorCounter += 1 
                    writeMissingFieldError(logfile, "Elev", errorCount, shapefullpath)
                for field in fieldsShapefile:
                    if field == "Elev":
                        continue
                    if field not in fieldsShpNames:
                        errorCounter += 1
                        writeMissingFieldError(logfile, field, errorCount, shapefullpath)
            else:
                errorCounter += 1
                writeSpatialReferenceError(logfile, errorCount, shapefullpath)

def Validate():

    try:
        #global parentFolder, munFolder, munID, shpMunID, munName, mun
        global munFolder, munID, shpMunID, munName, mun, munFullName
        global method, shapefilesExist, gdb

        # Default value
        shapefilesExist = True

        # Get 2 of the parameters
        mun = arcpy.GetParameterAsText(0)
        method = arcpy.GetParameterAsText(1)
        #parentFolder = arcpy.GetParameterAsText(2) + "/"
        #gdb = arcpy.GetParameterAsText(3) + "/"


        # Set different variables according to what the input method is
        if method == "GIS":
            shapefilesExist = True
        elif method == "Survey":
            shapefilesExist = False

        # ===============================================================================
        # ===============================================================================
        # ===============================================================================
        # Hard-coded parent folder - on the VM
        #parentFolder = "C:/Projects/DMA/UploadTool/Uploads/"
        # On my machine
        #parentFolder = "C:/Work/Projects/DMA/UploadTool/Uploads/"

        arcpy.env.scratchWorkspace = '%scratchworkspace%'

        # The folder names on the server that store the whole structure of
        # files (what's in the zip file)
        # need to be called these following names and paths:

        # Get municipality folder, name and IDs from mun variable
        # Set variables accordingly
        current_municipality = get_object_dictionary('municipalities.json')[mun]
        munFolder = arcpy.env.scratchWorkspace + current_municipality['munFolder']
        munName = current_municipality['munName']
        munFullName = current_municipality['munFullName']
        munID = current_municipality['munID']
        shpMunID = current_municipality['shpMunID']

#        # Unzip the file to the munFolder
        global munZipfile, zip_ref
        zip_ref = zipfile.ZipFile(munZipfile, "r")
        # If munFolder doesn't exist, create it
        if not os.path.exists(munFolder):
            os.mkdir(munFolder)
        # If it does exist, clear out its contents (previous run)
        else:
            rmdirContents(munFolder)

        # Extract to municipality folder
        zip_ref.extractall(munFolder)
        zip_ref.close()


        # Count number of errors
        errorCounter = 0

        # Note: The coordinate system of the shapefiles for the pilot
        # municipalities is NAD83 UTM20
        # The current standard at NSGI is NAD83 CSRS UTM20, and the geodatabase
        # feature classes
        # will be using the new one.  So, the data will be to be
        # projected/transformed before input.
        # In the future, any new data should be collected in NAD83 CSRS UTMN20
        # so won't need
        # projecting/transforming
        #
        # Coordinate system of pilot municipality shapefiles (NAD83 UTM20)
        srNAD83_UTM20 = arcpy.SpatialReference(26920)
        # Coordinate system of GDB feature classes (NAD83 CSRS UTM20)
        srNAD83_CSRS_UTM20 = arcpy.SpatialReference(2961)
        # Datum transformation between the two
        gt = "NAD_1983_To_WGS_1984_1 + NAD_1983_CSRS_To_WGS_1984_2"

        # Extract to method?
        dtNow = datetime.datetime.now()
        errorFilenameShort = "UploadTool_Errors_" + str(dtNow.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
        errorFilename = munFolder + errorFilenameShort
        errorLogFile = open(errorFilename, "w")
        errorLogFile.write("Upload Tool Error Log for " + munFullName + "\n")
        errorLogFile.write(str(dtNow.strftime("%d %b %Y, %H:%M:%S")) + "\n")
        errorLogFile.write("---------------------\n\n")


#        # Main Municipality spreadsheet (XLSM)
        for file in os.listdir(munFolder):
            if file.endswith(".xlsm") and file.startswith(munID):
                fileSpreadsheet = munFolder + file
                existSpreadsheet = True
                break
            else:
                existSpreadsheet = False

        if existSpreadsheet == False:
            errorCounter += 1
            errorLogFile.write(str(errorCounter) + "." + "The " + munFullName + " spreadsheet (.XLSM)" + " cannot be found." + "\n")
        else:
            # open the spreadsheet and see what the fields are in the General
            # Asset Information sheet
            wb = xlrd.open_workbook(fileSpreadsheet)
            sheet = wb.sheet_by_name("GENERAL ASSET INFORMATION")
            csvGenAssetInfo = open(munFolder + "GenAssetInfo_" + munID + ".csv", "wb")
            wr = csv.writer(csvGenAssetInfo, quoting=csv.QUOTE_ALL)

            # Write rows with data (including header row)
            for rownum in xrange(sheet.nrows):
                # Skip the first two rows
                if rownum == 0 or rownum == 1:
                    continue
                # Write other row values to CSV
                wr.writerow(sheet.row_values(rownum))

            # Close the spreadsheet and CSV
            wb.release_resources()
            del wb
            csvGenAssetInfo.close()

#            # List of all fields that should exist in the spreadsheet (in this
#            order)
            fieldsGenAssetInfoCSV = get_array('asset_fields.json', 'asset_fields')
#            # Check if all the necessary fields are in the spreadsheet CSV
#            file
            fieldsCSV = []
            csvGenAssetInfo = open(munFolder + "GenAssetInfo_" + munID + ".csv", "rb")
            reader = csv.reader(csvGenAssetInfo)
            # read the header
            i = reader.next()
            # load the stripped field names into an array
            for field in i:
                fieldsCSV.append(field.strip())
            for field in fieldsGenAssetInfoCSV:
                field = field.strip()

                if field not in fieldsCSV:
                    if field == "GIS Link":
                        if shapefilesExist == True:
                            errorCounter += 1
                            errorLogFile.write(str(errorCounter) + "." + "The " + field + " cannot be found in the " + munFullName + " spreadsheet (.XLSM) file." + "\n\n")
                    else:
                        errorCounter += 1
                        errorLogFile.write(str(errorCounter) + "." + "The " + field + " cannot be found in the " + munFullName + " spreadsheet (.XLSM) file." + "\n\n")

            # Close the spreadsheet CSV
            csvGenAssetInfo.close()

#            # The sheet/CSV has too many empty or unneeded columns, so will
#            only take ones we need
#            # Need to export to a new CSV in the municipality folder
            #f = pd.read_csv(munFolder + "GenAssetInfo_" + munID + ".csv")
            if shapefilesExist == False:
                keep_col = get_array('required_asset_fields.json', 'required_asset_fields').remove('GIS Link')
            else:
                keep_col = get_array('required_asset_fields.json', 'required_asset_fields')
            #new_f = f[keep_col]
            #new_f.to_csv(munFolder + "GenAssetInfo.csv", index=False)

#            # Will create a DBF in the municipality folder
            dbfGenAssetInfo = munFolder + "GenAssetInfo.dbf"
#            # Convert CSV to DBF
            arcpy.TableToTable_conversion(munFolder + "GenAssetInfo.csv", munFolder, "GenAssetInfo.dbf")

#            # Check the content of the CSV file for data errors
#            # =================================================
#            # Check every FCode values against this full list
#            # Added WWST May 06, 2019 - forgot to add it before
            fcodes = get_array('feature_codes.json', 'fcodes')

            with arcpy.da.SearchCursor(dbfGenAssetInfo, keep_col) as dbfCursor:
                for dbfRec in dbfCursor:
                    # Go to next record if AssetCode is blank (some
                    # spreadsheets have blank records)
                    if dbfRec.isNull('Asset_Code'): continue
                    field = dbfRec.getValue('Asset_Code')
                    if empty_string(str(field)): continue
                    else: assetcode = str(field)

                    # FeatureCod- dbfRec[4]
                    field = dbfRec.getValue('FeatureCode')
                    if not field or empty_string(str(field)) or not str(field) in fcodes:
                        errorCounter = writeError(errorLogFile, 'FeatureCode', assetcode, errorCounter, munFullName)

#                    # Condition - dbfRec[5]
                    field = dbfRec.getValue('Condition')
                    if field == None or not is_number(field) or is_number(field) > 5:
                        errorCounter = writeError(errorLogFile, 'Condition', assetcode, errorCounter, munFullName)

#                    # Quantity - dbfRec[8]
                    field = dbfRec.getValue('Quantity')
                    if field == None or not is_number(field) or empty_string(field):
                        errorCounter = writeError(errorLogFile, 'Quantity', assetcode, errorCounter, munFullName)

#                    # Estimated (Estimated RUL) - dbfRec[19]
                    field = dbfRec.getValue('Estimated RUL')
                    if field == None or not is_number(field) or empty_string(field):
                        errorCounter = writeError(errorLogFile, 'Estimated RUL', assetcode, errorCounter, munFullName)


#                    # RplmtCst - dbfRec[20]
                    field = dbfRec.getValue('RplmtCst')
                    if field == None or not is_number(field) or empty_string(field):
                        errorCounter = writeError(errorLogFile, 'RplmtCst', assetcode, errorCounter, munFullName)


#                    # ConditionB (ConditionBasis) - dbfRec[21]
                    field = dbfRec.getValue('ConditionBasis')
                    if not field or empty_string(field):
                        errorCounter = writeError(errorLogFile, 'ConditionBasis', assetcode, errorCounter, munFullName)

#                    # CostLookup - dbfRec[31]
                    field = dbfRec.getValue('CostLookup')
                    if not field or empty_string(field):
                        errorCounter = writeError(errorLogFile, 'CostLookup', assetcode, errorCounter, munFullName)

#                    # Unit_Cost - dbfRec[37]
                    field = dbfRec.getValue('Unit Cost')
                    if field == None or not is_number(field) or empty_string(field):
                        errorCounter = writeError(errorLogFile, 'Unit Cost', assetcode, errorCounter, munFullName)
                        
                    if shapefilesExist == True:
                        # GIS_Link - dbfRec[39]
                        field = dbfRec.getValue('GIS Link')
                        if not field or empty_string(field):
                            errorCounter = writeError(errorLogFile, 'GIS Link', assetcode, errorCounter, munFullName)

#            # Parent folder of all shapefiles
            shpFolder = munFolder + "GIS Imports/"
            if not os.path.exists(shpFolder):
                errorCounter += 1
                errorLogFile.write(str(errorCounter) + "." + "The 'GIS_Imports' folder cannot be found." + "\n\n")


            # There is inconsistent naming across shapefiles for the various
            # fields
            # specifically:
            # "Elev" Sometimes called "Elevation"
            # "FCode" Sometimes called "FeatureCod" "FreatureCo" or "Feature"
            # "N" Sometimes called "Northing"
            # "E" Sometimes called "Easting"
            # "Install_Yr" Sometimes called "Install Yr" or "Install_Da"
            # "Comments" Sometimes called "Comment"
            # "Quantity" Sometimes called "Length"
            fieldsShapefile = get_array("shapefile_fields.json", "shapefile_fields")

            # Check fields in shapefiles if shapefilesExist = True (method =
            # "GIS")
            if shapefilesExist == True:
                shapefileNames = get_array('shapefile_names.json', 'shapefile_names')
                for shapefile_name in shapefileNames:
                    shpfilefolder = shpFolder + shapefile_name + '/'
                    shpfilename = shpMunID + ' ' + shapefile_name + '.shp'
                    shpFullPath = shpfilefolder + shpFileName
                    validateFiles(errorLogFile, errorCounter, shpfilefolder, shpFullPath, fieldsShapeFile)

        # Close the error log file
        errorLogFile.close()


        # =============================================================================================
        # Send an email to the user if validation fails (with txt file), or
        # after upload, if successful

        if errorCounter > 0:
            #raise Exception?
            UploadStatus = "Validation Failed"
            NotifyClient(munFullName, errorFilenameShort, errorFilename, UploadStatus)
            arcpy.AddError("Validation Failed")
        else:
            # Proceed with the Upload
            UploadStatus = Upload()

        # =============================================================================================

    # NOTE: These exceptions are from the very beginning of the Validate method
    except KeyboardInterrupt:
        exit()

    except Exception, e:
        arcpy.AddMessage("ERROR: Exception on line number: " + str(sys.exc_traceback.tb_lineno) + "\n" + str(e) + "\n")
        UploadStatus = "Validation Failed"
        NotifyClient(munFullName, errorFilenameShort, errorFilename, UploadStatus)
    finally:
        if not errorLogFile.closed:
            errorLogFile.close()

def Upload():

    try:
        
        global totalCounter

        # Get the Spreadsheet Export folder
        ssExportFolder = munFolder + "Spreadsheet Export/"
        # Get folder where shapefiles reside (or will reside)
        shpFolder = munFolder + "GIS Imports/"

        # Set workspace to Spreadsheet Export folder
        arcpy.env.workspace = ssExportFolder
        # Overwrite any outputs
        arcpy.env.overwriteOutput = True


        # Get the CSV file of spreadsheet (General Asset Information sheet)
        csvGenAssetInfo = munFolder + "GenAssetInfo.csv"
        # Convert CSV file to DBF
        arcpy.TableToTable_conversion(csvGenAssetInfo, munFolder, "GenAssetInfo.dbf")
        dbfGenAssetInfo = munFolder + "GenAssetInfo.dbf"



#        ====================================================================================================================
#        Begin of Survey-method-only code
#        ====================================================================================================================

        # If the Survey method is chosen, then we have to input the data into
        # the shapefiles first
        if shapefilesExist == False:

            # Get the actual spreadsheet
            for file in os.listdir(munFolder):
                if file.endswith(".xlsm") and file.startswith(munID):
                    fileSpreadsheet = munFolder + file
                    break


            # Get the Asset Details sheet
            wb = xlrd.open_workbook(fileSpreadsheet)
            sheetAssetDetails = wb.sheet_by_name("Asset Details")
            csvAssetDetails = open(munFolder + "AssetDetails.csv", "wb")
            wr = csv.writer(csvAssetDetails, quoting=csv.QUOTE_ALL)

            # Write remaining rows with data
            for rownum in xrange(sheetAssetDetails.nrows):
                # Skip the first two rows
                if rownum == 0 or rownum == 1:
                    continue
                # Write other row values to CSV
                wr.writerow(sheetAssetDetails.row_values(rownum))

            # Close the spreadsheet and CSV
            wb.release_resources()
            del wb
            csvAssetDetails.close()


            # Will create a temporary DBF in the municipality folder
            dbfFile = munFolder + "AssetDetails.dbf"
            # Delete if already there
            if os.path.isfile(dbfFile):
                os.remove(dbfFile)
            # Might also be a dbf.xml file
            if os.path.isfile(munFolder + "AssetDetails.dbf.xml"):
                os.remove(munFolder + "AssetDetails.dbf.xml")
            # Convert CSV to DBF
            arcpy.TableToTable_conversion(munFolder + "AssetDetails.csv", munFolder, "AssetDetails.dbf")


            # Need to create all the shapefiles in the various subfolders of
            # the GIS Imports folder
            arcpy.env.workspace = shpFolder
            arcpy.env.overwriteOutput = True

            # Will create them in UTM 20 NAD83 CSRS spatial reference
            srNAD83_CSRS_UTM20 = arcpy.SpatialReference(2961)

#            #print "Creating shapefiles from the AssetDetails sheet..." + "\n"
            shapefileNames = get_array('shapefile_names.json', 'shapefile_names')
            for sfname in shapefileNames:
                if arcpy.Exists(shpFolder + sfname + '/' + shpMunID + ' ' + sfname + '.shp'):
                    arcpy.Delete_management(shpFolder + sfname + '/' + shpMunID + ' ' + sfname + '.shp')
                shapefileName = shpFolder + sfname + "/" + shpMunID + " " + sfname + ".shp"
                arcpy.CreateFeatureclass_management(shpFolder + sfname, shpMunID + " " + sfname, "POINT", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
                arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
                arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
                arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
                arcpy.AddField_management(shapefileName, "Elevation", "LONG")
                arcpy.AddField_management(shapefileName, "Width", "LONG")

            # Cursor through DBF file and put things in the appropriate
            # shapefiles
            inputFields_AssetDetails = get_array("asset_details.json", "asset_details")
            outputFields_Shp_Point = get_array("point_fields.json", "point_fields")
            outputFields_Shp_Line = get_array("polyline_fields.json", "polyline_fields")

#            # Initialize counter
            counter = 0 # not sure this is ever used?????

            #region load point features
            for sfname in shapefileNames:
                if sfname.endswith(' P'):
                    usfname = sfname.replace(' ', '_') # need a version with an underscore instead of space
                    tab_P = "AssetDetails_" + usfname
                    query = get_object_value('query_strings.json', 'query' + usfname)
                    arcpy.MakeTableView_management(tabAssetDetails, tab_P, query)
                    count_P = arcpy.GetCount_management(tab_P).getOutput(0)
                    if count_P > 0:
                        arcpy.CopyRows_management(tab_P, munFolder + "AssetDetails_" + usfname + ".dbf")

                    outputShapeFile = shpFolder + sfname + "/" + shpMunID + " " + sfname + ".shp"
                    editShapefile = arcpy.da.Editor(shpFolder + sfname + "/")
                    editShapefile.startEditing(False, True)
                    editShapefile.startOperation()
                    current_dbf = munFolder + "AssetDetails_" + usfname + ".dbf"
                    with arcpy.da.SearchCursor(current_dbf, inputFields_AssetDetails) as inputCursor:
                        for inputRec in inputCursor:
                            # Create shape from Northing and Easting
                            # coordinates
                            x = inputRec[2]  # Easting
                            y = inputRec[1]  # Northing
                            # AssetCode
                            AssetCode = inputRec[0]
                            # Elevation
                            Elev = float(inputRec[3])
                            # Width
                            if is_number(inputRec[4]):
                                Width = Dbl(inputRec[4])
                            else:
                                Width = 0
                            # Feature Code
                            FCode = inputRec[5]
                            # Write values to output shapefile
                            with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Point) as outputCursor:
                               # Insert the feature
                               outputCursor.insertRow((x, y, AssetCode, munID, FCode, Elev, Width))
                    # Stop the edit operation
                    editShapefile.stopOperation()
                    # Stop the edit session and save the changes
                    editShapefile.stopEditing(True)
            #endregion

            #region load line features
            for sfname in shapefileNames:
                print(sfname)
                if sfname.endswith(' L'):
                    #print(sfname)
                    usfname = sfname.replace(' ', '_') # also need a version with underscore instead of space
                    udbf = munFolder + "AssetDetails_" + usfname + ".dbf"
                    tab_L = "AssetDetails_" + usfname
                    query = get_object_value('query_strings.json', 'query' + usfname)
                    arcpy.MakeTableView_management(tabAssetDetails, tab_L, query)
                    count_L = arcpy.GetCount_management(tab_L).getOutput(0)
                    if count_L > 0:
                        arcpy.CopyRows_management(tabPWS_L, udbf)
                    # Make a list of AssetCodes
                    lstAssetCodes = []
                    
                    # Cursor through input table and get a list of asset codes
                    with arcpy.da.SearchCursor(udbf, inputFields_AssetDetails) as inputCursor:
                        # Cursor through all records to get a unique list
                        for inputRec in inputCursor:
                            if inputRec[0] not in lstAssetCodes: lstAssetCodes.append(inputRec[0])
                    # Output shapefile
                    outputShapeFile = shpFolder + sfname + "/" + shpMunID + " " + sfname + ".shp"
                    editShapefile = arcpy.da.Editor(shpFolder + sfname + "/")

                    # Start editing - without an undo/redo stack
                    editShapefile.startEditing(False, True)
                    # Start an edit operation
                    editShapefile.startOperation()

                    # For each Asset Code, query the table and make polylines
                    for ac in lstAssetCodes:

                        # Create query
                        queryAssetCode = "\"Asset_Code\" = '" + ac + "'"
                        with arcpy.da.SearchCursor(udbf, inputFields_AssetDetails, queryAssetCode) as inputCursor:

                            # Create an empty array
                            arrayPoints = arcpy.Array()

                            for inputRec in inputCursor:
                                # Get Feature Code first
                                FCode = inputRec[5]
                                #print FCode

                                # If FCode has "-S" at the end, create a point
                                # and add
                                #to the array.
                                # Then just go to the next record
                                if "-S" in FCode:
                                    # Northing and Easting coordinates for
                                    # Start Point
                                    x = inputRec[2] # Easting
                                    y = inputRec[1] # Northing
                                    # Create point
                                    pntStart = arcpy.Point(x, y)
                                    # Add start point to the array
                                    arrayPoints.add(pntStart)
                                else:
                                    # AssetCode
                                    AssetCode = inputRec[0]
                                    # Elevation
                                    Elev = float(inputRec[3])
                                    # Width
                                    if is_number(inputRec[4]):
                                        Width = Dbl(inputRec[4])
                                    else:
                                        Width = 0
                                    # FCode
                                    FCode = inputRec[5]
                                    # Northing and Easting coordinates for next
                                    # Point
                                    x = inputRec[2] # Easting
                                    y = inputRec[1] # Northing
                                    # Create point
                                    pntNext = arcpy.Point(x, y)
                                    # Add to array
                                    arrayPoints.add(pntNext)

                            # Make sure array has at least 2 points
                            if arrayPoints.count >= 2:
                                # Make the line once all points collected
                                # (usually just 2)
                                polyline = arcpy.Polyline(arrayPoints, srNAD83_CSRS_UTM20)

                                # Write values to output shapefile
                                with arcpy.da.InsertCursor(outputShapeFile,
                                outputFields_Shp_Line) as outputCursor:
                                    # Insert the feature
                                    outputCursor.insertRow(((polyline), AssetCode, munID, FCode, Elev, Width))


                    # Stop the edit operation
                    editShapefile.stopOperation()
                    # Stop the edit session and save the changes
                    editShapefile.stopEditing(True)
#endregion


#        ====================================================================================================================
#        # End of Survey-method-only code
#        ====================================================================================================================

#        ====================================================================================================================
#        # Begin of GIS-method-only code
#        ====================================================================================================================
        # Hard-code the gdb connection
        # NSGI
        gdb = "D:/SDEConnect/AssetViewer.sde"

        # Check if any features/records for this municipality exist already and
        # truncate them if they do


        # Set the current workspace
        arcpy.env.workspace = gdb

        # Start editing on the output file GDB
        edit = arcpy.da.Editor(gdb)
        # Start editing - without an undo/redo stack
        edit.startEditing(False, False)
        # Start an edit operation
        edit.startOperation()

        # Query the municipality code
        munQuery = "MunID = '" + munID + "'"

        fds = get_array('dataset_names.json', 'dataset_names')
        for dsname in fds:
            for fc in arcpy.ListFeatureClasses("", "", dsname):
                if not arcpy.TestSchemaLock(fc):
                    # Make a feature layer with any features matching the MunID
                    # query
                    fcLayer = fc + "_" + munID
                    arcpy.MakeFeatureLayer_management(fc, fcLayer, munQuery)
                    countMunID = arcpy.GetCount_management(fc + "_" + munID).getOutput(0)
                    if countMunID > 0:
                        # Delete any dataset features for that municipality
                        arcpy.DeleteRows_management(fc + "_" + munID)
                else:
                    arcpy.AddError("The database is locked by another user or process.")
                    raise Exception
        # Stand-alone tables
        dstn = get_array('dataset_table_names.json', 'dataset_table_names')
        for tab in arcpy.ListTables():
            if not arcpy.TestSchemaLock(tab):
                for dst in dstn:
                    if dst in tab:
                        # Make a table view with any records matching the MunID
                        # query
                        tabView = tab + "_" + munID
                        arcpy.MakeTableView_management(tab, tabView, munQuery)
                        countMunID = arcpy.GetCount_management(tabView).getOutput(0)
                        #print "Records found in " + tab + ": " + countMunID
                        if countMunID > 0:
                            # Delete any records in stand-alone tables for that
                            # municipality
                            #print "Deleting " + countMunID + " records in " +
                            #tab + "\n"
                            arcpy.DeleteRows_management(tab + "_" + munID)
                        break
                else:
                    arcpy.AddError("The database is locked by another user or process.")
                    raise Exception


        # Stop the edit operation
        edit.stopOperation()

        # Initialize total counter
        global totalcounter
        totalcounter = 0

        # Go into each shapefile folder, find shapefile and join to spreadsheet
        # CSV file
        subFolders = [x[0] for x in os.walk(shpFolder)] # a list comprehension

        for subFolder in subFolders:
            # Don't need to do the root folder
            if subFolder == shpFolder:
                continue
            # Start an edit operation
            edit.startOperation()
            # Set the workspace to be the current shapefile folder
            shpWorkspace = subFolder
            arcpy.env.workspace = shpWorkspace
            arcpy.env.overwriteOutput = True

            shapefile = ""

            # check the last five characters of the subFolder name
            if subFolder[-5:] == "PWS L":
                # Shapefile will be called "<shpMunID> PWS L.shp"
                shapefile = shpMunID + " PWS L.shp"
            elif subFolder[-5:] == "PWS P":
                # Shapefile will be called "<shpMunID> PWS P.shp"
                shapefile = shpMunID + " PWS P.shp"
            elif subFolder[-5:] == "SWC L":
                # Shapefile will be called "<shpMunID> SWC L.shp"
                shapefile = shpMunID + " SWC L.shp"
            elif subFolder[-5:] == "SWC P":
                # Shapefile will be called "<shpMunID> SWC P.shp"
                shapefile = shpMunID + " SWC P.shp"
            elif subFolder[-5:] == "TRN L":
                # Shapefile will be called "<shpMunID> TRN L.shp"
                shapefile = shpMunID + " TRN L.shp"
            elif subFolder[-5:] == "TRN P":
                # Shapefile will be called "<shpMunID> TRN P.shp"
                shapefile = shpMunID + " TRN P.shp"
            elif subFolder[-5:] == "WWC L":
                # Shapefile will be called "<shpMunID> WWC L.shp"
                shapefile = shpMunID + " WWC L.shp"
            elif subFolder[-5:] == "WWC P":
                # Shapefile will be called "<shpMunID> WWC P.shp"
                shapefile = shpMunID + " WWC P.shp"
            else:
                shapefile = ""

            # Set fc to the shapefile and get shape type
            fc = shapefile
            desc = arcpy.Describe(fc)
            shapeType = desc.shapeType

            # Coordinate system of shapefiles (NAD83 UTM20)
            srNAD83_UTM20 = arcpy.SpatialReference(26920)
            # Coordinate system of GDB feature classes (NAD83 CSRS UTM20)
            srNAD83_CSRS_UTM20 = arcpy.SpatialReference(2961)
            # Datum transformation between the two
            gt = "NAD_1983_To_WGS_1984_1 + NAD_1983_CSRS_To_WGS_1984_2"


            # If shapefiles already existed (i.e.  GIS Method)
            if shapefilesExist == True:

                # Project the shapefile to UTM 20 NAD83 CSRS if not already in
                # that coordinate system
                if arcpy.Describe(fc).spatialReference.factoryCode == 26920:
                    # Project tool doesn't like spaces, so need to get rid of
                    # them
                    fcProj = fc.replace(" ", "_")[:-4] + "_Proj.shp"
                    arcpy.Project_management(fc, fcProj, srNAD83_CSRS_UTM20, gt)
                    # Join the shapefile to the spreadsheet dbf
                    fcJoin = fc.replace(" ", "_")[:-4] + "_Join"
                    arcpy.MakeFeatureLayer_management(fcProj, fcJoin)
                    #shapefileName = fc.replace(" ", "_")[:-4] + "_Proj"
                    shapefileName = fcProj.replace(" ", "_")[:-4]

                # If already in UTM 20 NAD83 CSRS, don't need to project
                elif arcpy.Describe(fc).spatialReference.factoryCode == 2961:
                    # Join the shapefile to the spreadsheet dbf
                    fcJoin = fc.replace(" ", "_")[:-4] + "_Join"
                    arcpy.MakeFeatureLayer_management(fc, fcJoin)
                    # Commented out 02 May 2019 and replaced with line below
                    it
                    #shapefileName = fc.replace(" ", "_")[:-4]
                    shapefileName = fc.replace(" ", " ")[:-4]

                # Join the shapefile with the dbf based on the GIS_Link field
                arcpy.AddJoin_management(fcJoin, "GIS_Link", dbfGenAssetInfo, "GIS_Link")

            else:
                # Join the shapefile to the spreadsheet dbf
                fcJoin = fc.replace(" ", "_")[:-4] + "_Join"
                arcpy.MakeFeatureLayer_management(fc, fcJoin)

                # Join the shapefile with the dbf based on the AssetCode field
                arcpy.AddJoin_management(fcJoin, "AssetCode", dbfGenAssetInfo, "Asset_Code")
                shapefileName = fc[:-4]


            # Check if the Elevation field is called Elevation, ELEVATION, Elev
            # or ELEV
            fieldNames = [f.name for f in arcpy.ListFields(fcJoin)]
            fieldElevName = ""
            if "Elevation" in fieldNames:
                fieldElevName = "Elevation"
            elif "ELEVATION" in fieldNames:
                fieldElevName = "ELEVATION"
            elif "Elev" in fieldNames:
                fieldElevName = "Elev"
            elif "ELEV" in fieldNames:
                fieldElevName = "ELEV"

#            # Only some of these fields are necessary for the upload
            input_fields = get_array('input_fields.json', 'input_fields')
            inputFields = ["Shape@", shapefileName + "." + fieldElevName, shapefileName + ".Width"]
            inputFields += input_fields
            if method == "GIS":
                shapefilesExist = True    
            # Need extra AssetCode and FCode fields in case there is no
            # matching record when joined
            elif method == "Survey":
                shapefilesExist = False
                inputFields.append(shapefileName + ".AssetCode") 
                inputFields.append(shapefileName + ".FCode")

            # Initialize counter
            counter = 0

            # Cursor through input feature class using query
            with arcpy.da.SearchCursor(fcJoin, inputFields) as inputCursor:

                # Write values to output feature class
                for inputRec in inputCursor:

                    # Get shape
                    shp = inputRec[0]

                    # Elevation
                    if inputRec[1] == None:
                        Elev = None
                    elif is_number(inputRec[1]):
                        Elev = float(inputRec[1])
                    else:
                        Elev = None

                    # Width
                    if inputRec[2] == None:
                        Width = None
                    elif is_number(inputRec[2]):
                        #Width = int(inputRec[2])
                        Width = int(round(inputRec[2]))
                        #Width = float(inputRec[2])
                    else:
                        Width = None

                    # Asset Code
                    # Depending on whether shapefiles existed (method), get
                    # AssetCode from one of two fields
                    if not inputRec[3] and shapefilesExist == False:
                        AssetCode = str(inputRec[31])
                        if AssetCode is not None:
                            MunID = inputRec[31].split("-")[0]
                            # Make sure MunID in AssetCode is the same as the
                            # current municipality
                            if MunID == munID:
                                AssetClass = inputRec[31].split("-")[1]
                                AssetSubtype = inputRec[31].split("-")[2]
                            else:
                                continue
                        else:
                            continue
                    elif str(inputRec[3]) == "" or str(inputRec[3]) == " ":
                        AssetCode = None
                        continue
                    else:
                        AssetCode = inputRec[3]
                        NoneType = type(None)
                        if not isinstance(AssetCode, NoneType):
                            MunID = inputRec[3].split("-")[0]
                            # Make sure MunID in AssetCode is the same as the
                            # current municipality
                            if MunID == munID:
                                AssetClass = inputRec[3].split("-")[1]
                                AssetSubtype = inputRec[3].split("-")[2]
                            else:
                                continue
                        else:
                            continue


                    # Location Description
                    if not inputRec[4]:
                        LocDesc = None
                    elif str(inputRec[4]) == "" or str(inputRec[4]) == " ":
                        LocDesc = None
                    else:
                        LocDesc = str(inputRec[4])

                    # FCode
                    if not inputRec[5]:
                        if shapefilesExist == False:
                            FCode = str(inputRec[32])
                        else:
                            FCode = None
                    elif str(inputRec[5]) == "" or str(inputRec[5]) == " ":
                        FCode = None
                    else:
                        FCode = str(inputRec[5])

                    # Condition
                    if inputRec[6] == None:
                        Condition = None
                    elif is_number(inputRec[6]):
                        if int(inputRec[6]) == 0:
                            Condition = 0
                        elif int(inputRec[6]) > 5:
                            Condition = None
                        else:
                            Condition = int(inputRec[6])
                    else:
                        Condition = None

                    # Inspection Date
                    # There are currently no Inspection Dates in spreadsheets -
                    # this may change?  Not sure how they will be formatted.
                    if not inputRec[7]:
                        InspectDate = None
                    elif str(inputRec[7]) == "" or str(inputRec[7]) == " ":
                        InspectDate = None
                    else:
                        InspectDate = inputRec[7]

                    # Status - often in spreadsheets as "active" or "activate"
                    # or "Activate"
                    if not inputRec[8]:
                        Status = None
                    elif str(inputRec[8]) == "" or str(inputRec[8]) == " ":
                        Status = "Active"
                    elif str(inputRec[8]) in ["active","Active","activate","Activate"]:
                        Status = "Active"
                    else:
                        Status = str(inputRec[8])

                    # Quantity
                    if shapeType == "Polyline":
                        if inputRec[9] == None:
                            MeasuredLength = None
                        elif is_number(inputRec[9]):
                            if inputRec[9] == 0:
                                MeasuredLength = 0
                            else:
                                #MeasuredLength = int(float(inputRec[9]))
                                MeasuredLength = int(round(float(inputRec[9])))
                        else:
                            MeasuredLength = 0
                    else:
                        MeasuredLength = 0

                    # Material
                    # Check some road and sidewalk/trail fcodes for materials
                    if FCode in ("RRCB-A", "RRCB-A-S", "RRRD-A", "RRRD-A-S", "RRDR-A", "RRDR-A-S", "RRSW-A", "RRSW-A-S"):
                        Material = "Asphalt"
                    elif FCode in ("RRCB-C", "RRCB-C-S", "RRSW-C", "RRSW-C-S"):
                        Material = "Concrete"
                    elif FCode in ("RRGR", "RRGR-S"):
                        Material = "Gravel"
                    elif FCode in ("RRSW-B", "RRSW-B-S"):
                        Material = "Brick"
                    else:
                        if not inputRec[11]:
                            Material = "Unknown"
                        elif str(inputRec[11]) == "" or str(inputRec[11]) == " ":
                            Material = "Unknown"
                        else:
                            Material = str(inputRec[11])

                    # Comments
                    if not inputRec[12]:
                        Comments = None
                    elif str(inputRec[12]) == "" or str(inputRec[12]) == " ":
                        Comments = None
                    else:
                        Comments = str(inputRec[12])

                    # Region
                    if not inputRec[13]:
                        Region = None
                    elif str(inputRec[13]) == "" or str(inputRec[13]) == " ":
                        Region = None
                    else:
                        Region = str(inputRec[13])

                    # Department
                    if not inputRec[14]:
                        Dept = None
                    elif str(inputRec[14]) == "" or str(inputRec[14]) == " ":
                        Dept = None
                    else:
                        Dept = str(inputRec[14])

                    # Division
                    if not inputRec[15]:
                        Division = None
                    elif str(inputRec[15]) == "" or str(inputRec[15]) == " ":
                        Division = None
                    else:
                        Division = str(inputRec[15])

                    # Person Responsible
                    if not inputRec[16]:
                        PersResp = None
                    elif str(inputRec[16]) == "" or str(inputRec[16]) == " ":
                        PersResp = None
                    else:
                        PersResp = str(inputRec[16])

                    # Install Year
                    if inputRec[17] == None:
                        InstallYear = None
                    elif is_number(inputRec[17]):
                        if inputRec[17] == 0:
                            InstallYear = None
                        else:
                            InstallYear = int(float(inputRec[17]))
                    else:
                        InstallYear = None

                    # Age
                    if inputRec[10] == None:
                        Age = None
                    elif is_number(inputRec[10]):
                        if inputRec[10] == 0:
                            Age = None
                        else:
                            Age = int(float(inputRec[10]))
                    else:
                        Age = None

                    # Estimated RUL
                    if inputRec[18] == None:
                        EstimatedRUL = None
                    elif is_number(inputRec[18]):
                        EstimatedRUL = int(inputRec[18])
                        #EstimatedRUL = int(float(inputRec[18]))
                    else:
                        EstimatedRUL = None

                    # Replacement Cost
                    if inputRec[19] == None:
                        ReplacementCost = None
                    elif is_number(inputRec[19]):
                        ReplacementCost = float(inputRec[19])
                    else:
                        ReplacementCost = None

                    # Condition Basis
                    if not inputRec[20]:
                        ConditionBasis = None
                    elif str(inputRec[20]) == "" or str(inputRec[20]) == " ":
                        ConditionBasis = None
                    else:
                        ConditionBasis = str(inputRec[20])

                    # Residual Value
                    if inputRec[21] == None:
                        ResidValue = None
                    elif is_number(inputRec[21]):
                        #ResidValue = int(inputRec[21])
                        ResidValue = float(inputRec[21])
                    else:
                        ResidValue = None

                    # Disposal Date
                    #DisposalDate = inputRec[22]
                    # There are no Disposal Dates in spreadsheets - this may
                    # change?
                    DisposalDate = None

                    # Risk
                    if inputRec[23] == None:
                        Risk = None
                    elif is_number(inputRec[23]):
                        Risk = int(inputRec[23])
                    else:
                        Risk = None

                    # Consequences of Failure
                    if inputRec[24] == None:
                        CnsqOfFail = None
                    elif is_number(inputRec[24]):
                        CnsqOfFail = int(inputRec[24])
                    else:
                        CnsqOfFail = None

                    # Follow-up Date
                    #FollowUpDate = inputRec[25]
                    # Should never be Follow-up Dates in spreadsheets
                    FollowUpDate = None

                    # Record Drawing
                    if not inputRec[26]:
                        RecordDrawing = None
                    elif str(inputRec[26]) == "" or str(inputRec[26]) == " ":
                        RecordDrawing = None
                    else:
                        RecordDrawing = str(inputRec[26])

                    # Replacement Year
                    if inputRec[27] == None:
                        ReplacementYear = None
                    elif is_number(inputRec[27]):
                        ReplacementYear = int(float(inputRec[27]))
                    else:
                        ReplacementYear = None

                    # Cost Code (lookup)
                    if not inputRec[28]:
                        CostCode = None
                    elif str(inputRec[28]) == "" or str(inputRec[28]) == " ":
                        CostCode = None
                    else:
                        CostCode = str(inputRec[28])

                    # Cost Factor
                    if inputRec[29] == None:
                        CostFactor = None
                    elif inputRec[29] == 0:
                        CostFactor = None
                    elif str(inputRec[29]) == "" or str(inputRec[29]) == " ":
                        CostFactor = None
                    else:
                        CostFactor = str(int(float(inputRec[29])))

                    # Unit Cost
                    if inputRec[30] == None:
                        UnitCost = None
                    elif is_number(inputRec[30]):
                        if inputRec[30] == 0:
                            UnitCost = None
                        else:
                            UnitCost = float(inputRec[30])
                    else:
                        UnitCost = None

                    # If certain fields aren't filled out with values, then we
                    # need to flag them as Incomplete and set
                    # a default FollowUp Date of 2 weeks from the day of
                    # upload.
                    Complete = "Yes"
                    # for readability
                    fields = [AssetCode, 
                                AssetClass, 
                                AssetSubtype, 
                                FCode, 
                                LocDesc, 
                                Status, 
                                InstallYear,
                                Age, 
                                Condition, 
                                ConditionBasis, 
                                EstimatedRUL, 
                                CostCode, 
                                UnitCost, 
                                ReplacementCost]
                    if shapeType == "Point":
                        if None in fields or Condition == 0:
                            Complete = "No"
                            FollowUpDate = datetime.datetime.now().date() + timedelta(days=14)
                        else:
                            Complete = "Yes"
                            FollowUpDate = None

                    elif shapeType == "Polyline":
                        # Need to check for MeasuredLength as well
                        if None in fields or Condition == 0 or MeasuredLength == 0:
                            Complete = "No"
                            FollowUpDate = datetime.datetime.now().date() + timedelta(days=14)
                        else:
                            Complete = "Yes"
                            FollowUpDate = None


                    # Query the FCode value to see which feature class the
                    # feature should go into
                    outputfc = ""
                    outputtab = ""
                    gdbOwner = "ASSETVIEWER."

                    # Point feature class FCodes
                    if shapeType == "Point":
                        if FCode == "CB":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_Catchbasin")
                        elif FCode == "IO" or FCode == "IO-S":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_InletOutlet")
                        elif FCode == "LIFT":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_LiftStation")
                        elif FCode == "MHST":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_Manhole")
                        elif FCode == "PND":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_Pond")
                        elif FCode == "TRMTD":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_TreatmentDevice")
                        elif FCode == "UGS":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_UndergroundStorage")
                        elif FCode == "STPR":
                            outputfc = set_output_fc(gdb,gdbOwner,"Transportation","TRN_Bridge")
                        elif FCode == "TFSP":
                            outputfc = set_output_fc(gdb,gdbOwner,"Transportation","TRN_Sign")
                        elif FCode == "TFTL":
                            outputfc = set_output_fc(gdb,gdbOwner,"Transportation","TRN_Signal")
                        elif FCode in ("TSIG","UTPO","TFSLOR","TFSL"):
                            outputfc = set_output_fc(gdb,gdbOwner,"Transportation","TRN_Streetlight")
                        elif FCode == "FTTESAN":
                            outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_Fitting")
                        elif FCode == "PMPS":
                            outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_LiftPumpStation")
                        elif FCode == "MHCO" or FCode == "MHSA":
                            outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_Manhole")
                        elif FCode == "SEPT":
                            outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_SepticField")
                        elif FCode == "WWCTF":
                            outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_TreatmentFacility")
                        elif FCode in ("WWCPMP", "WWTFGEN", "WWSPMP"):
                            # Check the contents of the LocDesc field to see
                            # what the related feature is
                            if not LocDesc == None: # If not <Null>
                                if "-WWC-LPS-PMPS-" in LocDesc:
                                    outputtab = gdb + "/" + gdbOwner + "WWC_LiftPumpStation_Assets"
                                elif "-WWC-TRFWW-WWCTF-" in LocDesc:
                                    outputtab = gdb + "/" + gdbOwner + "WWC_TreatmentFacility_Assets"
                                else:
                                    outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_TreatmentFacility")
                            else: #In case LocDesc is empty, put record here:
                                outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_TreatmentFacility")
                        elif FCode in ("WWTFAC", 
                                       "WWBSC", 
                                       "WWBLWR", 
                                       "WWTFBLD",
                                       "WWCCSYS", 
                                       "WWCLCC", 
                                       "WWCLAR", 
                                       "WWCOMP", 
                                       "WWDAFS",
                                       "WWDAFT", 
                                       "WWELECM", 
                                       "WWFFT", 
                                       "WWFLME", 
                                       "WWGDTP",
                                       "WWISV", 
                                       "WWLAB", 
                                       "WWLAG", 
                                       "WWOFS", 
                                       "WWOXDI", 
                                       "WWPADAE", 
                                       "WWPTNK", 
                                       "WWSBRT", 
                                       "WWSCRC", 
                                       "WWSDB",
                                       "WWSCM", 
                                       "WWST",
                                       "WWTLEM"):
                            outputtab = gdb + "/" + gdbOwner + "WWC_TreatmentFacility_Assets"
                        elif FCode == "BST":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_BoosterStation")
                        elif FCode == "CS":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_CorporationStop")
                        elif FCode == "WV":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_CurbStop")
                        elif FCode in ("FTBD11", 
                                       "FTBD22", 
                                       "FTBD45", 
                                       "FTBD90",
                                       "FTCAP", 
                                       "FTCP", 
                                       "FTHY", 
                                       "FTHYTE", 
                                       "FTRD", 
                                       "FTTS",
                                       "FTTE"):
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_Fitting")
                        elif FCode == "HY":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_Hydrant")
                        elif FCode == "METER":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_MeteringSystem")
                        elif FCode == "PRV" or FCode == "APV":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_PRV")
                        elif FCode == "WSST":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_StorageTank")
                        elif FCode == "WSTF":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_TreatmentFacility")
                        elif FCode == "FTVLHY" or FCode == "GV":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_Valve")
                        elif FCode == "WS":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_WaterSource")
                        elif FCode in ("WSTFAC", "WSCPMP", "WSISV", "WSSPMP"):
                            # Check the contents of the LocDesc field to see
                            # what the related feature is
                            if not LocDesc == None: #If not <Null>
                                if "-PWS-BST-BST-" in LocDesc:
                                    outputtab = gdb + "/" + gdbOwner + "PWS_BoosterStation_Assets"
                                elif "-PWS-TRFWS-WSTF-" in LocDesc:
                                    outputtab = gdb + "/" + gdbOwner + "PWS_TreatmentFacility_Assets"
                                else:
                                    outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_TreatmentFacility")
                            else: #In case LocDesc is empty, put record here:
                                outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_TreatmentFacility")
                        elif FCode in ("WSTFBLD", 
                                       "WSCCSYS", 
                                       "WSCLLD",
                                       "WSCLAR", 
                                       "WSCOMP", 
                                       "WSDAFS", 
                                       "WSDAFT", 
                                       "WSELECM",
                                       "WSFLME", 
                                       "WSGDTP", 
                                       "WSTFGEN", 
                                       "WSLAB", 
                                       "WSMFS", 
                                       "WSMMF", 
                                       "WSOFS", 
                                       "WSPTNK", 
                                       "WSSCM", 
                                       "WSTLEM", 
                                       "WSTP",
                                       "WSUV", 
                                       "WSVACCL"):
                            outputtab = gdb + "/" + gdbOwner + "PWS_TreatmentFacility_Assets"
                        else:
                            outputfc = ""
                            outputtab = ""

                    # Polyline feature class FCodes
                    elif shapeType == "Polyline":
                        if FCode == "CLVT" or FCode == "CLVT-S":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_Culvert")
                        elif FCode in ("DRCH", "DRCH-S", "RRGT", "RRGT-S"):
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_DrainageChannel")
                        elif FCode == "GRVPST" or FCode == "GRVPST-S":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_GravityPipe")
                        elif FCode == "SWFRCM" or FCode == "SWFRCM-S":
                            outputfc = set_output_fc(gdb,gdbOwner,"Stormwater","SWC_PressureStormPipe")
                        elif FCode in ("FL", 
                                       "FL-S", 
                                       "STGR", 
                                       "STGR-S", 
                                       "SB",
                                       "SB-S"):
                            outputfc = set_output_fc(gdb,gdbOwner,"Transportation","TRN_BarrierGuardrail")
                        elif FCode in ("RRCB-A", 
                                       "RRCB-A-S", 
                                       "RRCB-C", 
                                       "RRCB-C-S", 
                                       "RRRD-A", 
                                       "RRRD-A-S", 
                                       "RRGR", 
                                       "RRGR-S"):
                            outputfc = set_output_fc(gdb,gdbOwner,"Transportation","TRN_Road")
                        elif FCode in ("RRBW-W", 
                                       "RRBW-W-S", 
                                       "RRDR-A",
                                       "RRDR-A-S", 
                                       "RRPW", 
                                       "RRPW-S", 
                                       "RRSW-C", 
                                       "RRSW-C-S",
                                       "RRSW-A", 
                                       "RRSW-A-S", 
                                       "RRSW-B", 
                                       "RRSW-B-S", 
                                       "RRTR",
                                       "RRTR-S", 
                                       "RRSW", 
                                       "RRSW-S"):
                            outputfc = set_output_fc(gdb,gdbOwner,"Transportation","TRN_SidewalkTrail")
                        elif FCode in ("GRVPSA", "GRVPSA-S", "GRVPCO", "GRVPCO-S"):
                            outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_GravityPipe")
                        elif FCode == "WWFRCM" or FCode == "WWFRCM-S":
                            outputfc = set_output_fc(gdb,gdbOwner,"Wastewater","WWC_PressureSewerPipe")
                        elif FCode == "DIMN" or FCode == "DIMN-S":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_DistributionPipe")
                        elif FCode == "TRNS" or FCode == "TRNS-S":
                            outputfc = set_output_fc(gdb,gdbOwner,"WaterSupply","PWS_TransmissionPipe")
                        else:
                            outputfc = ""
                            outputtab = ""
                    # Insert a feature into an output fc or record into an
                    # output table
                    if outputfc != "":
                        if shapeType == "Point":
                            with arcpy.da.InsertCursor(outputfc, outputFields_Point) as outputCursor:
                                # Insert the feature
                                outputCursor.insertRow([shp, AssetCode, MunID,
                                AssetClass, AssetSubtype, FCode, LocDesc,
                                Elev, Status, Material, CostFactor, Width,
                                InstallYear, Age, Condition, ConditionBasis,
                                InspectDate, EstimatedRUL, ReplacementYear,
                                CostCode, UnitCost, ReplacementCost,
                                ResidValue, DisposalDate, CnsqOfFail, Risk,
                                RecordDrawing, Region, Dept, Division,
                                PersResp, FollowUpDate, Comments, Complete])

                        elif shapeType == "Polyline":
                            with arcpy.da.InsertCursor(outputfc, outputFields_Line) as outputCursor:
                                # Insert the feature
                                outputCursor.insertRow([shp, AssetCode, MunID,
                                AssetClass, AssetSubtype, FCode, LocDesc,
                                Status, Material, CostFactor, Width,
                                MeasuredLength, InstallYear, Age, Condition,
                                ConditionBasis, InspectDate, EstimatedRUL,
                                ReplacementYear, CostCode, UnitCost,
                                ReplacementCost, ResidValue, DisposalDate,
                                CnsqOfFail, Risk, RecordDrawing, Region, Dept,
                                Division, PersResp, FollowUpDate, Comments,
                                Complete])

                    if outputtab != "":
                        tab_fields = [AssetCode, MunID,
                                AssetClass, AssetSubtype, FCode, LocDesc,
                                Status, Material, CostFactor, Width,
                                InstallYear, Age, Condition, ConditionBasis,
                                InspectDate, EstimatedRUL, ReplacementYear,
                                CostCode, UnitCost, ReplacementCost,
                                ResidValue, DisposalDate, CnsqOfFail, Risk,
                                RecordDrawing, Region, Dept, Division,
                                PersResp, FollowUpDate, Comments, LocDesc,
                                Complete]
                        if outputtab == gdb + "/" + gdbOwner + "PWS_BoosterStation_Assets":
                            with arcpy.da.InsertCursor(outputtab, outputFields_Table_BST) as outputCursor:
                                # Insert the record (no geometry)
                                outputCursor.insertRow(tab_fields)

                        elif outputtab == gdb + "/" + gdbOwner + "PWS_TreatmentFacility_Assets":
                            with arcpy.da.InsertCursor(outputtab, outputFields_Table_WSTF) as outputCursor:
                                # Insert the record (no geometry)
                                outputCursor.insertRow(tab_fields)

                        elif outputtab == gdb + "/" + gdbOwner + "WWC_LiftPumpStation_Assets":
                            with arcpy.da.InsertCursor(outputtab, outputFields_Table_LPS) as outputCursor:
                                # Insert the record (no geometry)
                                outputCursor.insertRow(tab_fields)

                        elif outputtab == gdb + "/" + gdbOwner + "WWC_TreatmentFacility_Assets":
                            with arcpy.da.InsertCursor(outputtab, outputFields_Table_WWCTF) as outputCursor:
                                # Insert the record (no geometry)
                                outputCursor.insertRow(tab_fields)
                    counter += 1
            # Add counter to totalcounter
            totalcounter = totalcounter + counter
            # Stop the edit operation
            edit.stopOperation()
            # Clean up ??
            arcpy.RemoveJoin_management(fcJoin)
            del outputCursor
            del counter
            del shapeType
            del inputFields
        # Use this to save ?  so that it can be displayed in Dashboard
        arcpy.AddMessage("Total records processed and uploaded: " + str(totalcounter))

        # Stop the edit session and save the changes
        edit.stopEditing(True)

        # Import the UnitCost sheet into the UnitCost table for the
        # municipality
        # Have to get actual spreadsheet for the UnitCost information, convert
        # to a CSV, then to a DBF and then load into UnitCost table

        # Find spreadsheet and the Unit Cost sheet, export to a CSV in the
        # municipality folder
        for file in os.listdir(munFolder):
            if file.endswith(".xlsm") and file.startswith(munID):
                fileSpreadsheet = munFolder + file
                break
        wb = xlrd.open_workbook(fileSpreadsheet)
        sheet = wb.sheet_by_name("Unit Cost")
        csvUnitCost = open(munFolder + "UnitCost.csv", "wb")
        wr = csv.writer(csvUnitCost, quoting=csv.QUOTE_ALL)
        # Need to write header manually since sheet has merged rows and won't
        # export perfectly
        wr.writerow(("Field1",
            "Item",
             "Lookup Code",
             "Cost Factor",
             "Life",
             "Unit",
             "Base Cost",
             "Field2",
             "Total Cost",
             "Field4",
             "Field5",
             "Field6",
             "Field7",
             "Field8",
             "Field9",
             "Field10",
             "Field11"))
        # Write remaining rows with data
        for rownum in xrange(sheet.nrows):
            # Skip the first two rows
            if rownum == 0 or rownum == 1:
                continue
            # Write other row values to CSV
            wr.writerow(sheet.row_values(rownum))
        # Close the spreadsheet and CSV
        wb.release_resources()
        del wb
        csvUnitCost.close()
        # The sheet/CSV has too many empty or unneeded columns, so will only
        # take ones we need
        # Need to export to a new CSV in the municipality folder
        # global munName
        f = pd.read_csv(munFolder + "UnitCost.csv")
        keep_col = ["Item", "Lookup Code", "Cost Factor", "Life", "Unit", "Base Cost", "Total Cost"]
        new_f = f[keep_col]
        new_f.to_csv(munFolder + "UnitCost_" + munID + ".csv", index=False)
        # Will create a temporary DBF in the municipality folder
        dbfFile = munFolder + "UnitCost_" + munID + ".dbf"
        # Delete if already there
        if os.path.isfile(dbfFile):
            os.remove(dbfFile)
        # Might also be a dbf.xml file
        if os.path.isfile(munFolder + "UnitCost_" + munID + ".dbf.xml"):
            os.remove(munFolder + "UnitCost_" + munID + ".dbf.xml")
        # Convert CSV to DBF
        arcpy.TableToTable_conversion(munFolder + "UnitCost_" + munID + ".csv", munFolder, "UnitCost_" + munID + ".dbf")
        # Truncate UnitCost table in the GDB before loading new data in
        arcpy.env.workspace = gdb
        # Get corresponding UnitCost table for the municipality from the GDB
        unitCostTab = gdbOwner + "UnitCost_" + munID
        arcpy.TruncateTable_management(unitCostTab)
        # Start editing - without an undo/redo stack
        edit.startEditing(False, False)
        # Start another edit operation on GDB
        edit.startOperation()
        # Input fields from DBF and output GDB fields
        inputDBFFields = ["Item", "Lookup_Cod", "Cost_Facto", "Life", "Unit", "Base_Cost", "Total_Cost"]
        outputGDBFields = ["ItemDesc", "CostCode", "CostFactor", "UsefulLife", "Unit", "BaseCost", "TotalCost"]
        # Initialize counter (might not need this)
        unitCostCounter = 0
        # Cursor through input dbf
        with arcpy.da.SearchCursor(munFolder + "UnitCost_" + munID + ".dbf", inputDBFFields) as inputDBFCursor:
            # Write values to output feature class
            for inputDBFRec in inputDBFCursor:
                # To get rid of the rows with blank values at the end of
                # CSV / DBF - skip over these
                if inputDBFRec[0] == " ":
                    continue
                else:
                    # Item
                    Item = inputDBFRec[0]
                    # Cost Code (Lookup Code)
                    if(empty_string(inputDBFRec[1])):
                        CostCode = None
                    else:
                        CostCode = inputDBFRec[1]
                    # Cost Factor
                    if empty_string(inputDBFRec[2]):
                        CostFactor = None
                    else:
                        if is_number(inputDBFRec[2]):
                            CostFactor = float(inputDBFRec[2])
                            CostFactor = int(CostFactor)
                        else:
                            CostFactor = inputDBFRec[2]
                    # Useful Life
                    if empty_string(str(inputDBFRec[3])):
                        UsefulLife = None
                    else:
                        if is_number(inputDBFRec[3]):
                            UsefulLife = int(inputDBFRec[3])
                        else:
                            UsefulLife = None
                    # Unit
                    if empty_string(inputDBFRec[4]):
                        Unit = None
                    else:
                        Unit = inputDBFRec[4]
                    # Base Cost
                    if empty_string(str(inputDBFRec[5])):
                        BaseCost = None
                    else:
                        BaseCost = inputDBFRec[5]
                    # Total Cost
                    if empty_string(str(inputDBFRec[6])):
                        TotalCost = None
                    else:
                        TotalCost = inputDBFRec[6]
                    # Write values to UnitCost table in GDB
                    with arcpy.da.InsertCursor(unitCostTab, outputGDBFields) as unitCostCursor:
                        # Insert the record
                        unitCostCursor.insertRow([Item, CostCode, CostFactor, UsefulLife, Unit, BaseCost, TotalCost])
                        # Update counter
                        unitCostCounter += 1
        # Stop the edit operation
        edit.stopOperation()
        # Stop the edit session and save the changes
        edit.stopEditing(True)
        # Clean up
        del unitCostCursor
        del unitCostTab
        del outputGDBFields
        del unitCostCounter
        # Status
        UploadStatus = "Upload Successful"
        # Send email
        NotifyClient(munFullName, "", "", UploadStatus)
    except arcpy.ExecuteError:
        arcpy.AddMessage(arcpy.GetMessages(2))
        UploadStatus = "Upload Failed: " + "\n" + arcpy.GetMessages(2)
        # Abort edit operation
        if "edit" in locals() or "edit" in globals():
            if edit.isEditing == "true":
                edit.abortOperation()
                # Stop the edit session without saving any changes
                edit.stopEditing(False)
        # Send email
        NotifyClient(munFullName, "", "", UploadStatus)
    except Exception, e:
        UploadStatus = "ERROR: Exception on line number:" + str(sys.exc_traceback.tb_lineno) + "\n" + str(e) + "\n"
        NotifyClient(munFullName, "", "", UploadStatus)
        # Abort edit operation
        if "edit" in locals() or "edit" in globals():
            if edit.isEditing == "true":
                edit.abortOperation()
                # Stop the edit session without saving any changes
                edit.stopEditing(False)

def NotifyClient(munFullName, errorFilenameShort, errorFilename, UploadStatus):
    arcpy.AddMessage("Sending email...")
    # Get the email parameter
    email = arcpy.GetParameterAsText(2)
    # From email address
    fromaddr = "noreply@gov.ns.ca"
    toaddr = email
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = munFullName + ": Infrastructure Registry for Municipal Assets Upload Tool"
    # Attach csv error file if there were validation errors
    if UploadStatus == "Upload Successful":
        body = "Upload Status: " + UploadStatus + "\n\n" + "Total records processed and uploaded: " + str(totalcounter) + "\n" + "Your data will refresh as soon as you zoom or pan around in the map."
        msg.attach(MIMEText(body, "plain"))
    elif UploadStatus == "Validation Failed":
        body = "Upload Status: " + UploadStatus + "\n" + "See attached error log file."
        msg.attach(MIMEText(body, "plain"))
        filename = errorFilenameShort
        attachment = open(errorFilename, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename = %s" % filename)
        msg.attach(part)
    elif "Cannot acquire a lock" in UploadStatus:
        body = "Upload Status: Upload Failed." + "\n" + "The database is currently in use by another user or process." + "\n"
        msg.attach(MIMEText(body, "plain"))
    else:
        body = "Upload Status: " + UploadStatus + "\n"
        msg.attach(MIMEText(body, "plain"))
    # Email server for government
    server = smtplib.SMTP("mail.gov.ns.ca", 25)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

if __name__ == '__main__':
    main()