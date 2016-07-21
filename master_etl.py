import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


def replace_boolean_values(series=pd.Series):
    """
    A convenience DRY method to accommodate the needs of Google Sheets/JavaScript. 
    """
    series = series.replace(False, """'no'""")
    series = series.replace(True, """'yes'""")
    return series

def replace_binary_values(series=pd.Series):
    """
    A convenience DRY method to accommodate the needs of Google Sheets/JavaScript. 
    """
    series = series.replace(0, """'no'""")
    series = series.replace(1, """'yes'""")
    return series

def load_master_initial_merge():
    """
    GitHub Issue #3:
    Initial merge is Master SCORP .csv  + GEO .xlsx file. Logic should pull street type and address fields from Geo and overwrite master. 

    """
    scorp_master_file = r"State Comprehensive Outdoor Recreation Plan Inventory of Facilities\MasterSCORP_Base.xlsx"
    geo_master_file = r"State Comprehensive Outdoor Recreation Plan Inventory of Facilities\SCORP_FILTER_GEO.xlsx"
    # State index_col so that data matches correctly.
    sm = pd.read_excel(scorp_master, index_col="OBJECTID")
    gm = pd.read_excel(geo_master_file, index_col="OBJECTID")
    # Take Street type, street, town from geo, where available. 
    sm["Street_Type"] = gm["Street_Type"]
    sm["Street"] = gm["Street"]
    sm['Town'] = gm['Town']

    # Export MasterSCORP_Updated.csv to be new master, then return the dataframe to whomeever called it. 
    export_filename = r"State Comprehensive Outdoor Recreation Plan Inventory of Facilities\MasterSCORP_Updated.csv"
    sm.to_csv(export_filename)
    return sm


def calc_swimming(df):
    """
    GitHub Issue #6
    If pool or beach == 1, 'Swimming' = Y. """

    df["swimming"] = df[["Pool","Beach"]] == 1
    df["swimming"] = replace_boolean_values(df["swimming"])
    return df


def filter_inappropriate_sites(df):
	"""
	If owner == STA and GoRI_TestFlag == (Nan or 0) , filter out.

	"""
    df = ~df[df['OwnerTyp'].str.contains('STA') & df['GoRI_TestFlag'] == nan & df['GoRI_TestFlag'] == nan] # This is a hideous way to do this. 
    # I'll come up with a better one soon.
    df = df[df['GoRI_TestFlag'] != 0] 
    return df

def calc_hiking(df):
	"""
    GitHub Issue #10
	If 'Trails' or 'Walking Path' == 1, 'Hiking' = Y
    Boolean converted to Y/N for GoogleSheets/Javascript purposes.
	"""

    df["Hiking"] = df[["Trails","Walking Path"]] == 1
    df["Hiking"] = replace_boolean_values(df["Hiking"])
    return df

def calc_walking(df):
	"""
    GitHub Issue #14
	If 'Track' or Walking Path' == 1, Walking = Y

	"""
    df["Walking"] = df[["Track","Walking Path","Trails"]] == 1
    df["Walking"] = replace_boolean_values(df["Walking"])
    return df


def calc_running(df):
    """
    If 'Track' or Walking Path' == 1, Running = Y Issue #9
    From @theryankelly in: 

    Current Flag for Running Includes 1 or > from fields:
    "Walking Path"
    "Track"
    "Bike Path"
    "Trails"

    May need to create a running path column beforehand that selects out the walking paths and trails suitable for running. Currently, Cliff Walk (a walking path flag) is but should not be a running path.

    """
    # df["Running"] = df[["Walking Path", "Track", "Bike Path", "Trails"]] == 1
    df["Running"] = df["Walking Path"].combine_first(df["Track"] == 1)
    df["Running"] = df["Running"].combine_first(df["Bike Path"] == 1)
    df["Running"] = df["Running"].combine_first(df["Trails"] == 1)
    df["Running"] = replace_boolean_values(df["Running"])
    return df

def calc_biking(df):
    """
    GitHub Issue #11 per @theryankelly:
        Current Flag for Running (calc_running method above) Includes 1 or > from field: "Bike Path"

    Interesting problem because it's yes if either: 
        1) a calculated field/column contains 'yes'
        2) a base column contains 1.

    Easiest answer is to convert/replace 1/0 for 'yes'/'no' for Bike Path. Added DRY method up top. 

    """
    df["Bike Path"] = replace_binary_values(df["Bike Path"])
    df["Biking"] = df["Running"].combine_first(df["Bike Path"].str.contains('yes'))

    return df


def filter_all_n(df):
    """
    GitHub Issue #15
    Using calculated fields of Running, Swimming, Biking, Paddling, Hiking, Walking and "Type" State Park. Filter list of assets.

    """
    


# def save_new_go_ri(df):



load_master_initial_merge()