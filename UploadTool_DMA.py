## ###################################################################################
##         Client : NS Department of Municipal Affairs
##        Purpose : Infrastructure Registry for Municipal Assets Upload Tool
##         Author : Bluejack Consulting Inc.
##  Last modified : 03/09/2018
## Python Version : 2.7
## #####################################################################################

#import os
#import sys
#import glob
#import shutil
#import string
#import numbers
#import datetime
#from datetime import timedelta
#import copy
#import shutil
#import arcpy
#import xlrd
#import csv
#import pandas as pd
#import time
#import smtplib
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText
#from email.MIMEBase import MIMEBase
#from email import encoders
#import zipfile


## Script name
#scriptName = "UploadTool_DMA.py"


## Start Time...
#starttime = datetime.datetime.now()

##region Municipality codes
## Municipality Codes
## These are the Municipality codes that exist in the spreadsheets and geodatabase,
## but there are remnants of the old IDs in the names of the shapefiles

##CB = "Cape Breton Regional Municipality"
##HX = "Halifax Regional Municipality"
##FN = "First Nations"

##AP = "County of Annapolis"
##AT = "County of Antigonish"
##CO = "County of Colchester"
##CU = "County of Cumberland"
##IN = "County of Inverness"
##KI = "County of Kings"
##PI = "County of Pictou"
##RI = "County of Richmond"
##VI = "County of Victoria"

##AY = "District of Argyle"
##BA = "District of Barrington"
##CT = "District of Chester"
##CL = "District of Clare"
##DI = "District of Digby"
##EH = "District of East Hants"
##GU = "District of Guysborough"
##LU = "District of Lunenburg"
##SH = "District of Shelburne"
##SM = "District of St. Mary's"
##WH = "District of West Hants"
##YA = "District of Yarmouth"

##QU = "Region of Queens"

##AM = "Town of Amherst"
##AR = "Town of Annapolis Royal"
##AS = "Town of Antigonish"
##BE = "Town of Berwick"
##BT = "Town of Bridgetown"
##BW = "Town of Bridgewater"
##CA = "Town of Canso"
##CH = "Town of Clark's Harbour"
##DG = "Town of Digby"
##HP = "Town of Hantsport"
##KE = "Town of Kentville"
##LO = "Town of Lockeport"
##LN = "Town of Lunenburg"
##MB = "Town of Mahone Bay"
##MI = "Town of Middleton"
##MU = "Town of Mulgrave"
##NG = "Town of New Glasgow"
##OX = "Town of Oxford"
##PA = "Town of Parrsboro"
##PC = "Town of Pictou"
##PH = "Town of Port Hawkesbury"
##SB = "Town of Shelburne"
##SP = "Town of Springhill"
##SL = "Town of Stellarton"
##SW = "Town of Stewiacke"
##TN = "Town of Trenton"
##TU = "Town of Truro"
##WE = "Town of Westville"
##WI = "Town of Windsor"
##WO = "Town of Wolfville"
##YM = "Town of Yarmouth"

##VAY = "Village of Aylesford"
##VBD = "Village of Baddeck"
##VBH = "Village of Bible Hill"
##VCN = "Village of Canning"
##VCH = "Village of Chester"
##VCS = "Village of Cornwallis Square"
##VFP = "Village of Freeport"
##VGW = "Village of Greenwood"
##VHB = "Village of Havre Boucher"
##VHE = "Village of Hebbville"
##VKI = "Village of Kingston"
##VLW = "Village of Lawrencetown"
##VNM = "Village of New Minas"
##VPW = "Village of Port Williams"
##VPG = "Village of Pugwash"
##VRH = "Village of River Hebert"
##VSP = "Village of St. Peter's"
##VTM = "Village of Tatamagouche"
##VTI = "Village of Tiverton"
##VWP = "Village of Westport"
##VWM = "Village of Weymouth"
##endregion


## Coordinate system of pilot municipality shapefiles (NAD83 UTM20)
#srNAD83_UTM20 = arcpy.SpatialReference(26920)
## Coordinate system of GDB feature classes (NAD83 CSRS UTM20)
#srNAD83_CSRS_UTM20 = arcpy.SpatialReference(2961)
## Datum transformation between the two
#gt = "NAD_1983_To_WGS_1984_1 + NAD_1983_CSRS_To_WGS_1984_2"


## Initialize variable
#edit = None


outputFields_Point = app_utilities.get_array('point_feature_fields.json')['outputFields_Point']
outputFields_Line = app_utilities.get_array('line_feature_fields.json')['outputFields_Line']
outputFields_Table_WWCTF = app_utilities.get_array('waste_water_treatment_facility.json')['outputFields_Table_WWCTF']
outputFields_Table_LPS = app_utilities.get_array('waste_water_lift_pump_station.json')['outputFields_Table_LPS']
outputFields_Table_BST = app_utilities.get_array('water_supply_booster_station.json')['outputFields_Table_BST']
outputFields_Table_WSTF = app_utilities.get_array('water_supply_treatment_facility.json')['outputFields_Table_WSTF']




#def main():

#    Unzip()
#    Validate()
#    #Upload()


#def is_number(n):
#    try:
#        float(n)   # Type-casting the string to 'float'.
#                   # If string is not a valid 'float,
#                   # it'll raise 'ValueError' exception
#    except ValueError:
#        return False
#    return True


#def rmdirContents(folder):
#    for root, dirs, files in os.walk(folder):
#        for f in files:
#            os.unlink(os.path.join(root, f))
#        for d in dirs:
#            shutil.rmtree(os.path.join(root, d))


#def Unzip():
#    # Get the zip file parameter
#    global munZipfile, zip_ref
#    munZipfile = arcpy.GetParameterAsText(3)


#def Validate():

#    try:
#        #global parentFolder, munFolder, munID, shpMunID, munName, mun
#        global munFolder, munID, shpMunID, munName, mun, munFullName
#        global method, shapefilesExist, gdb

#        # Default value
#        shapefilesExist = True

#        # Get 2 of the parameters
#        mun = arcpy.GetParameterAsText(0)
#        method = arcpy.GetParameterAsText(1)
#        #parentFolder = arcpy.GetParameterAsText(2) + "/"
#        #gdb = arcpy.GetParameterAsText(3) + "/"


#        # Set different variables according to what the input method is
#        if method == "GIS":
#            shapefilesExist = True
#        elif method == "Survey":
#            shapefilesExist = False


#        # ===============================================================================
#        # ===============================================================================
#        # ===============================================================================
#        # Hard-coded parent folder - on the VM
#        #parentFolder = "C:/Projects/DMA/UploadTool/Uploads/"
#        # On my machine
#        #parentFolder = "C:/Work/Projects/DMA/UploadTool/Uploads/"

#        arcpy.env.scratchWorkspace  = '%scratchworkspace%'

#        # ===============================================================================
#        # ===============================================================================
#        # =======================================================================



#        # Defaults
#        munFolder = ""
#        munID = ""
#        shpMunID = ""


#        # The folder names on the server that store the whole structure of files (what's in the zip file)
#        # need to be called these following names and paths:

#        # Get municipality folder, name and IDs from mun variable
#        # Set variables accordingly
#current_municipality = app_utilities.get_object_dictionary('municipalities.json')[mun]
#munFolder = current_municipality.munFolder

#        if mun == "CB":
#            munFolder = arcpy.env.scratchFolder + "/CapeBreton/"
#            munName = "CapeBreton"
#            munFullName = "Cape Breton Regional Municipality"
#            munID = "CB"
#            shpMunID = "CB"
#        elif mun == "HX":
#            munFolder = arcpy.env.scratchFolder + "/Halifax/"
#            munName = "Halifax"
#            munFullName = "Halifax Regional Municipality"
#            munID = "HX"
#            shpMunID = "HX"
#        elif mun == "FN":
#            munFolder = arcpy.env.scratchFolder + "/FirstNations/"
#            munName = "FirstNations"
#            munFullName = "First Nations"
#            munID = "FN"
#            shpMunID = "FN"
#        elif mun == "AP":
#            munFolder = arcpy.env.scratchFolder + "/CountyAnnapolis/"
#            munName = "CountyAnnapolis"
#            munFullName = "County of Annapolis"
#            munID = "AP"
#            shpMunID = "AP"
#        elif mun == "AT":
#            munFolder = arcpy.env.scratchFolder + "/CountyAntigonish/"
#            munName = "CountyAntigonish"
#            munFullName = "County of Antigonish"
#            munID = "AT"
#            shpMunID = "AT"
#        elif mun == "CO":
#            munFolder = arcpy.env.scratchFolder + "/CountyColchester/"
#            munName = "CountyColchester"
#            munFullName = "County of Colchester"
#            munID = "CO"
#            shpMunID = "CO"
#        elif mun == "CU":
#            munFolder = arcpy.env.scratchFolder + "/CountyCumberland/"
#            munName = "CountyCumberland"
#            munFullName = "County of Cumberland"
#            munID = "CU"
#            shpMunID = "CU"
#        elif mun == "IN":
#            munFolder = arcpy.env.scratchFolder + "/CountyInverness/"
#            munName = "CountyInverness"
#            munFullName = "County of Inverness"
#            munID = "IN"
#            shpMunID = "IN"
#        elif mun == "KI":
#            munFolder = arcpy.env.scratchFolder + "/CountyKings/"
#            munName = "CountyKings"
#            munFullName = "County of Kings"
#            munID = "KI"
#            shpMunID = "KI"
#        elif mun == "PI":
#            munFolder = arcpy.env.scratchFolder + "/CountyPictou/"
#            munName = "CountyPictou"
#            munFullName = "County of Pictou"
#            munID = "PI"
#            shpMunID = "PI"
#        elif mun == "RI":
#            munFolder = arcpy.env.scratchFolder + "/CountyRichmond/"
#            munName = "CountyRichmond"
#            munFullName = "County of Richmond"
#            munID = "RI"
#            shpMunID = "RI"
#        elif mun == "VI":
#            munFolder = arcpy.env.scratchFolder + "/CountyVictoria/"
#            munName = "CountyVictoria"
#            munFullName = "County of Victoria"
#            munID = "VI"
#            shpMunID = "VI"
#        elif mun == "AY":
#            munFolder = arcpy.env.scratchFolder + "/DistrictArgyle/"
#            munName = "DistrictArgyle"
#            munFullName = "District of Argyle"
#            munID = "AY"  # New IDs
#            shpMunID = "ARG"  # Shapefiles have old IDs
#        elif mun == "BA":
#            munFolder = arcpy.env.scratchFolder + "/DistrictBarrington/"
#            munName = "DistrictBarrington"
#            munFullName = "District of Barrington"
#            munID = "BA"
#            shpMunID = "BA"
#        elif mun == "CT":
#            munFolder = arcpy.env.scratchFolder + "/DistrictChester/"
#            munName = "DistrictChester"
#            munFullName = "District of Chester"
#            munID = "CT"
#            shpMunID = "CT"
#        elif mun == "CL":
#            munFolder = arcpy.env.scratchFolder + "/DistrictClare/"
#            munName = "DistrictClare"
#            munFullName = "District of Clare"
#            munID = "CL"
#            shpMunID = "CL"
#        elif mun == "DI":
#            munFolder = arcpy.env.scratchFolder + "/DistrictDigby/"
#            munName = "DistrictDigby"
#            munFullName = "District of Digby"
#            munID = "DI"
#            shpMunID = "DI"
#        elif mun == "EH":
#            munFolder = arcpy.env.scratchFolder + "/DistrictEastHants/"
#            munName = "DistrictEastHants"
#            munFullName = "District of East Hants"
#            munID = "EH"
#            shpMunID = "EH"
#        elif mun == "GU":
#            munFolder = arcpy.env.scratchFolder + "/DistrictGuysborough/"
#            munName = "DistrictGuysborough"
#            munFullName = "District of Guysborough"
#            munID = "GU"
#            shpMunID = "GU"
#        elif mun == "LU":
#            munFolder = arcpy.env.scratchFolder + "/DistrictLunenburg/"
#            munName = "DistrictLunenburg"
#            munFullName = "District of Lunenburg"
#            munID = "LU"
#            shpMunID = "LU"
#        elif mun == "SH":
#            munFolder = arcpy.env.scratchFolder + "/DistrictShelburne/"
#            munName = "DistrictShelburne"
#            munFullName = "District of Shelburne"
#            munID = "SH"
#            shpMunID = "SH"
#        elif mun == "SM":
#            munFolder = arcpy.env.scratchFolder + "/DistrictStMarys/"
#            munName = "DistrictStMarys"
#            munFullName = "District of St. Mary's"
#            munID = "SM"
#            shpMunID = "SM"
#        elif mun == "WH":
#            munFolder = arcpy.env.scratchFolder + "/DistrictWestHants/"
#            munName = "DistrictWestHants"
#            munFullName = "District of West Hants"
#            munID = "WH"
#            shpMunID = "WH"
#        elif mun == "YA":
#            munFolder = arcpy.env.scratchFolder + "/DistrictYarmouth/"
#            munName = "DistrictYarmouth"
#            munFullName = "District of Yarmouth"
#            munID = "YA"
#            shpMunID = "YA"
#        elif mun == "QU":
#            munFolder = arcpy.env.scratchFolder + "/RegionQueens/"
#            munName = "RegionQueens"
#            munFullName = "Region of Queens"
#            munID = "QU"
#            shpMunID = "QU"
#        elif mun == "AM":
#            munFolder = arcpy.env.scratchFolder + "/TownAmherst/"
#            munName = "TownAmherst"
#            munFullName = "Town of Amherst"
#            munID = "AM"
#            shpMunID = "AM"
#        elif mun == "AR":
#            munFolder = arcpy.env.scratchFolder + "/TownAnnapolisRoyal/"
#            munName = "TownAnnapolisRoyal"
#            munFullName = "Town of Annapolis Royal"
#            munID = "AR"
#            shpMunID = "AR"
#        elif mun == "AS":
#            munFolder = arcpy.env.scratchFolder + "/TownAntigonish/"
#            munName = "TownAntigonish"
#            munFullName = "Town of Antigonish"
#            munID = "AS"
#            shpMunID = "AS"
#        elif mun == "BE":
#            munFolder = arcpy.env.scratchFolder + "/TownBerwick/"
#            munName = "TownBerwick"
#            munFullName = "Town of Berwick"
#            munID = "BE"
#            shpMunID = "BE"
#        elif mun == "BT":
#            munFolder = arcpy.env.scratchFolder + "/TownBridgetown/"
#            munName = "TownBridgetown"
#            munFullName = "Town of Bridgetown"
#            munID = "BT"
#            shpMunID = "BT"
#        elif mun == "BW":
#            munFolder = arcpy.env.scratchFolder + "/TownBridgewater/"
#            munName = "TownBridgewater"
#            munFullName = "Town of Bridgewater"
#            munID = "BW"
#            shpMunID = "BW"
#        elif mun == "CA":
#            munFolder = arcpy.env.scratchFolder + "/TownCanso/"
#            munName = "TownCanso"
#            munFullName = "Town of Canso"
#            munID = "CA"
#            shpMunID = "CA"
#        elif mun == "CH":
#            munFolder = arcpy.env.scratchFolder + "/TownClarksHarbour/"
#            munName = "TownClarksHarbour"
#            munFullName = "Town of Clark's Harbour"
#            munID = "CH"
#            shpMunID = "CH"
#        elif mun == "DG":
#            munFolder = arcpy.env.scratchFolder + "/TownDigby/"
#            munName = "TownDigby"
#            munFullName = "Town of Digby"
#            munID = "DG"
#            shpMunID = "DG"
#        elif mun == "HP":
#            munFolder = arcpy.env.scratchFolder + "/TownHantsport/"
#            munName = "TownHantsport"
#            munFullName = "Town of Hantsport"
#            munID = "HP"
#            shpMunID = "HP"
#        elif mun == "KE":
#            munFolder = arcpy.env.scratchFolder + "/TownKentville/"
#            munName = "TownKentville"
#            munFullName = "Town of Kentville"
#            munID = "KE"
#            shpMunID = "KE"
#        elif mun == "LO":
#            munFolder = arcpy.env.scratchFolder + "/TownLockeport/"
#            munName = "TownLockeport"
#            munFullName = "Town of Lockeport"
#            munID = "LO"
#            shpMunID = "LKP"
#        elif mun == "LN":
#            munFolder = arcpy.env.scratchFolder + "/TownLunenburg/"
#            munName = "TownLunenburg"
#            munFullName = "Town of Lunenburg"
#            munID = "LN"
#            shpMunID = "LN"
#        elif mun == "MB":
#            munFolder = arcpy.env.scratchFolder + "/TownMahoneBay/"
#            munName = "TownMahoneBay"
#            munFullName = "Town of Mahone Bay"
#            munID = "MB"
#            shpMunID = "MHB"
#        elif mun == "MI":
#            munFolder = arcpy.env.scratchFolder + "/TownMiddleton/"
#            munName = "TownMiddleton"
#            munFullName = "Town of Middleton"
#            munID = "MI"
#            shpMunID = "MI"
#        elif mun == "MU":
#            munFolder = arcpy.env.scratchFolder + "/TownMulgrave/"
#            munName = "TownMulgrave"
#            munFullName = "Town of Mulgrave"
#            munID = "MU"
#            shpMunID = "MU"
#        elif mun == "NG":
#            munFolder = arcpy.env.scratchFolder + "/TownNewGlasgow/"
#            munName = "TownNewGlasgow"
#            munFullName = "Town of New Glasgow"
#            munID = "NG"
#            shpMunID = "NG"
#        elif mun == "OX":
#            munFolder = arcpy.env.scratchFolder + "/TownOxford/"
#            munName = "TownOxford"
#            munFullName = "Town of Oxford"
#            munID = "OX"
#            shpMunID = "OX"
#        elif mun == "PA":
#            munFolder = arcpy.env.scratchFolder + "/TownParrsboro/"
#            munName = "TownParrsboro"
#            munFullName = "Town of Parrsboro"
#            munID = "PA"
#            shpMunID = "PA"
#        elif mun == "PC":
#            munFolder = arcpy.env.scratchFolder + "/TownPictou/"
#            munName = "TownPictou"
#            munFullName = "Town of Pictou"
#            munID = "PC"
#            shpMunID = "PC"
#        elif mun == "PH":
#            munFolder = arcpy.env.scratchFolder + "/TownPortHawkesbury/"
#            munName = "TownPortHawkesbury"
#            munFullName = "Town of Port Hawkesbury"
#            munID = "PH"
#            shpMunID = "PHK"
#        elif mun == "SB":
#            munFolder = arcpy.env.scratchFolder + "/TownShelburne/"
#            munName = "TownShelburne"
#            munFullName = "Town of Shelburne"
#            munID = "SB"
#            shpMunID = "SHL"
#        elif mun == "SP":
#            munFolder = arcpy.env.scratchFolder + "/TownSpringhill/"
#            munName = "TownSpringhill"
#            munFullName = "Town of Springhill"
#            munID = "SP"
#            shpMunID = "SP"
#        elif mun == "SL":
#            munFolder = arcpy.env.scratchFolder + "/TownStellarton/"
#            munName = "TownStellarton"
#            munFullName = "Town of Stellarton"
#            munID = "SL"
#            shpMunID = "SL"
#        elif mun == "SW":
#            munFolder = arcpy.env.scratchFolder + "/TownStewiacke/"
#            munName = "TownStewiacke"
#            munFullName = "Town of Stewiacke"
#            munID = "SW"
#            shpMunID = "SW"
#        elif mun == "TN":
#            munFolder = arcpy.env.scratchFolder + "/TownTrenton/"
#            munName = "TownTrenton"
#            munFullName = "Town of Trenton"
#            munID = "TN"
#            shpMunID = "TN"
#        elif mun == "TU":
#            munFolder = arcpy.env.scratchFolder + "/TownTruro/"
#            munName = "TownTruro"
#            munFullName = "Town of Truro"
#            munID = "TU"
#            shpMunID = "TU"
#        elif mun == "WE":
#            munFolder = arcpy.env.scratchFolder + "/TownWestville/"
#            munName = "TownWestville"
#            munFullName = "Town of Westville"
#            munID = "WE"
#            shpMunID = "WE"
#        elif mun == "WI":
#            munFolder = arcpy.env.scratchFolder + "/TownWindsor/"
#            munName = "TownWindsor"
#            munFullName = "Town of Windsor"
#            munID = "WI"
#            shpMunID = "WI"
#        elif mun == "WO":
#            munFolder = arcpy.env.scratchFolder + "/TownWolfville/"
#            munName = "TownWolfville"
#            munFullName = "Town of Wolfville"
#            munID = "WO"
#            shpMunID = "WO"
#        elif mun == "YM":
#            munFolder = arcpy.env.scratchFolder + "/TownYarmouth/"
#            munName = "TownYarmouth"
#            munFullName = "Town of Yarmouth"
#            munID = "YM"
#            shpMunID = "YM"
#        elif mun == "VAY":
#            munFolder = arcpy.env.scratchFolder + "/VillageAylesford/"
#            munName = "VillageAylesford"
#            munFullName = "Village of Aylesford"
#            munID = "VAY"
#            shpMunID = "VAY"
#        elif mun == "VBD":
#            munFolder = arcpy.env.scratchFolder + "/VillageBaddeck/"
#            munName = "VillageBaddeck"
#            munFullName = "Village of Baddeck"
#            munID = "VBD"
#            shpMunID = "VBD"
#        elif mun == "VBH":
#            munFolder = arcpy.env.scratchFolder + "/VillageBibleHill/"
#            munName = "VillageBibleHill"
#            munFullName = "Village of Bible Hill"
#            munID = "VBH"
#            shpMunID = "VBH"
#        elif mun == "VCN":
#            munFolder = arcpy.env.scratchFolder + "/VillageCanning/"
#            munName = "VillageCanning"
#            munFullName = "Village of Canning"
#            munID = "VCN"
#            shpMunID = "VCN"
#        elif mun == "VCH":
#            munFolder = arcpy.env.scratchFolder + "/VillageChester/"
#            munName = "VillageChester"
#            munFullName = "Village of Chester"
#            munID = "VCH"
#            shpMunID = "VCH"
#        elif mun == "VCS":
#            munFolder = arcpy.env.scratchFolder + "/VillageCornwallisSquare/"
#            munName = "VillageCornwallisSquare"
#            munFullName = "Village of Cornwallis Square"
#            munID = "VCS"
#            shpMunID = "VCS"
#        elif mun == "VFP":
#            munFolder = arcpy.env.scratchFolder + "/VillageFreeport/"
#            munName = "VillageFreeport"
#            munFullName = "Village of Freeport"
#            munID = "VFP"
#            shpMunID = "VFP"
#        elif mun == "VGW":
#            munFolder = arcpy.env.scratchFolder + "/VillageGreenwood/"
#            munName = "VillageGreenwood"
#            munFullName = "Village of Greenwood"
#            munID = "VGW"
#            shpMunID = "VGW"
#        elif mun == "VHB":
#            munFolder = arcpy.env.scratchFolder + "/VillageHavreBoucher/"
#            munName = "VillageHavreBoucher"
#            munFullName = "Village of Havre Boucher"
#            munID = "VHB"
#            shpMunID = "VHB"
#        elif mun == "VHE":
#            munFolder = arcpy.env.scratchFolder + "/VillageHebbville/"
#            munName = "VillageHebbville"
#            munFullName = "Village of Hebbville"
#            munID = "VHE"
#            shpMunID = "VHE"
#        elif mun == "VKI":
#            munFolder = arcpy.env.scratchFolder + "/VillageKingston/"
#            munName = "VillageKingston"
#            munFullName = "Village of Kingston"
#            munID = "VKI"
#            shpMunID = "VKI"
#        elif mun == "VLW":
#            munFolder = arcpy.env.scratchFolder + "/VillageLawrencetown/"
#            munName = "VillageLawrencetown"
#            munFullName = "Village of Lawrencetown"
#            munID = "VLW"
#            shpMunID = "VLW"
#        elif mun == "VNM":
#            munFolder = arcpy.env.scratchFolder + "/VillageNewMinas/"
#            munName = "VillageNewMinas"
#            munFullName = "Village of New Minas"
#            munID = "VNM"
#            shpMunID = "VNM"
#        elif mun == "VPW":
#            munFolder = arcpy.env.scratchFolder + "/VillagePortWilliams/"
#            munName = "VillagePortWilliams"
#            munFullName = "Village  of Port Williams"
#            munID = "VPW"
#            shpMunID = "VPW"
#        elif mun == "VPG":
#            munFolder = arcpy.env.scratchFolder + "/VillagePugwash/"
#            munName = "VillagePugwash"
#            munFullName = "Village of Pugwash"
#            munID = "VPG"
#            shpMunID = "VPG"
#        elif mun == "VRH":
#            munFolder = arcpy.env.scratchFolder + "/VillageRiverHebert/"
#            munName = "VillageRiverHebert"
#            munFullName = "Village of River Hebert"
#            munID = "VRH"
#            shpMunID = "VRH"
#        elif mun == "VSP":
#            munFolder = arcpy.env.scratchFolder + "/VillageStPeters/"
#            munName = "VillageStPeters"
#            munFullName = "Village of St. Peter's"
#            munID = "VSP"
#            shpMunID = "VSP"
#        elif mun == "VTM":
#            munFolder = arcpy.env.scratchFolder + "/VillageTatamagouche/"
#            munName = "VillageTatamagouche"
#            munFullName = "Village of Tatamagouche"
#            munID = "VTM"
#            shpMunID = "VTM"
#        elif mun == "VTI":
#            munFolder = arcpy.env.scratchFolder + "/VillageTiverton/"
#            munName = "VillageTiverton"
#            munFullName = "Village of Tiverton"
#            munID = "VTI"
#            shpMunID = "VTI"
#        elif mun == "VWP":
#            munFolder = arcpy.env.scratchFolder + "/VillageWestport/"
#            munName = "VillageWestport"
#            munFullName = "Village of Westport"
#            munID = "VWP"
#            shpMunID = "VWP"
#        elif mun == "VWM":
#            munFolder = arcpy.env.scratchFolder + "/VillageWeymouth/"
#            munName = "VillageWeymouth"
#            munFullName = "Village of Weymouth"
#            munID = "VWM"
#            shpMunID = "VWM"


