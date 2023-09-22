#import seaborn as sns
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_city_info():
    #ds = pd.read_csv('main_property_data.csv')
    data = requests.get('https://www.metatopos.eu/belgcombiN.html')
    soup = BeautifulSoup(data.content, 'html.parser')
    zipcodes =[]
    cities =[]
    subcities =[]
    provinces =[]
    conscern = soup.find_all("td")
    for i in range(0, len(conscern), 7):
        zipcodes.append(conscern[i].text)
        cities.append(conscern[i+1].text)
        subcities.append(conscern[i+2].text)
        provinces.append(conscern[i+3].text)

    df = pd.DataFrame({'zip': zipcodes, 'city': cities, 'subcity': subcities, 'province': provinces})
    df.to_csv('zipcodes.csv', index=False)

def first_cleanup():
    try:
        ds = pd.read_csv("./data/property_data.csv")
        df = pd.read_csv('./data/zipcodes.csv')
    except:
        pass

    ds = ds.dropna(subset = ['zip'])
    ds = ds.drop_duplicates()
    ds = ds.drop('ID', axis=1)
    ds = ds.drop('city', axis=1)
    ds = ds.drop('garden', axis=1)
    ds = ds.drop('garden_area', axis=1)
    #ds = ds.drop('pool', axis=1)
    ds['pool'] = ds['pool'].fillna(0)
    #ds.drop('type', inplace=True, axis=1)
    #ds.drop('subtype', inplace=True, axis=1)
    ds = ds.drop('saletype', axis=1)
    ds = ds.drop('URL', axis=1)
    #ds.drop('State of the building', inplace=True, axis=1)
    ds['terrace'] = ds['terrace'].fillna(0)
    #ds['Garden'].fillna(0, inplace=True)
    #ds['Garden area'].fillna(0, inplace=True)
    ds['kitchen'] = ds['kitchen'].fillna(0)
    #ds['Type of Sale'].fillna('isUnknown', inplace=True)
    ds['zip'] = ds['zip'].astype(int)
    ds['zip'] = ds['zip'].astype(str)
    df = df.drop(index=df.index[0], axis=0)
    df.drop('subcity', inplace=True, axis=1)
    ds = ds.astype(str)
    df = df.drop_duplicates(subset=['zip'])
    ds1 = ds.sort_values('zip')
    df = df.sort_values('zip')
    merged = pd.merge(ds1, df, on='zip', how='left', left_index=False)
    merged.to_csv('./data/merged_data.csv', index=False)
first_cleanup()