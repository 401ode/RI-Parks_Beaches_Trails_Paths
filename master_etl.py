import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


def replace_boolean_values(series):
    """
    A convenience DRY method to accommodate the needs of Google Sheets/JavaScript. 
    """
    series = series.replace(False, "N")
    series = series.replace(True, "F")
    return series


def load_master():
    scorp_master = r"State Comprehensive Outdoor Recreation Plan Inventory of Facilities\SCORP_FILTER_GEO.xlsx"
    sg = pd.read_excel(scorp_master)
    return sg


def calc_swimming(df):
	"""
    GitHub Issue #6
    If pool or beach == 1, 'Swimming' = Y.
    """
    
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
    df["Running"] = df[["Walking Path", "Track", "Bike Path", "Trails"]] == 1
    df["Running"] replace_boolean_values(df["Running"])
    return df

def filter_all_n(df):
    """
    GitHub Issue #15
    Using calculated fields of Running, Swimming, Biking, Paddling, Hiking, Walking and "Type" State Park. Filter list of assets.

    """
    