#        # Unzip the file to the munFolder
#        global munZipfile, zip_ref
#        zip_ref = zipfile.ZipFile(munZipfile, "r")
#        # If munFolder doesn't exist, create it
#        if not os.path.exists(munFolder):
#            os.mkdir(munFolder)
#        # If it does exist, clear out its contents (previous run)
#        else:
#            rmdirContents(munFolder)


#        # Extract to municipality folder
#        zip_ref.extractall(munFolder)
#        zip_ref.close()


#        # Count number of errors
#        errorCounter = 0

#        # Note: The coordinate system of the shapefiles for the pilot municipalities is NAD83 UTM20
#        # The current standard at NSGI is NAD83 CSRS UTM20, and the geodatabase feature classes
#        # will be using the new one. So, the data will be to be projected/transformed before input.
#        # In the future, any new data should be collected in NAD83 CSRS UTMN20 so won't need
#        # projecting/transforming
#        #
#        # Coordinate system of pilot municipality shapefiles (NAD83 UTM20)
#        srNAD83_UTM20 = arcpy.SpatialReference(26920)
#        # Coordinate system of GDB feature classes (NAD83 CSRS UTM20)
#        srNAD83_CSRS_UTM20 = arcpy.SpatialReference(2961)
#        # Datum transformation between the two
#        gt = "NAD_1983_To_WGS_1984_1 + NAD_1983_CSRS_To_WGS_1984_2"



#        # Create CSV file to store file errors
#        # ====================================
###        csvFilenameShort = "UploadTool_FileErrors_" + str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".csv"
###        csvFilename = munFolder + csvFilenameShort
###        csvFileErrors = open(csvFilename, "wb")
###        writeFileErrors = csv.writer(csvFileErrors, quoting=csv.QUOTE_ALL)
###        errorLogFile.write("File", "Issue", "Description"))

#        #global errorFilenameShort, errorFilename
#        dtNow = datetime.datetime.now()
#        errorFilenameShort = "UploadTool_Errors_" + str(dtNow.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
#        errorFilename = munFolder + errorFilenameShort
#        errorLogFile = open(errorFilename, "w")
#        errorLogFile.write("Upload Tool Error Log for " + munFullName + "\n")
#        errorLogFile.write(str(dtNow.strftime("%d %b %Y, %H:%M:%S")) + "\n")
#        errorLogFile.write("---------------------\n\n")


#        # Main Municipality spreadsheet (XLSM)
#        for file in os.listdir(munFolder):
#            if file.endswith(".xlsm") and file.startswith(munID):
#                fileSpreadsheet = munFolder + file
#                existSpreadsheet = True
#                break
#            else:
#                existSpreadsheet = False

#        if existSpreadsheet == False:
#            errorCounter = errorCounter + 1
#            errorLogFile.write(str(errorCounter) + "." + "The " + munFullName + " spreadsheet (.XLSM)" + " cannot be found." + "\n")

#        else:
#            # open the spredasheet and see what the fields are in the General Asset Information sheet
#            wb = xlrd.open_workbook(fileSpreadsheet)
#            sheet = wb.sheet_by_name("GENERAL ASSET INFORMATION")
#            csvGenAssetInfo = open(munFolder + "GenAssetInfo_" + munID + ".csv", "wb")
#            wr = csv.writer(csvGenAssetInfo, quoting=csv.QUOTE_ALL)

#            # Write rows with data (including header row)
#            for rownum in xrange(sheet.nrows):
#                # Skip the first two rows
#                if rownum == 0 or rownum == 1:
#                    continue
#                # Write other row values to CSV
#                wr.writerow(sheet.row_values(rownum))

#            # Close the spreadsheet and CSV
#            wb.release_resources()
#            del wb
#            csvGenAssetInfo.close()


#            # List of all fields that should exist in the spreadsheet (in this order)
#            fieldsGenAssetInfoCSV = []
#            fieldsGenAssetInfoCSV.append("Asset_Code")
#            fieldsGenAssetInfoCSV.append("Descr")
#            fieldsGenAssetInfoCSV.append("LocDesc")
#            fieldsGenAssetInfoCSV.append("FeatureCode")
#            fieldsGenAssetInfoCSV.append("Condition")
#            fieldsGenAssetInfoCSV.append("Inspected")
#            fieldsGenAssetInfoCSV.append("Status")
#            fieldsGenAssetInfoCSV.append("Quantity")
#            fieldsGenAssetInfoCSV.append("Age")
#            fieldsGenAssetInfoCSV.append("Material")
#            fieldsGenAssetInfoCSV.append("Other")
#            fieldsGenAssetInfoCSV.append("Comments")
#            fieldsGenAssetInfoCSV.append("Area")
#            fieldsGenAssetInfoCSV.append("Department")
#            fieldsGenAssetInfoCSV.append("Division")
#            fieldsGenAssetInfoCSV.append("PersResp")
#            fieldsGenAssetInfoCSV.append("Install yr")
#            fieldsGenAssetInfoCSV.append("Useful Life")
#            fieldsGenAssetInfoCSV.append("Estimated RUL")
#            fieldsGenAssetInfoCSV.append("RplmtCst")
#            fieldsGenAssetInfoCSV.append("ConditionBasis")
#            fieldsGenAssetInfoCSV.append("ResidValue")
#            fieldsGenAssetInfoCSV.append("DispDate")
#            fieldsGenAssetInfoCSV.append("Risk")
#            fieldsGenAssetInfoCSV.append("CnsqOfFail")
#            fieldsGenAssetInfoCSV.append("DatLastAss")
#            fieldsGenAssetInfoCSV.append("FollowUp")
#            fieldsGenAssetInfoCSV.append("EditTag")
#            fieldsGenAssetInfoCSV.append("Record Drawing")
#            fieldsGenAssetInfoCSV.append("Replacement Year")
#            fieldsGenAssetInfoCSV.append("CostLookup")
#            fieldsGenAssetInfoCSV.append("Replace1")
#            fieldsGenAssetInfoCSV.append("Replace2")
#            fieldsGenAssetInfoCSV.append(" Replace3")
#            fieldsGenAssetInfoCSV.append(" Replace4")
#            fieldsGenAssetInfoCSV.append("Cost Factor")
#            fieldsGenAssetInfoCSV.append("Unit Cost")
#            fieldsGenAssetInfoCSV.append("Edit Tag")
#            fieldsGenAssetInfoCSV.append("GIS Link")



#            # Check if all the necessary fields are in the spreadsheet CSV file
#            fieldsCSV = []
#            existCSV = True
#            csvGenAssetInfo = open(munFolder + "GenAssetInfo_" + munID + ".csv", "rb")
#            reader = csv.reader(csvGenAssetInfo)
#            i = reader.next()
#            for field in i:
#                fieldsCSV.append(field.strip())
#            for field in fieldsGenAssetInfoCSV:
#                field = field.strip()
#                if field not in fieldsCSV:
#                    if field == "GIS Link":
#                        if shapefilesExist == True:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The " + field + " cannot be found in the " + munFullName + " spreadsheet (.XLSM) file." + "\n\n")
#                    else:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The " + field + " cannot be found in the " + munFullName + " spreadsheet (.XLSM) file." + "\n\n")

#            # Close the spreadsheet CSV
#            csvGenAssetInfo.close()

#            # The sheet/CSV has too many empty or unneeded columns, so will only take ones we need
#            # Need to export to a new CSV in the municipality folder
#            f = pd.read_csv(munFolder + "GenAssetInfo_" + munID + ".csv")
#            if shapefilesExist == False:
#                keep_col = ["Asset_Code","Descr","LocDesc","FeatureCode","Condition","Inspected","Status","Quantity","Age","Material","Other","Comments","Area","Department","Division","PersResp","Install yr","Useful Life","Estimated RUL","RplmtCst","ConditionBasis","ResidValue","DispDate","Risk","CnsqOfFail","DatLastAss","FollowUp","EditTag","Record Drawing","Replacement Year","CostLookup","Replace1","Replace2"," Replace3"," Replace4","Cost Factor","Unit Cost","Edit Tag"]
#            else:
#                keep_col = ["Asset_Code","Descr","LocDesc","FeatureCode","Condition","Inspected","Status","Quantity","Age","Material","Other","Comments","Area","Department","Division","PersResp","Install yr","Useful Life","Estimated RUL","RplmtCst","ConditionBasis","ResidValue","DispDate","Risk","CnsqOfFail","DatLastAss","FollowUp","EditTag","Record Drawing","Replacement Year","CostLookup","Replace1","Replace2"," Replace3"," Replace4","Cost Factor","Unit Cost","Edit Tag","GIS Link"]
#            new_f = f[keep_col]
#            new_f.to_csv(munFolder + "GenAssetInfo.csv", index=False)

