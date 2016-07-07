import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


def load_master():
    scorp_master = r"State Comprehensive Outdoor Recreation Plan Inventory of Facilities\SCORP_FILTER_GEO.xlsx"
    sg = pd.read_excel(scorp_master)
    return sg


def calc_swimming(df):
	"""
    If pool or beach == 1, 'Swimming' = Y.
    """
    df["swimming"] = df[["Pool","Beach"]] == 1
    df["swimming"] = df["swimming"].replace(False,"N")
    df["swimming"] = df["swimming"].replace(True,"Y")
    return df


def filter_inappropriate_sites(df):
	"""
	If owner == STA and GoRI_TestFlag == (Nan or 0) , filter out.

	"""
    df = ~df[df['OwnerTyp'].str.contains('STA') & df['GoRI_TestFlag'] == nan & df['GoRI_TestFlag'] == nan] # This is a hideous way to do this. I'll come up with a better one soon.
    df = df[df['GoRI_TestFlag'] != 0]
    return df

def calc_hiking(df):
	"""
	If 'Trails' or 'Walking Path' == 1, 'Hiking' = Y
    Boolean converted to Y/N for GoogleSheets/Javascript purposes.
	"""

    df["Hiking"] = df[["Trails","Walking Path"]] == 1
    df["Hiking"] = df["Hiking"].replace(False,"N")
    df["Hiking"] = df["Hiking"].replace(True,"Y")
    return df

def calc_walking(df):
	"""
	If 'Track' or Walking Path' == 1, Walking = Y

	"""


def calc_running(df):
    """
    If 'Track' or Walking Path' == 1, Running = Y
    From @theryankelly: 

    Current Flag for Running Includes 1 or > from fields:
    "Walking Path"
    "Track"
    "Bike Path"
    "Trails"

    May need to create a running path column beforehand that selects out the walking paths and trails suitable for running. Currently, Cliff Walk (a walking path flag) is but should not be a running path.

    """
    df["Running"] = df[["Walking Path", "Track", "Bike Path", "Trails"]] == 1
    df["Running"] = df["Running"].replace(False,"N")
    df["Running"] = df["Running"].replace(True,"Y")
    return df