#            # Will create a DBF in the municipality folder
#            dbfGenAssetInfo = munFolder + "GenAssetInfo.dbf"
#            # Convert CSV to DBF
#            arcpy.TableToTable_conversion(munFolder + "GenAssetInfo.csv", munFolder, "GenAssetInfo.dbf")



#            # Check the content of the CSV file for data errors
#            # =================================================
#            # Check every FCode values against this full list
#            # Added WWST May 06, 2019 - forgot to add it before
#            fcodes = ["APV", "BST", "CB", "CLVT", "CLVT-S", "CS", "DIMN", "DIMN-S", "DRCH", "DRCH-S", \
#                      "FL", "FL-S", "FTBD11", "FTBD22", "FTBD45", "FTBD90", "FTCAP", "FTCP", "FTHY", "FTHYTE", "FTRD", "FTTS", "FTTE", "FTTESAN", "FTVLHY", \
#                      "GRVPCO", "GRVPCO-S", "GRVPSA", "GRVPSA-S", "GRVPST", "GRVPST-S", "GV", "HY", "IO", "IO-S", "LIFT", \
#                      "METER", "MHCO", "MHSA", "MHST", "PMPS", "PND", "PRV", \
#                      "RRCB-A", "RRCB-A-S", "RRCB-C", "RRCB-C-S", "RRRD-A", "RRRD-A-S", "RRGR", "RRGR-S", "RRBW-W", \
#                      "RRBW-W-S", "RRDR-A", "RRDR-A-S", "RRGT", "RRGT-S", "RRPW", "RRPW-S", "RRSW", "RRSW-S", "RRSW-C", \
#                      "RRSW-C-S", "RRSW-A", "RRSW-A-S", "RRSW-B", "RRSW-B-S", "RRTR", "RRTR-S", \
#                      "SB", "SB-S", "SEPT", "STGR", "STGR-S", "STPR", "SWFRCM", "SWFRCM-S", \
#                      "TFSLOR", "TFSL", "TFSP", "TFTL", "TRMTD", "TRNS", "TRNS-S", "TSIG", "UGS", "UTPO", \
#                      "WS", "WSST", "WSTF", "WSTFAC", "WSTFBLD", "WSCCSYS", "WSCLLD", "WSCLAR", "WSCOMP", "WSCPMP", "WSDAFS", "WSDAFT", "WSELECM", "WSFLME", "WSGDTP", \
#                      "WSTFGEN", "WSISV", "WSLAB", "WSMFS", "WSMMF", "WSOFS", "WSPTNK", "WSSCM", "WSSPMP", "WSTLEM", "WSTP", "WSUV", "WSVACCL", \
#                      "WV", "WWCTF", "WWTFAC", "WWBSC", "WWBLWR", "WWTFBLD", "WWCCSYS", "WWCLCC", "WWCLAR", "WWCOMP", "WWCPMP", "WWDAFS", "WWDAFT", "WWELECM", \
#                      "WWFFT", "WWFLME", "WWGDTP", "WWTFGEN", "WWISV", "WWLAB", "WWLAG", "WWOFS", "WWOXDI", "WWPADAE", "WWPTNK", \
#                      "WWSBRT", "WWSCRC", "WWSDB", "WWSCM", "WWSPMP", "WWST", "WWTLEM", "WWFRCM", "WWFRCM-S"]


#            # Initialize line counter for DBF file
#            dbfCounter = 1 # Start on line 2 (line 1 is headers)

#            with arcpy.da.SearchCursor(dbfGenAssetInfo, "*") as dbfCursor:
#                for dbfRec in dbfCursor:
#                    # Go to next record if AssetCode is blank (some spreadsheets have blank records)
#                    if str(dbfRec[1]) == "" or str(dbfRec[1]) == " ":
#                        continue

#    ##                # Asset_Code
#    ##                if not dbfRec[1]:
#    ##                    errorCounter = errorCounter + 1
#    ##                    errorLogFile.write(str(errorCounter) + "." + "Spreadsheet_Export.csv", "Data Value Check", "Line " + str(csvCounter) + ": Missing value for Asset_Code")
#    ##                elif str(dbfRec[1]) == "" or str(dbfRec[1]) == " ":
#    ##                    errorCounter = errorCounter + 1
#    ##                    errorLogFile.write(str(errorCounter) + "." + "Spreadsheet_Export.csv", "Data Value Check", "Line " + str(csvCounter) + ": Missing value for Asset_Code")

#                    # FeatureCod- dbfRec[4]
#                    if not dbfRec[4]:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'FeatureCode' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif str(dbfRec[4]) == "" or str(dbfRec[4]) == " ":
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'FeatureCode' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    else:
#                        if not dbfRec[4] in fcodes:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "Check the 'FeatureCode' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")

#                    # Condition - dbfRec[5]
#                    if dbfRec[5] == None:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Condition' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif is_number(dbfRec[5]):
#                        if int(dbfRec[5]) > 5:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "Check the 'Condition' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    else:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Condition' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")


#                    # Quantity - dbfRec[8]
#                    if dbfRec[8] == None:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Quantity' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif not is_number(dbfRec[8]):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Quantity' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif str(dbfRec[8]) == "" or str(dbfRec[8]) == " ":
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Quantity' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")

#    ##                # Age - dbfRec[10]
#    ##                if not is_number(dbfRec[10]):
#    ##                    errorCounter = errorCounter + 1
#    ##                    errorLogFile.write(str(errorCounter) + "." + "Check the 'Age' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#    ##                elif str(dbfRec[10]) == "" or str(dbfRec[10]) == " ":
#    ##                    errorCounter = errorCounter + 1
#    ##                    errorLogFile.write(str(errorCounter) + "." + "Check the 'Age' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#    ##                elif len(dbfRec[10]) == 4:
#    ##                    errorCounter = errorCounter + 1
#    ##                    errorLogFile.write(str(errorCounter) + "." + "Check the 'Age' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#    ##
#    ##                # Install Year - dbfRec[18]
#    ##                if not is_number(dbfRec[18]):
#    ##                    errorCounter = errorCounter + 1
#    ##                    errorLogFile.write(str(errorCounter) + "." + "Check the 'Install Year' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#    ##                elif str(dbfRec[18]) == "" or str(dbfRec[18]) == " ":
#    ##                    errorCounter = errorCounter + 1
#    ##                    errorLogFile.write(str(errorCounter) + "." + "Check the 'Install Year' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#    ##                elif len(dbfRec[18]) > 4:
#    ##                    errorCounter = errorCounter + 1
#    ##                    errorLogFile.write(str(errorCounter) + "." + "Check the 'Install Year' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")


#                    # Estimated (Estimated RUL) - dbfRec[19]
#                    if dbfRec[19] == None:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Estimated RUL' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif not is_number(dbfRec[19]):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Estimated RUL' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif str(dbfRec[19]) == "" or str(dbfRec[19]) == " ":
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Estimated RUL' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")


#                    # RplmtCst - dbfRec[20]
#                    if dbfRec[20] == None:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'RplmtCost' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif not is_number(dbfRec[20]):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'RplmtCost' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif str(dbfRec[20]) == "" or str(dbfRec[20]) == " ":
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'RplmtCost' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")


#                    # ConditionB (ConditionBasis) - dbfRec[21]
#                    if not dbfRec[21]:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'ConditionBasis' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif str(dbfRec[21]) == "" or str(dbfRec[21]) == " ":
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'ConditionBasis' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")


#                    # CostLookup - dbfRec[31]
#                    if not dbfRec[31]:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'CostLookup' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif str(dbfRec[31]) == "" or str(dbfRec[31]) == " ":
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'CostLookup' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")


#                    # Unit_Cost - dbfRec[37]
#                    if dbfRec[37] == None:
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Unit Cost' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif not is_number(dbfRec[37]):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Unit Cost' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                    elif str(dbfRec[37]) == "" or str(dbfRec[37]) == " ":
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "Check the 'Unit Cost' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")

#                    if shapefilesExist == True:
#                        # GIS_Link - dbfRec[39]
#                        if not dbfRec[39]:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "Check the 'GIS_Link' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")
#                        elif str(dbfRec[39]) == "" or str(dbfRec[39]) == " ":
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "Check the 'GIS_Link' value for the " + dbfRec[1] + " Asset_Code record in the " + munFullName + " spreadsheet (.XLSM)." + "\n\n")

#                    # Increase counter
#                    dbfCounter = dbfCounter + 1


#            # Parent folder of all shapefiles
#            shpFolder = munFolder + "GIS Imports/"
#            if not os.path.exists(shpFolder):
#                errorCounter = errorCounter + 1
#                errorLogFile.write(str(errorCounter) + "." + "The 'GIS_Imports' folder cannot be found." + "\n\n")


#            # In some of the shapefiles, the fields are called different things (always in same order though)
#            fieldsShapefile = []
#            fieldsShapefile.append("Shape")
#            fieldsShapefile.append("Elev")  #Sometimes called "Elevation"
#            fieldsShapefile.append("Width")
#            fieldsShapefile.append("GIS_Link")

#            #fieldsShapefile.append("FID")
#            #fieldsShapefile.append("Mun_ID")
#            #fieldsShapefile.append("FCode")  #Sometimes called "FeatureCod" "FreatureCo" or "Feature"
#            #fieldsShapefile.append("N")  #Sometimes called "Northing"
#            #fieldsShapefile.append("E")  #Sometimes called "Easting"
#            #fieldsShapefile.append("Condition")
#            #fieldsShapefile.append("Material")
#            #fieldsShapefile.append("Install_Yr")  #Sometimes called "Install Yr" or "Install_Da"
#            #fieldsShapefile.append("LocDesc")
#            #fieldsShapefile.append("Diameter")
#            #fieldsShapefile.append("Comments")  #Sometimes called "Comment"
#            #fieldsShapefile.append("Quantity")  #Sometimes called "Length"
#            #fieldsShapefile.append("Status")



#            # Check fields in shapefiles if shapefilesExist = True (method = "GIS")
#            if shapefilesExist == True:

#                # PWS line
#                # ========
#                shpFolder_PWS_L = shpFolder + "PWS L/"
#                shpFileName = shpMunID + " PWS L.shp"
#                shpFullPath = shpFolder_PWS_L + shpFileName

#                if not os.path.exists(shpFolder_PWS_L):
#                    errorCounter = errorCounter + 1
#                    errorLogFile.write(str(errorCounter) + "." + "The 'PWS L' sub-folder cannot be found under the 'GIS Imports' folder." + "\n\n")
#                else:
#                    if not arcpy.Exists(shpFullPath):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile cannot be found under the 'GIS Imports/PWS L' folder." + "\n\n")
#                    else:
#                        # Make sure its spatial reference is NAD83 UTM20
#                        if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920 or arcpy.Describe(shpFullPath).spatialReference.factoryCode == 2961:
#                        #if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920:
#                            # Check that it has all the correct fields
#                            fieldsShp = arcpy.ListFields(shpFullPath)
#                            fieldsShpNames = []
#                            for field in fieldsShp:
#                                fieldsShpNames.append(field.name)
#                            # Check fields against mandatory shapefile fields
#                            # Only Shape, Elevation, Width and GIS_Link are taken from the shapefiles; others come from the spreadsheet CSV
#                            for field in fieldsShapefile:
#                                if field == "Elev":
#                                    if "Elev" not in fieldsShpNames:
#                                        if "Elevation" not in fieldsShpNames:
#                                            if "ELEVATION" not in fieldsShpNames:
#                                                errorCounter = errorCounter + 1
#                                                errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                                else:
#                                    if field not in fieldsShpNames:
#                                        errorCounter = errorCounter + 1
#                                        errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                        else:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile has an invalid Spatial Reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'." + "\n\n")


#                # PWS point
#                # ========
#                shpFolder_PWS_P = shpFolder + "PWS P/"
#                shpFileName = shpMunID + " PWS P.shp"
#                shpFullPath = shpFolder_PWS_P + shpFileName

#                if not os.path.exists(shpFolder_PWS_P):
#                    errorCounter = errorCounter + 1
#                    errorLogFile.write(str(errorCounter) + "." + "The 'PWS P' sub-folder cannot be found under the 'GIS Imports' folder." + "\n\n")
#                else:
#                    if not arcpy.Exists(shpFullPath):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile cannot be found under the 'GIS Imports/PWS P' folder." + "\n\n")
#                    else:
#                        # Make sure its spatial reference is NAD83 UTM20
#                        if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920 or arcpy.Describe(shpFullPath).spatialReference.factoryCode == 2961:
#                        #if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920:
#                            # Check that it has all the correct fields
#                            fieldsShp = arcpy.ListFields(shpFullPath)
#                            fieldsShpNames = []
#                            for field in fieldsShp:
#                                fieldsShpNames.append(field.name)
#                            # Check fields against mandatory shapefile fields
#                            # Only Shape, Elevation, Width and GIS_Link are taken from the shapefiles; others come from the spreadsheet CSV
#                            for field in fieldsShapefile:
#                                if field == "Elev":
#                                    if "Elev" not in fieldsShpNames:
#                                        if "Elevation" not in fieldsShpNames:
#                                            if "ELEVATION" not in fieldsShpNames:
#                                                errorCounter = errorCounter + 1
#                                                errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                                else:
#                                    if field not in fieldsShpNames:
#                                        errorCounter = errorCounter + 1
#                                        errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                        else:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile has an invalid Spatial Reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'." + "\n\n")


#                # SWC line
#                # ========
#                shpFolder_SWC_L = shpFolder + "SWC L/"
#                shpFileName = shpMunID + " SWC L.shp"
#                shpFullPath = shpFolder_SWC_L + shpFileName

#                if not os.path.exists(shpFolder_SWC_L):
#                    errorCounter = errorCounter + 1
#                    errorLogFile.write(str(errorCounter) + "." + "The 'SWC L' sub-folder cannot be found under the 'GIS Imports' folder." + "\n\n")
#                else:
#                    if not arcpy.Exists(shpFullPath):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile cannot be found under the 'GIS Imports/SWC L' folder." + "\n\n")
#                    else:
#                        # Make sure its spatial reference is NAD83 UTM20
#                        if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920 or arcpy.Describe(shpFullPath).spatialReference.factoryCode == 2961:
#                        #if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920:
#                            # Check that it has all the correct fields
#                            fieldsShp = arcpy.ListFields(shpFullPath)
#                            fieldsShpNames = []
#                            for field in fieldsShp:
#                                fieldsShpNames.append(field.name)
#                            # Check fields against mandatory shapefile fields
#                            # Only Shape, Elevation, Width and GIS_Link are taken from the shapefiles; others come from the spreadsheet CSV
#                            for field in fieldsShapefile:
#                                if field == "Elev":
#                                    if "Elev" not in fieldsShpNames:
#                                        if "Elevation" not in fieldsShpNames:
#                                            if "ELEVATION" not in fieldsShpNames:
#                                                errorCounter = errorCounter + 1
#                                                errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                                else:
#                                    if field not in fieldsShpNames:
#                                        errorCounter = errorCounter + 1
#                                        errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                        else:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile has an invalid Spatial Reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'." + "\n\n")

#                # SWC point
#                # ========
#                shpFolder_SWC_P = shpFolder + "SWC P/"
#                shpFileName = shpMunID + " SWC P.shp"
#                shpFullPath = shpFolder_SWC_P + shpFileName

#                if not os.path.exists(shpFolder_SWC_P):
#                    errorCounter = errorCounter + 1
#                    errorLogFile.write(str(errorCounter) + "." + "The 'SWC P' sub-folder cannot be found under the 'GIS Imports' folder." + "\n\n")
#                else:
#                    if not arcpy.Exists(shpFullPath):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile cannot be found under the 'GIS Imports/SWC P' folder." + "\n\n")
#                    else:
#                        # Make sure its spatial reference is NAD83 UTM20
#                        if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920 or arcpy.Describe(shpFullPath).spatialReference.factoryCode == 2961:
#                        #if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920:
#                            # Check that it has all the correct fields
#                            fieldsShp = arcpy.ListFields(shpFullPath)
#                            fieldsShpNames = []
#                            for field in fieldsShp:
#                                fieldsShpNames.append(field.name)
#                            # Check fields against mandatory shapefile fields
#                            # Only Shape, Elevation, Width and GIS_Link are taken from the shapefiles; others come from the spreadsheet CSV
#                            for field in fieldsShapefile:
#                                if field == "Elev":
#                                    if "Elev" not in fieldsShpNames:
#                                        if "Elevation" not in fieldsShpNames:
#                                            if "ELEVATION" not in fieldsShpNames:
#                                                errorCounter = errorCounter + 1
#                                                errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the " + shpFileName + " shapefile." + "\n\n")
#                                else:
#                                    if field not in fieldsShpNames:
#                                        errorCounter = errorCounter + 1
#                                        errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the " + shpFileName + " shapefile." + "\n\n")
#                        else:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile has an invalid Spatial Reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'." + "\n\n")


#                # TRN line
#                # ========
#                shpFolder_TRN_L = shpFolder + "TRN L/"
#                shpFileName = shpMunID + " TRN L.shp"
#                shpFullPath = shpFolder_TRN_L + shpFileName

#                if not os.path.exists(shpFolder_TRN_L):
#                    errorCounter = errorCounter + 1
#                    errorLogFile.write(str(errorCounter) + "." + "The 'TRN L' sub-folder cannot be found under the 'GIS Imports' folder." + "\n\n")
#                else:
#                    if not arcpy.Exists(shpFullPath):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile cannot be found under the 'GIS Imports/TRN L' folder." + "\n\n")
#                    else:
#                        # Make sure its spatial reference is NAD83 UTM20
#                        if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920 or arcpy.Describe(shpFullPath).spatialReference.factoryCode == 2961:
#                        #if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920:
#                            # Check that it has all the correct fields
#                            fieldsShp = arcpy.ListFields(shpFullPath)
#                            fieldsShpNames = []
#                            for field in fieldsShp:
#                                fieldsShpNames.append(field.name)
#                            # Check fields against mandatory shapefile fields
#                            # Only Shape, Elevation, Width and GIS_Link are taken from the shapefiles; others come from the spreadsheet CSV
#                            for field in fieldsShapefile:
#                                if field == "Elev":
#                                    if "Elev" not in fieldsShpNames:
#                                        if "Elevation" not in fieldsShpNames:
#                                            if "ELEVATION" not in fieldsShpNames:
#                                                errorCounter = errorCounter + 1
#                                                errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                                else:
#                                    if field not in fieldsShpNames:
#                                        errorCounter = errorCounter + 1
#                                        errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                        else:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile has an invalid Spatial Reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'." + "\n\n")


#                # TRN point
#                # ========
#                shpFolder_TRN_P = shpFolder + "TRN P/"
#                shpFileName = shpMunID + " TRN P.shp"
#                shpFullPath = shpFolder_TRN_P + shpFileName

#                if not os.path.exists(shpFolder_TRN_P):
#                    errorCounter = errorCounter + 1
#                    errorLogFile.write(str(errorCounter) + "." + "The 'TRN P' sub-folder cannot be found under the 'GIS Imports' folder." + "\n\n")
#                else:
#                    if not arcpy.Exists(shpFullPath):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile cannot be found under the 'GIS Imports/TRN P' folder." + "\n\n")
#                    else:
#                        # Make sure its spatial reference is NAD83 UTM20
#                        if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920 or arcpy.Describe(shpFullPath).spatialReference.factoryCode == 2961:
#                        #if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920:
#                            # Check that it has all the correct fields
#                            fieldsShp = arcpy.ListFields(shpFullPath)
#                            fieldsShpNames = []
#                            for field in fieldsShp:
#                                fieldsShpNames.append(field.name)
#                            # Check fields against mandatory shapefile fields
#                            # Only Shape, Elevation, Width and GIS_Link are taken from the shapefiles; others come from the spreadsheet CSV
#                            for field in fieldsShapefile:
#                                if field == "Elev":
#                                    if "Elev" not in fieldsShpNames:
#                                        if "Elevation" not in fieldsShpNames:
#                                            if "ELEVATION" not in fieldsShpNames:
#                                                errorCounter = errorCounter + 1
#                                                errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                                else:
#                                    if field not in fieldsShpNames:
#                                        errorCounter = errorCounter + 1
#                                        errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                        else:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile has an invalid Spatial Reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'." + "\n\n")


#                # WWC line
#                # ========
#                shpFolder_WWC_L = shpFolder + "WWC L/"
#                shpFileName = shpMunID + " WWC L.shp"
#                shpFullPath = shpFolder_WWC_L + shpFileName

#                if not os.path.exists(shpFolder_WWC_L):
#                    errorCounter = errorCounter + 1
#                    errorLogFile.write(str(errorCounter) + "." + "The 'WWC L' sub-folder cannot be found under the 'GIS Imports' folder." + "\n\n")
#                else:
#                    if not arcpy.Exists(shpFullPath):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile cannot be found under the 'GIS Imports/WWC L' folder." + "\n\n")
#                    else:
#                        # Make sure its spatial reference is NAD83 UTM20
#                        if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920 or arcpy.Describe(shpFullPath).spatialReference.factoryCode == 2961:
#                        #if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920:
#                            # Check that it has all the correct fields
#                            fieldsShp = arcpy.ListFields(shpFullPath)
#                            fieldsShpNames = []
#                            for field in fieldsShp:
#                                fieldsShpNames.append(field.name)
#                            # Check fields against mandatory shapefile fields
#                            # Only Shape, Elevation, Width and GIS_Link are taken from the shapefiles; others come from the spreadsheet CSV
#                            for field in fieldsShapefile:
#                                if field == "Elev":
#                                    if "Elev" not in fieldsShpNames:
#                                        if "Elevation" not in fieldsShpNames:
#                                            if "ELEVATION" not in fieldsShpNames:
#                                                errorCounter = errorCounter + 1
#                                                errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                                else:
#                                    if field not in fieldsShpNames:
#                                        errorCounter = errorCounter + 1
#                                        errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                        else:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile has an invalid Spatial Reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'." + "\n\n")


#                # WWC point
#                # ========
#                shpFolder_WWC_P = shpFolder + "WWC P/"
#                shpFileName = shpMunID + " WWC P.shp"
#                shpFullPath = shpFolder_WWC_P + shpFileName

#                if not os.path.exists(shpFolder_WWC_P):
#                    errorCounter = errorCounter + 1
#                    #errorLogFile.write(str(errorCounter) + "." + shpFolder_WWC_P, "File/Folder Check", "Folder Missing")
#                    errorLogFile.write(str(errorCounter) + "." + "The 'WWC P' sub-folder cannot be found under the 'GIS Imports' folder." + "\n\n")
#                else:
#                    if not arcpy.Exists(shpFullPath):
#                        errorCounter = errorCounter + 1
#                        errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile cannot be found under the 'GIS Imports/WWC P' folder." + "\n\n")
#                    else:
#                        # Make sure its spatial reference is NAD83 UTM20
#                        if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920 or arcpy.Describe(shpFullPath).spatialReference.factoryCode == 2961:
#                        #if arcpy.Describe(shpFullPath).spatialReference.factoryCode == 26920:
#                            # Check that it has all the correct fields
#                            fieldsShp = arcpy.ListFields(shpFullPath)
#                            fieldsShpNames = []
#                            for field in fieldsShp:
#                                fieldsShpNames.append(field.name)
#                            # Check fields against mandatory shapefile fields
#                            # Only Shape, Elevation, Width and GIS_Link are taken from the shapefiles; others come from the spreadsheet CSV
#                            for field in fieldsShapefile:
#                                if field == "Elev":
#                                    if "Elev" not in fieldsShpNames:
#                                        if "Elevation" not in fieldsShpNames:
#                                            if "ELEVATION" not in fieldsShpNames:
#                                                errorCounter = errorCounter + 1
#                                                errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                                else:
#                                    if field not in fieldsShpNames:
#                                        errorCounter = errorCounter + 1
#                                        errorLogFile.write(str(errorCounter) + "." + "The '" + field + "' field is missing from the '" + shpFileName + "' shapefile." + "\n\n")
#                        else:
#                            errorCounter = errorCounter + 1
#                            errorLogFile.write(str(errorCounter) + "." + "The '" + shpFileName + "' shapefile has an invalid Spatial Reference. The coordinate system must be 'NAD_1983_UTM_Zone_20N' or 'NAD_1983_CSRS_UTM_Zone_20N'." + "\n\n")



#        # Close the error log file
#        errorLogFile.close()


#        # =============================================================================================
#        # Send an email to the user if validation fails (with txt file), or after upload, if successful

#		# Commented out 25 Jan 2019
#        ##errorCounter = 0

#        if errorCounter > 0:
#            #raise Exception
#            UploadStatus = "Validation Failed"
#            NotifyClient(munFullName, errorFilenameShort, errorFilename, UploadStatus)
#            arcpy.AddError("Validation Failed")

#        else:
#            # Proceed with the Upload
#            UploadStatus = Upload()

#        # =============================================================================================


#    except KeyboardInterrupt:
#        exit()


#    except Exception, e:
#        arcpy.AddMessage("ERROR: Exception on line number:" + str(sys.exc_traceback.tb_lineno) + "\n" + str(e) + "\n")
#        UploadStatus = "Validation Failed"
#        NotifyClient(munFullName, errorFilenameShort, errorFilename, UploadStatus)
#        #sys.exit(1)


#def Upload():

#    try:

#        #global parentFolder, munFolder, munID, shpMunID, munName, munFullName, mun
#        global munFolder, munID, shpMunID, munName, munFullName, mun
#        global method, gdb, shapefilesExist, totalCounter


#        # Get the Spreadsheet Export folder
#        ssExportFolder = munFolder + "Spreadsheet Export/"
#        # Get folder where shapefiles reside (or will reside)
#        shpFolder = munFolder + "GIS Imports/"

#        # Set workspace to Spreadsheet Export folder
#        arcpy.env.workspace = ssExportFolder
#        # Overwrite any outputs
#        arcpy.env.overwriteOutput = True


#        # Get the CSV file of spreadsheet (General Asset Information sheet)
#        csvGenAssetInfo = munFolder + "GenAssetInfo.csv"
#        # Convert CSV file to DBF
#        arcpy.TableToTable_conversion(csvGenAssetInfo, munFolder, "GenAssetInfo.dbf")
#        dbfGenAssetInfo = munFolder + "GenAssetInfo.dbf"


#        # ==============================================================================================

#        # If the Survey method is chosen, then we have to input the data into the shapefiles first
#        if shapefilesExist == False:

#            # Get the actual spreadsheet
#            for file in os.listdir(munFolder):
#                if file.endswith(".xlsm") and file.startswith(munID):
#                    fileSpreadsheet = munFolder + file
#                    break


#            # Get the Asset Details sheet
#            wb = xlrd.open_workbook(fileSpreadsheet)
#            sheetAssetDetails = wb.sheet_by_name("Asset Details")
#            csvAssetDetails = open(munFolder + "AssetDetails.csv", "wb")
#            wr = csv.writer(csvAssetDetails, quoting=csv.QUOTE_ALL)

#            # Write remaining rows with data
#            for rownum in xrange(sheetAssetDetails.nrows):
#                # Skip the first two rows
#                if rownum == 0 or rownum == 1:
#                    continue
#                # Write other row values to CSV
#                wr.writerow(sheetAssetDetails.row_values(rownum))

#            # Close the spreadsheet and CSV
#            wb.release_resources()
#            del wb
#            csvAssetDetails.close()



#            # Will create a temporary DBF in the municipality folder
#            dbfFile = munFolder + "AssetDetails.dbf"
#            # Delete if already there
#            if os.path.isfile(dbfFile):
#                os.remove(dbfFile)
#            # Might also be a dbf.xml file
#            if os.path.isfile(munFolder + "AssetDetails.dbf.xml"):
#                os.remove(munFolder + "AssetDetails.dbf.xml")
#            # Convert CSV to DBF
#            arcpy.TableToTable_conversion(munFolder + "AssetDetails.csv", munFolder, "AssetDetails.dbf")


#            # Need to create all the shapefiles in the various subfolders of the GIS Imports folder
#            arcpy.env.workspace = shpFolder
#            arcpy.env.overwriteOutput = True

#            # Will create them in UTM 20 NAD83 CSRS spatial reference
#            srNAD83_CSRS_UTM20 = arcpy.SpatialReference(2961)

#            #print "Creating shapefiles from the AssetDetails sheet..." + "\n"


#            # Delete any shapefiles in the sub-folders
#            # PWS L
#            if arcpy.Exists(shpFolder + "PWS L/" + shpMunID + " PWS L.shp"):
#                arcpy.Delete_management(shpFolder + "PWS L/" + shpMunID + " PWS L.shp")
#            # PWS P
#            if arcpy.Exists(shpFolder + "PWS P/" + shpMunID + " PWS P.shp"):
#                arcpy.Delete_management(shpFolder + "PWS P/" + shpMunID + " PWS P.shp")
#            # SWC L
#            if arcpy.Exists(shpFolder + "SWC L/" + shpMunID + " SWC L.shp"):
#                arcpy.Delete_management(shpFolder + "SWC L/" + shpMunID + " SWC L.shp")
#            # SWC P
#            if arcpy.Exists(shpFolder + "SWC P/" + shpMunID + " SWC P.shp"):
#                arcpy.Delete_management(shpFolder + "SWC P/" + shpMunID + " SWC P.shp")
#            # TRN L
#            if arcpy.Exists(shpFolder + "TRN L/" + shpMunID + " TRN L.shp"):
#                arcpy.Delete_management(shpFolder + "TRN L/" + shpMunID + " TRN L.shp")
#            # TRN P
#            if arcpy.Exists(shpFolder + "TRN P/" + shpMunID + " TRN P.shp"):
#                arcpy.Delete_management(shpFolder + "TRN P/" + shpMunID + " TRN P.shp")
#            # WWC L
#            if arcpy.Exists(shpFolder + "WWC L/" + shpMunID + " WWC L.shp"):
#                arcpy.Delete_management(shpFolder + "WWC L/" + shpMunID + " WWC L.shp")
#            # WWC P
#            if arcpy.Exists(shpFolder + "WWC P/" + shpMunID + " WWC P.shp"):
#                arcpy.Delete_management(shpFolder + "WWC P/" + shpMunID + " WWC P.shp")


#            # Create point and line shapefiles for each Asset Class based on the above template shapefiles
#            shapefileName = shpFolder + "PWS P/" + shpMunID + " PWS P.shp"
#            arcpy.CreateFeatureclass_management(shpFolder + "PWS P", shpMunID + " PWS P", "POINT", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
#            arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
#            arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Elevation", "LONG")
#            arcpy.AddField_management(shapefileName, "Width", "LONG")

#            shapefileName = shpFolder + "PWS L/" + shpMunID + " PWS L.shp"
#            arcpy.CreateFeatureclass_management(shpFolder + "PWS L", shpMunID + " PWS L", "POLYLINE", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
#            arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
#            arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Elevation", "LONG")
#            arcpy.AddField_management(shapefileName, "Width", "LONG")

#            shapefileName = shpFolder + "SWC P/" + shpMunID + " SWC P.shp"
#            arcpy.CreateFeatureclass_management(shpFolder + "SWC P", shpMunID + " SWC P", "POINT", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
#            arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
#            arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Elevation", "LONG")
#            arcpy.AddField_management(shapefileName, "Width", "LONG")

#            shapefileName = shpFolder + "SWC L/" + shpMunID + " SWC L.shp"
#            arcpy.CreateFeatureclass_management(shpFolder + "SWC L", shpMunID + " SWC L", "POLYLINE", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
#            arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
#            arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Elevation", "LONG")
#            arcpy.AddField_management(shapefileName, "Width", "LONG")

#            shapefileName = shpFolder + "TRN P/" + shpMunID + " TRN P.shp"
#            arcpy.CreateFeatureclass_management(shpFolder + "TRN P", shpMunID + " TRN P", "POINT", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
#            arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
#            arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Elevation", "LONG")
#            arcpy.AddField_management(shapefileName, "Width", "LONG")

#            shapefileName = shpFolder + "TRN L/" + shpMunID + " TRN L.shp"
#            arcpy.CreateFeatureclass_management(shpFolder + "TRN L", shpMunID + " TRN L", "POLYLINE", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
#            arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
#            arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Elevation", "LONG")
#            arcpy.AddField_management(shapefileName, "Width", "LONG")

#            shapefileName = shpFolder + "WWC P/" + shpMunID + " WWC P.shp"
#            arcpy.CreateFeatureclass_management(shpFolder + "WWC P", shpMunID + " WWC P", "POINT", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
#            arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
#            arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Elevation", "LONG")
#            arcpy.AddField_management(shapefileName, "Width", "LONG")

#            shapefileName = shpFolder + "WWC L/" + shpMunID + " WWC L.shp"
#            arcpy.CreateFeatureclass_management(shpFolder + "WWC L", shpMunID + " WWC L", "POLYLINE", "", "DISABLED", "DISABLED", srNAD83_CSRS_UTM20)
#            arcpy.AddField_management(shapefileName, "AssetCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Mun_ID", "TEXT", "", "", 254)
#            arcpy.AddField_management(shapefileName, "FCode", "TEXT", "", "", 50)
#            arcpy.AddField_management(shapefileName, "Elevation", "LONG")
#            arcpy.AddField_management(shapefileName, "Width", "LONG")


#            # Cursor through DBF file and put things in the appropriate shapefiles
#            inputFields_AssetDetails = ["Asset_Code", "Northing", "Easting", "Elevation", "Width", "FC"]
#            outputFields_Shp_Point = ["SHAPE@X", "SHAPE@Y", "AssetCode", "Mun_ID", "FCode", "Elevation", "Width"]
#            outputFields_Shp_Line = ["SHAPE@", "AssetCode", "Mun_ID", "FCode", "Elevation", "Width"]


#            # Initialize counter
#            counter = 0


#            # Write values to output tables corresponding to Asset Class
#            tabAssetDetails = munFolder + "AssetDetails.dbf"


#            # -----------------------------------------------------------------------------------------------------------------------------------------------------------
#            tabPWS_P = "AssetDetails_PWS_P"
#            queryPWS_P = "\"FC\" IN ('BST','CS','WV','FTBD11','FTBD22','FTBD45','FTBD90','FTCAP','FTCP','FTHY','FTHYTE','FTRD','FTTS','FTTE','HY','METER','PRV','APV','WSST','WSTF','FTVLHY','GV','WS','WSTFAC','WSCPMP','WSISV','WSSPMP','WSTFBLD','WSCCSYS','WSCLLD','WSCLAR','WSCOMP','WSDAFS','WSDAFT','WSELECM','WSFLME','WSGDTP','WSTFGEN','WSLAB','WSMFS','WSMMF','WSOFS','WSPTNK','WSSCM','WSTLEM','WSUV','WSVACCL')"
#            arcpy.MakeTableView_management(tabAssetDetails, tabPWS_P, queryPWS_P)
#            countPWS_P = arcpy.GetCount_management(tabPWS_P).getOutput(0)
#            if countPWS_P > 0:
#                arcpy.CopyRows_management(tabPWS_P, munFolder + "AssetDetails_PWS_P.dbf")


#            # Output shapefile
#            outputShapeFile = shpFolder + "PWS P/" + shpMunID + " PWS P.shp"

#            # Start editing - without an undo/redo stack
#            editShapefile = arcpy.da.Editor(shpFolder + "PWS P/")
#            editShapefile.startEditing(False, True)
#            # Start an edit operation
#            editShapefile.startOperation()


#            # Cursor through input table and write points to shapefile
#            with arcpy.da.SearchCursor(munFolder + "AssetDetails_PWS_P.dbf", inputFields_AssetDetails) as inputCursor:

#                for inputRec in inputCursor:
#                    # Create shape from Northing and Easting coordinates
#                    x = inputRec[2]  # Easting
#                    y = inputRec[1]  # Northing
#                    # AssetCode
#                    AssetCode = inputRec[0]
#                    # Elevation
#                    Elev = float(inputRec[3])
#                    # Width
#                    if is_number(inputRec[4]):
#                        Width = Dbl(inputRec[4])
#                    else:
#                        Width = 0
#                    # Feature Code
#                    FCode = inputRec[5]

#                    # Write values to output shapefile
#                    with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Point) as outputCursor:
#                       # Insert the feature
#                       outputCursor.insertRow((x, y, AssetCode, munID, FCode, Elev, Width))


#            # Stop the edit operation
#            editShapefile.stopOperation()
#            # Stop the edit session and save the changes
#            editShapefile.stopEditing(True)


#            # -----------------------------------------------------------------------------------------------------------------------------------------------------------
#            tabPWS_L = "AssetDetails_PWS_L"
#            queryPWS_L = "\"FC\" IN ('DIMN','DIMN-S','TRNS','TRNS-S')"
#            arcpy.MakeTableView_management(tabAssetDetails, tabPWS_L, queryPWS_L)
#            countPWS_L = arcpy.GetCount_management(tabPWS_L).getOutput(0)
#            if countPWS_L > 0:
#                arcpy.CopyRows_management(tabPWS_L, munFolder + "AssetDetails_PWS_L.dbf")

#            # Make a list of AssetCodes
#            lstAssetCodes = []

#            # Cursor through input table and get a list of asset codes
#            with arcpy.da.SearchCursor(munFolder + "AssetDetails_PWS_L.dbf", inputFields_AssetDetails) as inputCursor:
#                # Cursor through all records to get a unique list
#                for inputRec in inputCursor:
#                    #print inputRec[0]
#                    if inputRec[0] not in lstAssetCodes:
#                        lstAssetCodes.append(inputRec[0])


#            # Output shapefile
#            outputShapeFile = shpFolder + "PWS L/" + shpMunID + " PWS L.shp"
#            editShapefile = arcpy.da.Editor(shpFolder + "PWS L/")

#            # Start editing - without an undo/redo stack
#            editShapefile.startEditing(False, True)
#            # Start an edit operation
#            editShapefile.startOperation()


#            #print "Importing PWS Line asset data..."


#            # For each Asset Code, query the table and make polylines
#            for ac in lstAssetCodes:

#                # Create query
#                queryAssetCode = "\"Asset_Code\" = '" + ac + "'"
#                with arcpy.da.SearchCursor(munFolder + "AssetDetails_PWS_L.dbf", inputFields_AssetDetails, queryAssetCode) as inputCursor:

#                    # Create an empty array
#                    arrayPoints = arcpy.Array()

#                    for inputRec in inputCursor:
#                        # Get Feature Code first
#                        FCode = inputRec[5]
#                        #print FCode

#                        # If FCode has "-S" at the end, create a point and add to the array.
#                        # Then just go to the next record
#                        if "-S" in FCode:
#                            # Northing and Easting coordinates for Start Point
#                            x = inputRec[2]  # Easting
#                            y = inputRec[1]  # Northing
#                            # Create point
#                            pntStart = arcpy.Point(x, y)
#                            # Add start point to the array
#                            arrayPoints.add(pntStart)
#                        else:
#                            # AssetCode
#                            AssetCode = inputRec[0]
#                            # Elevation
#                            Elev = float(inputRec[3])
#                            # Width
#                            if is_number(inputRec[4]):
#                                Width = Dbl(inputRec[4])
#                            else:
#                                Width = 0
#                            # FCode
#                            FCode = inputRec[5]
#                            # Northing and Easting coordinates for next Point
#                            x = inputRec[2]  # Easting
#                            y = inputRec[1]  # Northing
#                            # Create point
#                            pntNext = arcpy.Point(x, y)
#                            # Add to array
#                            arrayPoints.add(pntNext)

#                    # Make sure array has at least 2 points
#                    if arrayPoints.count >= 2:
#                        # Make the line once all points collected (usually just 2)
#                        polyline = arcpy.Polyline(arrayPoints, srNAD83_CSRS_UTM20)

#                        # Write values to output shapefile
#                        with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Line) as outputCursor:
#                            # Insert the feature
#                            outputCursor.insertRow(((polyline), AssetCode, munID, FCode, Elev, Width))


#            # Stop the edit operation
#            editShapefile.stopOperation()
#            # Stop the edit session and save the changes
#            editShapefile.stopEditing(True)


#            # -----------------------------------------------------------------------------------------------------------------------------------------------------------
#            tabSWC_P = "AssetDetails_SWC_P"
#            querySWC_P = "\"FC\" IN ('CB','IO','LIFT','MHST','PND','TRMTD','UGS')"
#            arcpy.MakeTableView_management(tabAssetDetails, tabSWC_P, querySWC_P)
#            countSWC_P = arcpy.GetCount_management(tabSWC_P).getOutput(0)
#            if countSWC_P > 0:
#                arcpy.CopyRows_management(tabSWC_P, munFolder + "AssetDetails_SWC_P.dbf")


#            # Output shapefile
#            outputShapeFile = shpFolder + "SWC P/" + shpMunID + " SWC P.shp"

#            # Start editing - without an undo/redo stack
#            editShapefile = arcpy.da.Editor(shpFolder + "SWC P/")
#            editShapefile.startEditing(False, True)
#            # Start an edit operation
#            editShapefile.startOperation()


#            #print "Importing SWC Point asset data..."


#            # Cursor through input table and write points to shapefile
#            with arcpy.da.SearchCursor(munFolder + "AssetDetails_SWC_P.dbf", inputFields_AssetDetails) as inputCursor:

#                for inputRec in inputCursor:
#                    # Create shape from Northing and Easting coordinates
#                    x = inputRec[2]  # Easting
#                    y = inputRec[1]  # Northing
#                    # AssetCode
#                    AssetCode = inputRec[0]
#                    # Elevation
#                    Elev = float(inputRec[3])
#                    # Width
#                    if is_number(inputRec[4]):
#                        Width = Dbl(inputRec[4])
#                    else:
#                        Width = 0
#                    # Feature Code
#                    FCode = inputRec[5]

#                    # Write values to output shapefile
#                    with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Point) as outputCursor:
#                       # Insert the feature
#                       outputCursor.insertRow((x, y, AssetCode, munID, FCode, Elev, Width))


#            # Stop the edit operation
#            editShapefile.stopOperation()
#            # Stop the edit session and save the changes
#            editShapefile.stopEditing(True)


#            # -----------------------------------------------------------------------------------------------------------------------------------------------------------
#            tabSWC_L = "AssetDetails_SWC_L"
#            querySWC_L = "\"FC\" IN ('CLVT','CLVT-S','DRCH','DRCH-S','RRGT','RRGT-S','GRVPST','GRVPST-S','SWFRCM','SWFRCM-S')"
#            arcpy.MakeTableView_management(tabAssetDetails, tabSWC_L, querySWC_L)
#            countSWC_L = arcpy.GetCount_management(tabSWC_L).getOutput(0)
#            if countSWC_L > 0:
#                arcpy.CopyRows_management(tabSWC_L, munFolder + "AssetDetails_SWC_L.dbf")

#            # Make a list of AssetCodes
#            lstAssetCodes = []

#            # Cursor through input table and get a list of asset codes
#            with arcpy.da.SearchCursor(munFolder + "AssetDetails_SWC_L.dbf", inputFields_AssetDetails) as inputCursor:

#                # Cursor through all records to get a unique list
#                for inputRec in inputCursor:
#                    if inputRec[0] not in lstAssetCodes:
#                        lstAssetCodes.append(inputRec[0])


#            # Output shapefile
#            outputShapeFile = shpFolder + "SWC L/" + shpMunID + " SWC L.shp"
#            editShapefile = arcpy.da.Editor(shpFolder + "SWC L/")

#            # Start editing - without an undo/redo stack
#            editShapefile.startEditing(False, True)
#            # Start an edit operation
#            editShapefile.startOperation()


#            #print "Importing SWC Line asset data..."


#            # For each Asset Code, query the table and make polylines
#            for ac in lstAssetCodes:

#                # Create query
#                queryAssetCode = "\"Asset_Code\" = '" + ac + "'"
#                with arcpy.da.SearchCursor(munFolder + "AssetDetails_SWC_L.dbf", inputFields_AssetDetails, queryAssetCode) as inputCursor:

#                    # Create an empty array
#                    arrayPoints = arcpy.Array()

#                    for inputRec in inputCursor:
#                        # Get Feature Code first
#                        FCode = inputRec[5]

#                        # If FCode has "-S" at the end, create a point and add to the array.
#                        # Then just go to the next record
#                        if "-S" in FCode:
#                            # Northing and Easting coordinates for Start Point
#                            x = inputRec[2]  # Easting
#                            y = inputRec[1]  # Northing
#                            # Create point
#                            pntStart = arcpy.Point(x, y)
#                            # Add start point to the array
#                            arrayPoints.add(pntStart)
#                        else:
#                            # AssetCode
#                            AssetCode = inputRec[0]
#                            # Elevation
#                            Elev = float(inputRec[3])
#                            # Width
#                            if is_number(inputRec[4]):
#                                Width = Dbl(inputRec[4])
#                            else:
#                                Width = 0
#                            # FCode
#                            FCode = inputRec[5]
#                            # Northing and Easting coordinates for next Point
#                            x = inputRec[2]  # Easting
#                            y = inputRec[1]  # Northing
#                            # Create point
#                            pntNext = arcpy.Point(x, y)
#                            # Add to array
#                            arrayPoints.add(pntNext)

#                    # Make sure array has at least 2 points
#                    if arrayPoints.count >= 2:
#                        # Make the line once all points collected (usually just 2)
#                        polyline = arcpy.Polyline(arrayPoints, srNAD83_CSRS_UTM20)

#                        # Write values to output shapefile
#                        with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Line) as outputCursor:
#                            # Insert the feature
#                            outputCursor.insertRow(((polyline), AssetCode, munID, FCode, Elev, Width))


#            # Stop the edit operation
#            editShapefile.stopOperation()
#            # Stop the edit session and save the changes
#            editShapefile.stopEditing(True)


#            # -----------------------------------------------------------------------------------------------------------------------------------------------------------
#            tabTRN_P = "AssetDetails_TRN_P"
#            queryTRN_P = "\"FC\" IN ('STPR','TFSP','TFTL','TSIG','UTPO','TFSLOR','TFSL')"
#            arcpy.MakeTableView_management(tabAssetDetails, tabTRN_P, queryTRN_P)
#            countTRN_P = arcpy.GetCount_management(tabTRN_P).getOutput(0)
#            if countTRN_P > 0:
#                arcpy.CopyRows_management(tabTRN_P, munFolder + "AssetDetails_TRN_P.dbf")

#            # Output shapefile
#            outputShapeFile = shpFolder + "TRN P/" + shpMunID + " TRN P.shp"

#            # Start editing - without an undo/redo stack
#            editShapefile = arcpy.da.Editor(shpFolder + "TRN P/")
#            editShapefile.startEditing(False, True)
#            # Start an edit operation
#            editShapefile.startOperation()


#            #print "Importing TRN Point asset data..."


#            # Cursor through input table and write points to shapefile
#            with arcpy.da.SearchCursor(munFolder + "AssetDetails_TRN_P.dbf", inputFields_AssetDetails) as inputCursor:

#                for inputRec in inputCursor:
#                    # Create shape from Northing and Easting coordinates
#                    x = inputRec[2]  # Easting
#                    y = inputRec[1]  # Northing
#                    # AssetCode
#                    AssetCode = inputRec[0]
#                    # Elevation
#                    Elev = float(inputRec[3])
#                    # Width
#                    if is_number(inputRec[4]):
#                        Width = Dbl(inputRec[4])
#                    else:
#                        Width = 0
#                    # Feature Code
#                    FCode = inputRec[5]

#                    # Write values to output shapefile
#                    with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Point) as outputCursor:
#                       # Insert the feature
#                       outputCursor.insertRow((x, y, AssetCode, munID, FCode, Elev, Width))

#            # Stop the edit operation
#            editShapefile.stopOperation()
#            # Stop the edit session and save the changes
#            editShapefile.stopEditing(True)


#            # -----------------------------------------------------------------------------------------------------------------------------------------------------------
#            tabTRN_L = "AssetDetails_TRN_L"
#            queryTRN_L = "\"FC\" IN ('FL','FL-S','STGR','STGR-S','SB','SB-S','RRCB-A','RRCB-A-S','RRCB-C','RRCB-C-S','RRRD-A','RRRD-A-S','RRGR','RRGR-S','RRBW-W','RRBW-W-S','RRDR-A','RRDR-A-S','RRPW','RRPW-S','RRSW-C','RRSW-C-S','RRSW-A','RRSW-A-S','RRSW-B','RRSW-B-S','RRTR','RRTR-S','RRSW','RRSW-S')"
#            arcpy.MakeTableView_management(tabAssetDetails, tabTRN_L, queryTRN_L)
#            countTRN_L = arcpy.GetCount_management(tabTRN_L).getOutput(0)
#            if countTRN_L > 0:
#                arcpy.CopyRows_management(tabTRN_L, munFolder + "AssetDetails_TRN_L.dbf")


#            # Make a list of AssetCodes
#            lstAssetCodes = []

#            # Cursor through input table and get a list of asset codes
#            with arcpy.da.SearchCursor(munFolder + "AssetDetails_TRN_L.dbf", inputFields_AssetDetails) as inputCursor:
#                # Cursor through all records to get a unique list
#                for inputRec in inputCursor:
#                    #print inputRec[0]
#                    if inputRec[0] not in lstAssetCodes:
#                        lstAssetCodes.append(inputRec[0])

#            # Output shapefile
#            outputShapeFile = shpFolder + "TRN L/" + shpMunID + " TRN L.shp"

#            # Start editing - without an undo/redo stack
#            editShapefile = arcpy.da.Editor(shpFolder + "TRN L/")
#            editShapefile.startEditing(False, True)
#            # Start an edit operation
#            editShapefile.startOperation()


#            #print "Importing TRN Line asset data..."


#            # For each Asset Code, query the table and make polylines
#            for ac in lstAssetCodes:

#                # Create query
#                queryAssetCode = "\"Asset_Code\" = '" + ac + "'"
#                with arcpy.da.SearchCursor(munFolder + "AssetDetails_TRN_L.dbf", inputFields_AssetDetails, queryAssetCode) as inputCursor:

#                    # Create an empty array
#                    arrayPoints = arcpy.Array()

#                    for inputRec in inputCursor:
#                        # Get Feature Code first
#                        FCode = inputRec[5]

#                        # If FCode has "-S" at the end, create a point and add to the array.
#                        # Then just go to the next record
#                        if "-S" in FCode:
#                            # Northing and Easting coordinates for Start Point
#                            x = inputRec[2]  # Easting
#                            y = inputRec[1]  # Northing
#                            # Create point
#                            pntStart = arcpy.Point(x, y)
#                            # Add start point to the array
#                            arrayPoints.add(pntStart)
#                        else:
#                            # AssetCode
#                            AssetCode = inputRec[0]
#                            # Elevation
#                            Elev = float(inputRec[3])
#                            # Width
#                            if is_number(inputRec[4]):
#                                Width = Dbl(inputRec[4])
#                            else:
#                                Width = 0
#                            # FCode
#                            FCode = inputRec[5]
#                            # Northing and Easting coordinates for next Point
#                            x = inputRec[2]  # Easting
#                            y = inputRec[1]  # Northing
#                            # Create point
#                            pntNext = arcpy.Point(x, y)
#                            # Add to array
#                            arrayPoints.add(pntNext)

#                    # Make sure array has at least 2 points
#                    if arrayPoints.count >= 2:
#                        # Make the line once all points collected (usually just 2)
#                        polyline = arcpy.Polyline(arrayPoints, srNAD83_CSRS_UTM20)

#                        # Write values to output shapefile
#                        with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Line) as outputCursor:
#                            # Insert the feature
#                            outputCursor.insertRow(((polyline), AssetCode, munID, FCode, Elev, Width))


#            # Stop the edit operation
#            editShapefile.stopOperation()
#            # Stop the edit session and save the changes
#            editShapefile.stopEditing(True)


#            # -----------------------------------------------------------------------------------------------------------------------------------------------------------
#            tabWWC_P = "AssetDetails_WWC_P"
#			# Added WWST May 06, 2019 - forgot to add it before
#            queryWWC_P = "\"FC\" IN ('FTTESAN','PMPS','MHCO','MHSA','SEPT','WWCTF','WWCPMP','WWTFGEN','WWSPMP','WWTFAC','WWBSC','WWBLWR','WWTFBLD','WWCCSYS','WWCLCC','WWCLAR','WWCOMP','WWDAFS','WWDAFT','WWELECM','WWFFT','WFLME','WWGDTP','WWISV','WWLAB','WWLAG','WWOFS','WWOXDI','WWPADAE','WWPTNK','WWSBRT','WWSCRC','WWSDB','WWSCM','WWST','WWTLEM')"
#            arcpy.MakeTableView_management(tabAssetDetails, tabWWC_P, queryWWC_P)
#            countWWC_P = arcpy.GetCount_management(tabWWC_P).getOutput(0)
#            if countWWC_P > 0:
#                arcpy.CopyRows_management(tabWWC_P, munFolder + "AssetDetails_WWC_P.dbf")


#            # Output shapefile
#            outputShapeFile = shpFolder + "WWC P/" + shpMunID + " WWC P.shp"

#            # Start editing - without an undo/redo stack
#            editShapefile = arcpy.da.Editor(shpFolder + "WWC P/")
#            editShapefile.startEditing(False, True)
#            # Start an edit operation
#            editShapefile.startOperation()


#            #print "Importing WWC Point asset data..."


#            # Cursor through input table and write points to shapefile
#            with arcpy.da.SearchCursor(munFolder + "AssetDetails_WWC_P.dbf", inputFields_AssetDetails) as inputCursor:

#                for inputRec in inputCursor:
#                    # Create shape from Northing and Easting coordinates
#                    x = inputRec[2]  # Easting
#                    y = inputRec[1]  # Northing
#                    # AssetCode
#                    AssetCode = inputRec[0]
#                    # Elevation
#                    Elev = float(inputRec[3])
#                    # Width
#                    if is_number(inputRec[4]):
#                        Width = Dbl(inputRec[4])
#                    else:
#                        Width = 0
#                    # Feature Code
#                    FCode = inputRec[5]

#                    # Write values to output shapefile
#                    with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Point) as outputCursor:
#                       # Insert the feature
#                       outputCursor.insertRow((x, y, AssetCode, munID, FCode, Elev, Width))

#            # Stop the edit operation
#            editShapefile.stopOperation()
#            # Stop the edit session and save the changes
#            editShapefile.stopEditing(True)


#            # -----------------------------------------------------------------------------------------------------------------------------------------------------------
#            tabWWC_L = "AssetDetails_WWC_L"
#            queryWWC_L = "\"FC\" IN ('GRVPSA','GRVPSA-S','GRVPCO','GRVPCO-S','WWFRCM','WWFRCM-S')"
#            arcpy.MakeTableView_management(tabAssetDetails, tabWWC_L, queryWWC_L)
#            countWWC_L = arcpy.GetCount_management(tabWWC_L).getOutput(0)
#            if countWWC_L > 0:
#                arcpy.CopyRows_management(tabWWC_L, munFolder + "AssetDetails_WWC_L.dbf")

#            # Make a list of AssetCodes
#            lstAssetCodes = []

#            # Cursor through input table and get a list of asset codes
#            with arcpy.da.SearchCursor(munFolder + "AssetDetails_WWC_L.dbf", inputFields_AssetDetails) as inputCursor:

#                # Cursor through all records to get a unique list
#                for inputRec in inputCursor:
#                    if inputRec[0] not in lstAssetCodes:
#                        lstAssetCodes.append(inputRec[0])


#            # Output shapefile
#            outputShapeFile = shpFolder + "WWC L/" + shpMunID + " WWC L.shp"

#            # Start editing - without an undo/redo stack
#            editShapefile = arcpy.da.Editor(shpFolder + "WWC L/")
#            editShapefile.startEditing(False, True)
#            # Start an edit operation
#            editShapefile.startOperation()


#            #print "Importing WWC Line asset data..."


#            # For each Asset Code, query the table and make polylines
#            for ac in lstAssetCodes:

#                # Create query
#                queryAssetCode = "\"Asset_Code\" = '" + ac + "'"
#                with arcpy.da.SearchCursor(munFolder + "AssetDetails_WWC_L.dbf", inputFields_AssetDetails, queryAssetCode) as inputCursor:

#                    # Create an empty array
#                    arrayPoints = arcpy.Array()

#                    for inputRec in inputCursor:
#                        # Get Feature Code first
#                        FCode = inputRec[5]

#                        # If FCode has "-S" at the end, create a point and add to the array.
#                        # Then just go to the next record
#                        if "-S" in FCode:
#                            # Northing and Easting coordinates for Start Point
#                            x = inputRec[2]  # Easting
#                            y = inputRec[1]  # Northing
#                            # Create point
#                            pntStart = arcpy.Point(x, y)
#                            # Add start point to the array
#                            arrayPoints.add(pntStart)
#                        else:
#                            # AssetCode
#                            AssetCode = inputRec[0]
#                            # Elevation
#                            Elev = float(inputRec[3])
#                            # Width
#                            if is_number(inputRec[4]):
#                                Width = Dbl(inputRec[4])
#                            else:
#                                Width = 0
#                            # FCode
#                            FCode = inputRec[5]
#                            # Northing and Easting coordinates for next Point
#                            x = inputRec[2]  # Easting
#                            y = inputRec[1]  # Northing
#                            # Create point
#                            pntNext = arcpy.Point(x, y)
#                            # Add to array
#                            arrayPoints.add(pntNext)

#                    # Make sure array has at least 2 points
#                    if arrayPoints.count >= 2:
#                        # Make the line once all points collected (usually just 2)
#                        polyline = arcpy.Polyline(arrayPoints, srNAD83_CSRS_UTM20)

#                        # Write values to output shapefile
#                        with arcpy.da.InsertCursor(outputShapeFile, outputFields_Shp_Line) as outputCursor:
#                            # Insert the feature
#                            outputCursor.insertRow(((polyline), AssetCode, munID, FCode, Elev, Width))


#            # Stop the edit operation
#            editShapefile.stopOperation()
#            # Stop the edit session and save the changes
#            editShapefile.stopEditing(True)


#        # ====================================================================================================================
#        # End of Survey-method-only code
#        # ====================================================================================================================




#        # ======================================================================
#        # Hard-code the gdb connection
#        # NSGI
#        gdb = "D:/SDEConnect/AssetViewer.sde"

#        # ======================================================================




#        # Check if any features/records for this municipality exist already and truncate them if they do
#        # ==============================================================================================

#        # Set the current workspace
#        arcpy.env.workspace = gdb

#        # Start editing on the output file GDB
#        edit = arcpy.da.Editor(gdb)
#        # Start editing - without an undo/redo stack
#        edit.startEditing(False, False)
#        # Start an edit operation
#        edit.startOperation()


#        # Query the municipality code
#        munQuery = "MunID = '" + munID + "'"


#        # Go through each feature dataset
#        # -------------------------------
#        # Stormwater
#        for fc in arcpy.ListFeatureClasses("", "", "Stormwater"):
#            if not arcpy.TestSchemaLock(fc):
#                # Make a feature layer with any features matching the MunID query
#                fcLayer = fc + "_" + munID
#                arcpy.MakeFeatureLayer_management(fc, fcLayer, munQuery)
#                countMunID = arcpy.GetCount_management(fc + "_" + munID).getOutput(0)
#                #print "Records found in " + fc + ": " + countMunID
#                if countMunID > 0:
#                    # Delete any Stormwater features for that municipality
#                    #print "Deleting " + countMunID + " records in " + fc + "\n"
#                    arcpy.DeleteRows_management(fc + "_" + munID)
#            else:
#                arcpy.AddError("The database is locked by another user or process.")
#                raise Exception

#        # Transportation
#        for fc in arcpy.ListFeatureClasses("", "", "Transportation"):
#            if not arcpy.TestSchemaLock(fc):
#                # Make a feature layer with any features matching the MunID query
#                fcLayer = fc + "_" + munID
#                arcpy.MakeFeatureLayer_management(fc, fcLayer, munQuery)
#                countMunID = arcpy.GetCount_management(fc + "_" + munID).getOutput(0)
#                #print "Records found in " + fc + ": " + countMunID
#                if countMunID > 0:
#                    # Delete any Transportation features for that municipality
#                    #print "Deleting " + countMunID + " records in " + fc + "\n"
#                    arcpy.DeleteRows_management(fc + "_" + munID)
#            else:
#                arcpy.AddError("The database is locked by another user or process.")
#                raise Exception

#        # Wastewater
#        for fc in arcpy.ListFeatureClasses("", "", "Wastewater"):
#            if not arcpy.TestSchemaLock(fc):
#                # Make a feature layer with any features matching the MunID query
#                fcLayer = fc + "_" + munID
#                arcpy.MakeFeatureLayer_management(fc, fcLayer, munQuery)
#                countMunID = arcpy.GetCount_management(fc + "_" + munID).getOutput(0)
#                #print "Records found in " + fc + ": " + countMunID
#                if countMunID > 0:
#                    # Delete any Wastewater features for that municipality
#                    #print "Deleting " + countMunID + " records in " + fc + "\n"
#                    arcpy.DeleteRows_management(fc + "_" + munID)
#            else:
#                arcpy.AddError("The database is locked by another user or process.")
#                raise Exception

#        # Water Supply
#        for fc in arcpy.ListFeatureClasses("", "", "WaterSupply"):
#            if not arcpy.TestSchemaLock(fc):
#                # Make a feature layer with any features matching the MunID query
#                fcLayer = fc + "_" + munID
#                arcpy.MakeFeatureLayer_management(fc, fcLayer, munQuery)
#                countMunID = arcpy.GetCount_management(fcLayer).getOutput(0)
#                #print "Records found in " + fc + ": " + countMunID
#                if countMunID > 0:
#                    # Delete any Water Supply features for that municipality
#                    #print "Deleting " + countMunID + " records in " + fc + "\n"
#                    arcpy.DeleteRows_management(fc + "_" + munID)
#            else:
#                arcpy.AddError("The database is locked by another user or process.")
#                raise Exception

#        # Stand-alone tables
#        for tab in arcpy.ListTables():
#            if not arcpy.TestSchemaLock(tab):
#                if "PWS_BoosterStation_Assets" in tab or "PWS_TreatmentFacility_Assets" in tab or "WWC_LiftPumpStation_Assets" in tab or "WWC_TreatmentFacility_Assets" in tab:
#                    # Make a table view with any records matching the MunID query
#                    tabView = tab + "_" + munID
#                    arcpy.MakeTableView_management(tab, tabView, munQuery)
#                    countMunID = arcpy.GetCount_management(tabView).getOutput(0)
#                    #print "Records found in " + tab + ": " + countMunID
#                    if countMunID > 0:
#                        # Delete any records in stand-alone tables for that municipality
#                        #print "Deleting " + countMunID + " records in " + tab + "\n"
#                        arcpy.DeleteRows_management(tab + "_" + munID)
#            else:
#                arcpy.AddError("The database is locked by another user or process.")
#                raise Exception


#        # Stop the edit operation
#        edit.stopOperation()

#        # ==============================================================================================


#        # Initialize total counter
#        global totalcounter
#        totalcounter = 0



#        # ====================================================================================================================
#        #
#        # Go into each shapefile folder, find shapefile and join to spreadsheet CSV file
#        subFolders = [x[0] for x in os.walk(shpFolder)]

#        for subFolder in subFolders:

#            # Don't need to do the root folder
#            if subFolder == shpFolder:
#                continue

#            # Start an edit operation
#            edit.startOperation()

#            # Set the workspace to be the current shapefile folder
#            shpWorkspace = subFolder
#            arcpy.env.workspace = shpWorkspace
#            arcpy.env.overwriteOutput = True

#            shapefile = ""

#            if subFolder[-5:] == "PWS L":
#                # Shapefile will be called "<shpMunID> PWS L.shp"
#                shapefile = shpMunID + " PWS L.shp"

#            elif subFolder[-5:] == "PWS P":
#                # Shapefile will be called "<shpMunID> PWS P.shp"
#                shapefile = shpMunID + " PWS P.shp"

#            elif subFolder[-5:] == "SWC L":
#                # Shapefile will be called "<shpMunID> SWC L.shp"
#                shapefile = shpMunID + " SWC L.shp"

#            elif subFolder[-5:] == "SWC P":
#                # Shapefile will be called "<shpMunID> SWC P.shp"
#                shapefile = shpMunID + " SWC P.shp"

#            elif subFolder[-5:] == "TRN L":
#                # Shapefile will be called "<shpMunID> TRN L.shp"
#                shapefile = shpMunID + " TRN L.shp"

#            elif subFolder[-5:] == "TRN P":
#                # Shapefile will be called "<shpMunID> TRN P.shp"
#                shapefile = shpMunID + " TRN P.shp"

#            elif subFolder[-5:] == "WWC L":
#                # Shapefile will be called "<shpMunID> WWC L.shp"
#                shapefile = shpMunID + " WWC L.shp"

#            elif subFolder[-5:] == "WWC P":
#                # Shapefile will be called "<shpMunID> WWC P.shp"
#                shapefile = shpMunID + " WWC P.shp"

#            else:
#                shapefile = ""


#            # Set fc to the shapefile and get shape type
#            fc = shapefile
#            desc = arcpy.Describe(fc)
#            shapeType = desc.shapeType

#            # Coordinate system of shapefiles (NAD83 UTM20)
#            srNAD83_UTM20 = arcpy.SpatialReference(26920)
#            # Coordinate system of GDB feature classes (NAD83 CSRS UTM20)
#            srNAD83_CSRS_UTM20 = arcpy.SpatialReference(2961)
#            # Datum transformation between the two
#            gt = "NAD_1983_To_WGS_1984_1 + NAD_1983_CSRS_To_WGS_1984_2"


#            # If shapefiles already existed (i.e. GIS Method)
#            if shapefilesExist == True:

#                # Project the shapefile to UTM 20 NAD83 CSRS if not already in that coordinate system
#                if arcpy.Describe(fc).spatialReference.factoryCode == 26920:
#                    # Project tool doesn't like spaces, so need to get rid of them
#                    fcProj = fc.replace(" ", "_")[:-4] + "_Proj.shp"
#                    arcpy.Project_management(fc, fcProj, srNAD83_CSRS_UTM20, gt)
#                    # Join the shapefile to the spreadsheet dbf
#                    fcJoin = fc.replace(" ", "_")[:-4] + "_Join"
#                    arcpy.MakeFeatureLayer_management(fcProj, fcJoin)
#                    #shapefileName = fc.replace(" ", "_")[:-4] + "_Proj"
#                    shapefileName = fcProj.replace(" ", "_")[:-4]

#                # If already in UTM 20 NAD83 CSRS, don't need to project
#                elif arcpy.Describe(fc).spatialReference.factoryCode == 2961:
#                    # Join the shapefile to the spreadsheet dbf
#                    fcJoin = fc.replace(" ", "_")[:-4] + "_Join"
#                    arcpy.MakeFeatureLayer_management(fc, fcJoin)
#                    # Commented out 02 May 2019 and replaced with line below it
#                    #shapefileName = fc.replace(" ", "_")[:-4]
#                    shapefileName = fc.replace(" ", " ")[:-4]

#                # Join the shapefile with the dbf based on the GIS_Link field
#                arcpy.AddJoin_management(fcJoin, "GIS_Link", dbfGenAssetInfo, "GIS_Link")

#            else:
#                # Join the shapefile to the spreadsheet dbf
#                fcJoin = fc.replace(" ", "_")[:-4] + "_Join"
#                arcpy.MakeFeatureLayer_management(fc, fcJoin)

#                # Join the shapefile with the dbf based on the AssetCode field
#                arcpy.AddJoin_management(fcJoin, "AssetCode", dbfGenAssetInfo, "Asset_Code")
#                shapefileName = fc[:-4]


#            # Check if the Elevation field is called Elevation, ELEVATION, Elev or ELEV
#            fieldNames = [f.name for f in arcpy.ListFields(fcJoin)]
#            fieldElevName = ""
#            for fieldName in fieldNames:
#                if "Elevation" in fieldName:
#                    fieldElevName = "Elevation"
#                elif "ELEVATION" in fieldName:
#                    fieldElevName = "ELEVATION"
#                elif "Elev" in fieldName:
#                    fieldElevName = "Elev"
#                elif "ELEV" in fieldName:
#                    fieldElevName = "ELEV"



#            # Only some of these fields are necessary for the upload
#            if method == "GIS":
#                shapefilesExist = True
#                inputFields = ["Shape@", shapefileName + "." + fieldElevName, shapefileName + ".Width", \
#                               "GenAssetInfo.Asset_Code", "GenAssetInfo.LocDesc", "GenAssetInfo.FeatureCod", "GenAssetInfo.Condition", \
#                               "GenAssetInfo.Inspected", "GenAssetInfo.Status", "GenAssetInfo.Quantity", "GenAssetInfo.Age", \
#                               "GenAssetInfo.Material", "GenAssetInfo.Comments", "GenAssetInfo.Area", "GenAssetInfo.Department", \
#                               "GenAssetInfo.Division", "GenAssetInfo.PersResp", "GenAssetInfo.Install_yr", "GenAssetInfo.Estimated", \
#                               "GenAssetInfo.RplmtCst", "GenAssetInfo.ConditionB", "GenAssetInfo.ResidValue", "GenAssetInfo.DispDate", \
#                               "GenAssetInfo.Risk", "GenAssetInfo.CnsqOfFail", "GenAssetInfo.FollowUp", "GenAssetInfo.Record_Dra", \
#                               "GenAssetInfo.Replacemen", "GenAssetInfo.CostLookup", "GenAssetInfo.Cost_Facto", "GenAssetInfo.Unit_Cost"]

#            # Need extra AssetCode and FCode fields in case there is no matching record when joined
#            elif method == "Survey":
#                shapefilesExist = False
#                inputFields = ["Shape@", shapefileName + "." + fieldElevName, shapefileName + ".Width", \
#                               "GenAssetInfo.Asset_Code", "GenAssetInfo.LocDesc", "GenAssetInfo.FeatureCod", "GenAssetInfo.Condition", \
#                               "GenAssetInfo.Inspected", "GenAssetInfo.Status", "GenAssetInfo.Quantity", "GenAssetInfo.Age", \
#                               "GenAssetInfo.Material", "GenAssetInfo.Comments", "GenAssetInfo.Area", "GenAssetInfo.Department", \
#                               "GenAssetInfo.Division", "GenAssetInfo.PersResp", "GenAssetInfo.Install_yr", "GenAssetInfo.Estimated", \
#                               "GenAssetInfo.RplmtCst", "GenAssetInfo.ConditionB", "GenAssetInfo.ResidValue", "GenAssetInfo.DispDate", \
#                               "GenAssetInfo.Risk", "GenAssetInfo.CnsqOfFail", "GenAssetInfo.FollowUp", "GenAssetInfo.Record_Dra", \
#                               "GenAssetInfo.Replacemen", "GenAssetInfo.CostLookup", "GenAssetInfo.Cost_Facto", "GenAssetInfo.Unit_Cost", \
#                               shapefileName + ".AssetCode", shapefileName + ".FCode"]


#            # Initialize counter
#            counter = 0



#            # Cursor through input feature class using query
#            with arcpy.da.SearchCursor(fcJoin, inputFields) as inputCursor:

#                # Write values to output feature class
#                for inputRec in inputCursor:

#                    # Get shape
#                    shp = inputRec[0]

#                    # Elevation
#                    if inputRec[1] == None:
#                        Elev = None
#                    elif is_number(inputRec[1]):
#                        Elev = float(inputRec[1])
#                    else:
#                        Elev = None

#                    # Width
#                    if inputRec[2] == None:
#                        Width = None
#                    elif is_number(inputRec[2]):
#                        #Width = int(inputRec[2])
#                        Width = int(round(inputRec[2]))
#                        #Width = float(inputRec[2])
#                    else:
#                        Width = None

#                    # Asset Code
#                    # Depending on whether shapefiles existed (method), get AssetCode from one of two fields
#                    if not inputRec[3] and shapefilesExist == False:
#                        AssetCode = str(inputRec[31])
#                        if AssetCode is not None:
#                            MunID = inputRec[31].split("-")[0]
#                            # Make sure MunID in AssetCode is the same as the current municipality
#                            if MunID == munID:
#                                AssetClass = inputRec[31].split("-")[1]
#                                AssetSubtype = inputRec[31].split("-")[2]
#                            else:
#                                continue
#                        else:
#                            continue
#                    elif str(inputRec[3]) == "" or str(inputRec[3]) == " ":
#                        AssetCode = None
#                        continue
#                    else:
#                        AssetCode = inputRec[3]
#                        NoneType = type(None)
#                        if not isinstance(AssetCode, NoneType):
#                            MunID = inputRec[3].split("-")[0]
#                            # Make sure MunID in AssetCode is the same as the current municipality
#                            if MunID == munID:
#                                AssetClass = inputRec[3].split("-")[1]
#                                AssetSubtype = inputRec[3].split("-")[2]
#                            else:
#                                continue
#                        else:
#                            continue


#                    # Location Description
#                    if not inputRec[4]:
#                        LocDesc = None
#                    elif str(inputRec[4]) == "" or str(inputRec[4]) == " ":
#                        LocDesc = None
#                    else:
#                        LocDesc = str(inputRec[4])

#                    # FCode
#                    if not inputRec[5]:
#                        if shapefilesExist == False:
#                            FCode = str(inputRec[32])
#                        else:
#                            FCode = None
#                    elif str(inputRec[5]) == "" or str(inputRec[5]) == " ":
#                        FCode = None
#                    else:
#                        FCode = str(inputRec[5])

#                    # Condition
#                    if inputRec[6] == None:
#                        Condition = None
#                    elif is_number(inputRec[6]):
#                        if int(inputRec[6]) == 0:
#                            Condition = 0
#                        elif int(inputRec[6]) > 5:
#                            Condition = None
#                        else:
#                            Condition = int(inputRec[6])
#                    else:
#                        Condition = None

#                    # Inspection Date
#                    # There are currently no Inspection Dates in spreadsheets - this may change? Not sure how they will be formatted.
#                    if not inputRec[7]:
#                        InspectDate = None
#                    elif str(inputRec[7]) == "" or str(inputRec[7]) == " ":
#                        InspectDate = None
#                    else:
#                        InspectDate = inputRec[7]

#                    # Status - often in spreadsheets as "active" or "activate" or "Activate"
#                    if not inputRec[8]:
#                        Status = None
#                    elif str(inputRec[8]) == "" or str(inputRec[8]) == " ":
#                        Status = "Active"
#                    elif str(inputRec[8]) == "active" or str(inputRec[8]) == "Active" or str(inputRec[8]) == "activate" or str(inputRec[8]) == "Activate":
#                        Status = "Active"
#                    else:
#                        Status = str(inputRec[8])

#                    # Quantity
#                    if shapeType == "Polyline":
#                        if inputRec[9] == None:
#                            MeasuredLength = None
#                        elif is_number(inputRec[9]):
#                            if inputRec[9] == 0:
#                                MeasuredLength = 0
#                            else:
#                                #MeasuredLength = int(float(inputRec[9]))
#                                MeasuredLength = int(round(float(inputRec[9])))
#                        else:
#                            MeasuredLength = 0
#                    else:
#                        MeasuredLength = 0

#                    # Material
#                    # Check some road and sidewalk/trail fcodes for materials
#                    if FCode in ("RRCB-A", "RRCB-A-S", "RRRD-A", "RRRD-A-S", "RRDR-A", "RRDR-A-S", "RRSW-A", "RRSW-A-S"):
#                        Material = "Asphalt"
#                    elif FCode in ("RRCB-C", "RRCB-C-S", "RRSW-C", "RRSW-C-S"):
#                        Material = "Concrete"
#                    elif FCode in ("RRGR", "RRGR-S"):
#                        Material = "Gravel"
#                    elif FCode in ("RRSW-B", "RRSW-B-S"):
#                        Material = "Brick"
#                    else:
#                        if not inputRec[11]:
#                            Material = "Unknown"
#                        elif str(inputRec[11]) == "" or str(inputRec[11]) == " ":
#                            Material = "Unknown"
#                        else:
#                            Material = str(inputRec[11])

#                    # Comments
#                    if not inputRec[12]:
#                        Comments = None
#                    elif str(inputRec[12]) == "" or str(inputRec[12]) == " ":
#                        Comments = None
#                    else:
#                        Comments = str(inputRec[12])

#                    # Region
#                    if not inputRec[13]:
#                        Region = None
#                    elif str(inputRec[13]) == "" or str(inputRec[13]) == " ":
#                        Region = None
#                    else:
#                        Region = str(inputRec[13])

#                    # Department
#                    if not inputRec[14]:
#                        Dept = None
#                    elif str(inputRec[14]) == "" or str(inputRec[14]) == " ":
#                        Dept = None
#                    else:
#                        Dept = str(inputRec[14])

#                    # Division
#                    if not inputRec[15]:
#                        Division = None
#                    elif str(inputRec[15]) == "" or str(inputRec[15]) == " ":
#                        Division = None
#                    else:
#                        Division= str(inputRec[15])

#                    # Person Responsible
#                    if not inputRec[16]:
#                        PersResp = None
#                    elif str(inputRec[16]) == "" or str(inputRec[16]) == " ":
#                        PersResp = None
#                    else:
#                        PersResp = str(inputRec[16])

#                    # Install Year
#                    if inputRec[17] == None:
#                        InstallYear = None
#                    elif is_number(inputRec[17]):
#                        if inputRec[17] == 0:
#                            InstallYear = None
#                        else:
#                            InstallYear = int(float(inputRec[17]))
#                    else:
#                        InstallYear = None

#                    # Age
#                    if inputRec[10] == None:
#                        Age = None
#                    elif is_number(inputRec[10]):
#                        if inputRec[10] == 0:
#                            Age = None
#                        else:
#                            Age = int(float(inputRec[10]))
#                    else:
#                        Age = None

#                    # Estimated RUL
#                    if inputRec[18] == None:
#                        EstimatedRUL = None
#                    elif is_number(inputRec[18]):
#                        EstimatedRUL = int(inputRec[18])
#                        #EstimatedRUL = int(float(inputRec[18]))
#                    else:
#                        EstimatedRUL = None

#                    # Replacement Cost
#                    if inputRec[19] == None:
#                        ReplacementCost = None
#                    elif is_number(inputRec[19]):
#                        ReplacementCost = float(inputRec[19])
#                    else:
#                        ReplacementCost = None

#                    # Condition Basis
#                    if not inputRec[20]:
#                        ConditionBasis = None
#                    elif str(inputRec[20]) == "" or str(inputRec[20]) == " ":
#                        ConditionBasis = None
#                    else:
#                        ConditionBasis = str(inputRec[20])

#                    # Residual Value
#                    if inputRec[21] == None:
#                        ResidValue = None
#                    elif is_number(inputRec[21]):
#                        #ResidValue = int(inputRec[21])
#                        ResidValue = float(inputRec[21])
#                    else:
#                        ResidValue = None

#                    # Disposal Date
#                    #DisposalDate = inputRec[22]
#                    # There are no Disposal Dates in spreadsheets - this may change?
#                    DisposalDate = None

#                    # Risk
#                    if inputRec[23] == None:
#                        Risk = None
#                    elif is_number(inputRec[23]):
#                        Risk = int(inputRec[23])
#                    else:
#                        Risk = None

#                    # Consequences of Failure
#                    if inputRec[24] == None:
#                        CnsqOfFail = None
#                    elif is_number(inputRec[24]):
#                        CnsqOfFail = int(inputRec[24])
#                    else:
#                        CnsqOfFail = None

#                    # Follow-up Date
#                    #FollowUpDate = inputRec[25]
#                    # Should never be Follow-up Dates in spreadsheets
#                    FollowUpDate = None

#                    # Record Drawing
#                    if not inputRec[26]:
#                        RecordDrawing = None
#                    elif str(inputRec[26]) == "" or str(inputRec[26]) == " ":
#                        RecordDrawing = None
#                    else:
#                        RecordDrawing = str(inputRec[26])

#                    # Replacement Year
#                    if inputRec[27] == None:
#                        ReplacementYear = None
#                    elif is_number(inputRec[27]):
#                        ReplacementYear = int(float(inputRec[27]))
#                    else:
#                        ReplacementYear = None

#                    # Cost Code (lookup)
#                    if not inputRec[28]:
#                        CostCode = None
#                    elif str(inputRec[28]) == "" or str(inputRec[28]) == " ":
#                        CostCode = None
#                    else:
#                        CostCode = str(inputRec[28])

#                    # Cost Factor
#                    if inputRec[29] == None:
#                        CostFactor = None
#                    elif inputRec[29] == 0:
#                        CostFactor = None
#                    elif str(inputRec[29]) == "" or str(inputRec[29]) == " ":
#                        CostFactor = None
#                    else:
#                        CostFactor = str(int(float(inputRec[29])))

#                    # Unit Cost
#                    if inputRec[30] == None:
#                        UnitCost = None
#                    elif is_number(inputRec[30]):
#                        if inputRec[30] == 0:
#                            UnitCost = None
#                        else:
#                            UnitCost = float(inputRec[30])
#                    else:
#                        UnitCost = None


#                    # If certain fields aren't filled out with values, then we need to flag them as Incomplete and set
#                    # a default FollowUp Date of 2 weeks from the day of upload.
#                    Complete = "Yes"
#                    if shapeType == "Point":
#                        if AssetCode == None or AssetClass == None or AssetSubtype == None or FCode == None or LocDesc == None or Status == None or InstallYear == None or Age == None or Condition == None or Condition == 0 or ConditionBasis == None or EstimatedRUL == None or CostCode == None or UnitCost == None or ReplacementCost == None:
#                            Complete = "No"
#                            FollowUpDate = datetime.datetime.now().date() + timedelta(days=14)
#                        else:
#                            Complete = "Yes"
#                            FollowUpDate = None

#                    elif shapeType == "Polyline":
#                        # Need to check for MeasuredLength as well
#                        if AssetCode == None or AssetClass == None or AssetSubtype == None or FCode == None or LocDesc == None or Status == None or InstallYear == None or Age == None or Condition == None or Condition == 0 or ConditionBasis == None or EstimatedRUL == None or CostCode == None or UnitCost == None or ReplacementCost == None or MeasuredLength == 0:
#                            Complete = "No"
#                            FollowUpDate = datetime.datetime.now().date() + timedelta(days=14)
#                        else:
#                            Complete = "Yes"
#                            FollowUpDate = None


#                    # Query the FCode value to see which feature class the feature should go into
#                    outputfc = ""
#                    outputtab = ""
#                    gdbOwner = "ASSETVIEWER."


#                    # Point feature class FCodes
#                    if shapeType == "Point":
#                        if FCode == "CB":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_Catchbasin"
#                        elif FCode == "IO" or FCode == "IO-S":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_InletOutlet"
#                        elif FCode == "LIFT":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_LiftStation"
#                        elif FCode == "MHST":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_Manhole"
#                        elif FCode == "PND":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_Pond"
#                        elif FCode == "TRMTD":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_TreatmentDevice"
#                        elif FCode == "UGS":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_UndergroundStorage"
#                        elif FCode == "STPR":
#                            outputfc = gdb + "/" + gdbOwner + "Transportation/" + gdbOwner + "TRN_Bridge"
#                        elif FCode == "TFSP":
#                            outputfc = gdb + "/" + gdbOwner + "Transportation/" + gdbOwner + "TRN_Sign"
#                        elif FCode == "TFTL":
#                            outputfc = gdb + "/" + gdbOwner + "Transportation/" + gdbOwner + "TRN_Signal"
#                        elif FCode == "TSIG" or FCode == "UTPO" or FCode == "TFSLOR" or FCode == "TFSL":
#                            outputfc = gdb + "/" + gdbOwner + "Transportation/" + gdbOwner + "TRN_Streetlight"
#                        elif FCode == "FTTESAN":
#                            outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_Fitting"
#                        elif FCode == "PMPS":
#                            outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_LiftPumpStation"
#                        elif FCode == "MHCO" or FCode == "MHSA":
#                            outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_Manhole"
#                        elif FCode == "SEPT":
#                            outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_SepticField"
#                        elif FCode == "WWCTF":
#                            outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_TreatmentFacility"
#                        elif FCode in ("WWCPMP", "WWTFGEN", "WWSPMP"):
#                            # Check the contents of the LocDesc field to see what the related feature is
#                            if not LocDesc== None: # If not <Null>
#                                if "-WWC-LPS-PMPS-" in LocDesc:
#                                    outputtab = gdb + "/" + gdbOwner + "WWC_LiftPumpStation_Assets"
#                                elif "-WWC-TRFWW-WWCTF-" in LocDesc:
#                                    outputtab = gdb + "/" + gdbOwner + "WWC_TreatmentFacility_Assets"
#                                else:
#                                    outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_TreatmentFacility"
#                            else: #In case LocDesc is empty, put record here:
#                                outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_TreatmentFacility"
#                        elif FCode in ("WWTFAC", "WWBSC", "WWBLWR", "WWTFBLD", "WWCCSYS", "WWCLCC", "WWCLAR", "WWCOMP", "WWDAFS", "WWDAFT", "WWELECM", "WWFFT", "WWFLME", "WWGDTP", "WWISV", "WWLAB", "WWLAG", "WWOFS", "WWOXDI", "WWPADAE", "WWPTNK", "WWSBRT", "WWSCRC", "WWSDB", "WWSCM", "WWST","WWTLEM"):
#                            outputtab = gdb + "/" + gdbOwner + "WWC_TreatmentFacility_Assets"
#                        elif FCode == "BST":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_BoosterStation"
#                        elif FCode == "CS":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_CorporationStop"
#                        elif FCode == "WV":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_CurbStop"
#                        elif FCode in ("FTBD11", "FTBD22", "FTBD45", "FTBD90", "FTCAP", "FTCP", "FTHY", "FTHYTE", "FTRD", "FTTS", "FTTE"):
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_Fitting"
#                        elif FCode == "HY":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_Hydrant"
#                        elif FCode == "METER":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_MeteringSystem"
#                        elif FCode == "PRV" or FCode == "APV":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_PRV"
#                        elif FCode == "WSST":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_StorageTank"
#                        elif FCode == "WSTF":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_TreatmentFacility"
#                        elif FCode == "FTVLHY" or FCode == "GV":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_Valve"
#                        elif FCode == "WS":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_WaterSource"
#                        elif FCode in ("WSTFAC", "WSCPMP", "WSISV", "WSSPMP"):
#                            # Check the contents of the LocDesc field to see what the related feature is
#                            if not LocDesc == None:  #If not <Null>
#                                if "-PWS-BST-BST-" in LocDesc:
#                                    outputtab = gdb + "/" + gdbOwner + "PWS_BoosterStation_Assets"
#                                elif "-PWS-TRFWS-WSTF-" in LocDesc:
#                                    outputtab = gdb + "/" + gdbOwner + "PWS_TreatmentFacility_Assets"
#                                else:
#                                    outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_TreatmentFacility"
#                            else:  #In case LocDesc is empty, put record here:
#                                outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_TreatmentFacility"
#                        elif FCode in ("WSTFBLD", "WSCCSYS", "WSCLLD", "WSCLAR", "WSCOMP", "WSDAFS", "WSDAFT", "WSELECM", "WSFLME", "WSGDTP", "WSTFGEN", "WSLAB", "WSMFS", "WSMMF", "WSOFS", "WSPTNK", "WSSCM", "WSTLEM", "WSTP", "WSUV", "WSVACCL"):
#                            outputtab = gdb + "/" + gdbOwner + "PWS_TreatmentFacility_Assets"
#                        else:
#                            outputfc = ""
#                            outputtab = ""

#                    # Polyline feature class FCodes
#                    elif shapeType == "Polyline":
#                        if FCode == "CLVT" or FCode == "CLVT-S":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_Culvert"
#                        elif FCode in ("DRCH", "DRCH-S", "RRGT", "RRGT-S"):
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_DrainageChannel"
#                        elif FCode == "GRVPST" or FCode == "GRVPST-S":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_GravityPipe"
#                        elif FCode == "SWFRCM" or FCode == "SWFRCM-S":
#                            outputfc = gdb + "/" + gdbOwner + "Stormwater/" + gdbOwner + "SWC_PressureStormPipe"
#                        elif FCode in ("FL", "FL-S", "STGR", "STGR-S", "SB", "SB-S"):
#                            outputfc = gdb + "/" + gdbOwner + "Transportation/" + gdbOwner + "TRN_BarrierGuardrail"
#                        elif FCode in ("RRCB-A", "RRCB-A-S", "RRCB-C", "RRCB-C-S", "RRRD-A", "RRRD-A-S", "RRGR", "RRGR-S"):
#                            outputfc = gdb + "/" + gdbOwner + "Transportation/" + gdbOwner + "TRN_Road"
#                        elif FCode in ("RRBW-W", "RRBW-W-S", "RRDR-A", "RRDR-A-S", "RRPW", "RRPW-S", "RRSW-C", "RRSW-C-S", "RRSW-A", "RRSW-A-S", "RRSW-B", "RRSW-B-S", "RRTR", "RRTR-S", "RRSW", "RRSW-S"):
#                            outputfc = gdb + "/" + gdbOwner + "Transportation/" + gdbOwner + "TRN_SidewalkTrail"
#                        elif FCode in ("GRVPSA", "GRVPSA-S", "GRVPCO", "GRVPCO-S"):
#                            outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_GravityPipe"
#                        elif FCode == "WWFRCM" or FCode == "WWFRCM-S":
#                            outputfc = gdb + "/" + gdbOwner + "Wastewater/" + gdbOwner + "WWC_PressureSewerPipe"
#                        elif FCode == "DIMN" or FCode == "DIMN-S":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_DistributionPipe"
#                        elif FCode == "TRNS" or FCode == "TRNS-S":
#                            outputfc = gdb + "/" + gdbOwner + "WaterSupply/" + gdbOwner + "PWS_TransmissionPipe"
#                        else:
#                            outputfc = ""
#                            outputtab = ""

#                    #arcpy.AddMessage(outputfc)
#                    #arcpy.AddMessage(outputtab)


#                    # Insert a feature into an output fc or record into an output table
#                    if outputfc != "":
#                        if shapeType == "Point":
#                            with arcpy.da.InsertCursor(outputfc, outputFields_Point) as outputCursor:
#                                # Insert the feature
#                                outputCursor.insertRow([shp, AssetCode, MunID, AssetClass, AssetSubtype, FCode, LocDesc, Elev, Status, Material, CostFactor, Width, InstallYear, Age, Condition, ConditionBasis, InspectDate, EstimatedRUL, ReplacementYear, CostCode, UnitCost, ReplacementCost, ResidValue, DisposalDate, CnsqOfFail, Risk, RecordDrawing, Region, Dept, Division, PersResp, FollowUpDate, Comments, Complete])

#                        elif shapeType == "Polyline":
#                            with arcpy.da.InsertCursor(outputfc, outputFields_Line) as outputCursor:
#                                # Insert the feature
#                                outputCursor.insertRow([shp, AssetCode, MunID, AssetClass, AssetSubtype, FCode, LocDesc, Status, Material, CostFactor, Width, MeasuredLength, InstallYear, Age, Condition, ConditionBasis, InspectDate, EstimatedRUL, ReplacementYear, CostCode, UnitCost, ReplacementCost, ResidValue, DisposalDate, CnsqOfFail, Risk, RecordDrawing, Region, Dept, Division, PersResp, FollowUpDate, Comments, Complete])

#                    if outputtab != "":
#                        if outputtab == gdb + "/" + gdbOwner + "PWS_BoosterStation_Assets":
#                            with arcpy.da.InsertCursor(outputtab, outputFields_Table_BST) as outputCursor:
#                                # Insert the record (no geometry)
#                                outputCursor.insertRow([AssetCode, MunID, AssetClass, AssetSubtype, FCode, LocDesc, Status, Material, CostFactor, Width, InstallYear, Age, Condition, ConditionBasis, InspectDate, EstimatedRUL, ReplacementYear, CostCode, UnitCost, ReplacementCost, ResidValue, DisposalDate, CnsqOfFail, Risk, RecordDrawing, Region, Dept, Division, PersResp, FollowUpDate, Comments, LocDesc, Complete])

#                        elif outputtab == gdb + "/" + gdbOwner + "PWS_TreatmentFacility_Assets":
#                            with arcpy.da.InsertCursor(outputtab, outputFields_Table_WSTF) as outputCursor:
#                                # Insert the record (no geometry)
#                                outputCursor.insertRow([AssetCode, MunID, AssetClass, AssetSubtype, FCode, LocDesc, Status, Material, CostFactor, Width, InstallYear, Age, Condition, ConditionBasis, InspectDate, EstimatedRUL, ReplacementYear, CostCode, UnitCost, ReplacementCost, ResidValue, DisposalDate, CnsqOfFail, Risk, RecordDrawing, Region, Dept, Division, PersResp, FollowUpDate, Comments, LocDesc, Complete])

#                        elif outputtab == gdb + "/" + gdbOwner + "WWC_LiftPumpStation_Assets":
#                            with arcpy.da.InsertCursor(outputtab, outputFields_Table_LPS) as outputCursor:
#                                # Insert the record (no geometry)
#                                outputCursor.insertRow([AssetCode, MunID, AssetClass, AssetSubtype, FCode, LocDesc, Status, Material, CostFactor, Width, InstallYear, Age, Condition, ConditionBasis, InspectDate, EstimatedRUL, ReplacementYear, CostCode, UnitCost, ReplacementCost, ResidValue, DisposalDate, CnsqOfFail, Risk, RecordDrawing, Region, Dept, Division, PersResp, FollowUpDate, Comments, LocDesc, Complete])

#                        elif outputtab == gdb + "/" + gdbOwner + "WWC_TreatmentFacility_Assets":
#                            with arcpy.da.InsertCursor(outputtab, outputFields_Table_WWCTF) as outputCursor:
#                                # Insert the record (no geometry)
#                                outputCursor.insertRow([AssetCode, MunID, AssetClass, AssetSubtype, FCode, LocDesc, Status, Material, CostFactor, Width, InstallYear, Age, Condition, ConditionBasis, InspectDate, EstimatedRUL, ReplacementYear, CostCode, UnitCost, ReplacementCost, ResidValue, DisposalDate, CnsqOfFail, Risk, RecordDrawing, Region, Dept, Division, PersResp, FollowUpDate, Comments, LocDesc, Complete])

#                    # Update counter
#                    counter = counter + 1
#                    #arcpy.AddMessage("Counter: " + str(counter))


#            # Add counter to totalcounter
#            totalcounter = totalcounter + counter

#            # Stop the edit operation
#            edit.stopOperation()


#            # Clean up ??
#            arcpy.RemoveJoin_management(fcJoin)
#            del outputCursor
#            #del outputfc
#            #del outputtab
#            del counter
#            del shapeType
#            del inputFields


#        # Use this to save ? so that it can be displayed in Dashboard
#        arcpy.AddMessage("Total records processed and uploaded: " + str(totalcounter))

#        # Stop the edit session and save the changes
#        edit.stopEditing(True)


#        # ###################################################################################
#        # Import the UnitCost sheet into the UnitCost table for the municipality
#        # ###################################################################################

#        # Have to get actual spreadsheet for the UnitCost information, convert to a CSV, then to a DBF and then load into UnitCost table

#        # Find spreadsheet and the Unit Cost sheet, export to a CSV in the municipality folder
#        for file in os.listdir(munFolder):
#            if file.endswith(".xlsm") and file.startswith(munID):
#                fileSpreadsheet = munFolder + file
#                break

#        wb = xlrd.open_workbook(fileSpreadsheet)
#        sheet = wb.sheet_by_name("Unit Cost")
#        csvUnitCost = open(munFolder + "UnitCost.csv", "wb")
#        wr = csv.writer(csvUnitCost, quoting=csv.QUOTE_ALL)

#        # Need to write header manually since sheet has merged rows and won't export perfectly
#        wr.writerow(("Field1","Item","Lookup Code","Cost Factor","Life","Unit","Base Cost","Field2","Total Cost","Field4","Field5","Field6","Field7","Field8","Field9","Field10","Field11"))


#        # Write remaining rows with data
#        for rownum in xrange(sheet.nrows):
#            # Skip the first two rows
#            if rownum == 0 or rownum == 1:
#                continue
#            # Write other row values to CSV
#            wr.writerow(sheet.row_values(rownum))


#        # Close the spreadsheet and CSV
#        wb.release_resources()
#        del wb
#        csvUnitCost.close()



#        # The sheet/CSV has too many empty or unneeded columns, so will only take ones we need
#        # Need to export to a new CSV in the municipality folder
#        #global munName
#        f = pd.read_csv(munFolder + "UnitCost.csv")
#        keep_col = ["Item", "Lookup Code", "Cost Factor", "Life", "Unit", "Base Cost", "Total Cost"]
#        new_f = f[keep_col]
#        new_f.to_csv(munFolder + "UnitCost_" + munID + ".csv", index=False)

#        # Will create a temporary DBF in the municipality folder
#        dbfFile = munFolder + "UnitCost_" + munID + ".dbf"
#        # Delete if already there
#        if os.path.isfile(dbfFile):
#            os.remove(dbfFile)
#        # Might also be a dbf.xml file
#        if os.path.isfile(munFolder + "UnitCost_" + munID + ".dbf.xml"):
#            os.remove(munFolder + "UnitCost_" + munID + ".dbf.xml")
#        # Convert CSV to DBF
#        arcpy.TableToTable_conversion(munFolder + "UnitCost_" + munID + ".csv", munFolder, "UnitCost_" + munID + ".dbf")

#        # Truncate UnitCost table in the GDB before loading new data in
#        arcpy.env.workspace = gdb
#        # Get corresponding UnitCost table for the municipality from the GDB
#        unitCostTab = gdbOwner + "UnitCost_" + munID
#        arcpy.TruncateTable_management(unitCostTab)


#        # Start editing - without an undo/redo stack
#        edit.startEditing(False, False)

#        # Start another edit operation on GDB
#        edit.startOperation()

#        # Input fields from DBF and output GDB fields
#        inputDBFFields = ["Item", "Lookup_Cod", "Cost_Facto", "Life", "Unit", "Base_Cost", "Total_Cost"]
#        outputGDBFields = ["ItemDesc", "CostCode", "CostFactor", "UsefulLife", "Unit", "BaseCost", "TotalCost"]

#        # Initialize counter (might not need this)
#        unitCostCounter = 0


#        # Cursor through input dbf
#        with arcpy.da.SearchCursor(munFolder + "UnitCost_" + munID + ".dbf", inputDBFFields) as inputDBFCursor:

#            # Write values to output feature class
#            for inputDBFRec in inputDBFCursor:

#                # To get rid of the rows with blank values at the end of CSV/DBF - skip over these
#                if inputDBFRec[0] == " ":
#                    continue
#                else:
#                    # Item
#                    Item = inputDBFRec[0]

#                    # Cost Code (Lookup Code)
#                    if inputDBFRec[1] == "" or inputDBFRec[1] == " ":
#                        CostCode = None
#                    else:
#                        CostCode = inputDBFRec[1]

#                    # Cost Factor
#                    if inputDBFRec[2] == "" or inputDBFRec[2] == " ":
#                        CostFactor = None
#                    else:
#                        if is_number(inputDBFRec[2]):
#                            CostFactor = float(inputDBFRec[2])
#                            CostFactor = int(CostFactor)
#                        else:
#                            CostFactor = inputDBFRec[2]

#                    # Useful Life
#                    if str(inputDBFRec[3]) == "" or str(inputDBFRec[3]) == " ":
#                        UsefulLife = None
#                    else:
#                        if is_number(inputDBFRec[3]):
#                            UsefulLife = int(inputDBFRec[3])
#                        else:
#                            UsefulLife = None

#                    # Unit
#                    if inputDBFRec[4] == "" or inputDBFRec[4] == " ":
#                        Unit = None
#                    else:
#                        Unit = inputDBFRec[4]

#                    # Base Cost
#                    if str(inputDBFRec[5]) == "" or str(inputDBFRec[5]) == " ":
#                        BaseCost = None
#                    else:
#                        BaseCost = inputDBFRec[5]

#                    # Total Cost
#                    if str(inputDBFRec[6]) == "" or str(inputDBFRec[6]) == " ":
#                        TotalCost = None
#                    else:
#                        TotalCost = inputDBFRec[6]

#                    # Write values to UnitCost table in GDB
#                    with arcpy.da.InsertCursor(unitCostTab, outputGDBFields) as unitCostCursor:
#                        # Insert the record
#                        unitCostCursor.insertRow([Item, CostCode, CostFactor, UsefulLife, Unit, BaseCost, TotalCost])
#                        # Update counter
#                        unitCostCounter = unitCostCounter + 1



#        # Stop the edit operation
#        edit.stopOperation()


#        # Stop the edit session and save the changes
#        edit.stopEditing(True)



#        # Clean up
#        del unitCostCursor
#        del unitCostTab
#        del outputGDBFields
#        del unitCostCounter

#        # Status
#        UploadStatus = "Upload Successful"

#        # Send email
#        NotifyClient(munFullName, "", "", UploadStatus)



#    except arcpy.ExecuteError:

#        arcpy.AddMessage(arcpy.GetMessages(2))
#        UploadStatus = "Upload Failed: " + "\n" + arcpy.GetMessages(2)

#        # Abort edit operation
#        if "edit" in locals() or "edit" in globals():
#        #if edit is not None:
#        #if not edit == None:
#            if edit.isEditing == "true":
#                edit.abortOperation()
#                # Stop the edit session without saving any changes
#                edit.stopEditing(False)

#        # Send email
#        NotifyClient(munFullName, "", "", UploadStatus)


#    except Exception, e:

#        UploadStatus = "ERROR: Exception on line number:" + str(sys.exc_traceback.tb_lineno) + "\n" + str(e) + "\n"
#        #NotifyClient(munFullName, None, None, UploadStatus)
#        NotifyClient(munFullName, "", "", UploadStatus)

#        # Abort edit operation
#        if "edit" in locals() or "edit" in globals():
#        #if edit is not None:
#        #if not edit == None:
#            if edit.isEditing == "true":
#                edit.abortOperation()
#                # Stop the edit session without saving any changes
#                edit.stopEditing(False)


#def NotifyClient(munFullName, errorFilenameShort, errorFilename, UploadStatus):

#    arcpy.AddMessage("Sending email...")

#    # Get the email parameter
#    email = arcpy.GetParameterAsText(2)

#    # From email address
#    fromaddr = "noreply@gov.ns.ca"
#    toaddr = email

#    msg = MIMEMultipart()
#    msg["From"] = fromaddr
#    msg["To"] = toaddr
#    msg["Subject"] = munFullName + ": Infrastructure Registry for Municipal Assets Upload Tool"

#    # Attach csv error file if there were validation errors
#    if UploadStatus == "Upload Successful":
#        body = "Upload Status: " + UploadStatus + "\n\n" + "Total records processed and uploaded: " + str(totalcounter) + "\n" + "Your data will refresh as soon as you zoom or pan around in the map."
#        msg.attach(MIMEText(body, "plain"))

#    elif UploadStatus == "Validation Failed":
#        body = "Upload Status: " + UploadStatus + "\n" + "See attached error log file."
#        msg.attach(MIMEText(body, "plain"))
#        filename = errorFilenameShort
#        attachment = open(errorFilename, "rb")
#        part = MIMEBase("application", "octet-stream")
#        part.set_payload((attachment).read())
#        encoders.encode_base64(part)
#        part.add_header("Content-Disposition", "attachment; filename = %s" % filename)
#        msg.attach(part)

#    elif "Cannot acquire a lock" in UploadStatus:
#        body = "Upload Status: Upload Failed." + "\n" + "The database is currently in use by another user or process." + "\n"
#        msg.attach(MIMEText(body, "plain"))

#    else:
#        body = "Upload Status: " + UploadStatus + "\n"
#        msg.attach(MIMEText(body, "plain"))


#    # Email server for government
#    server = smtplib.SMTP("mail.gov.ns.ca", 25)
###    server.starttls()
###    server.login(fromaddr, "")
#    text = msg.as_string()
#    server.sendmail(fromaddr, toaddr, text)
#    server.quit()


#if __name__ == '__main__':
#    main()
