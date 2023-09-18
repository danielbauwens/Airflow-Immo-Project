import pandas as pd
import numpy as np

def cleaning(df):
    '''Holds the code to clean and pre-process our scraped data before training our ML model on it.'''

    # Filling NaN values with 0.
    df['landplot'] = df['landplot'].fillna(0)
    df['facades'] = df['facades'].fillna(0)
    df['Living area'] = df['Living area'].fillna(0)
    #df = df.fillna(0)
    # Reduces zip codes to 2 digits for broader scope.
    df['Zip code'] = (df['Zip code']/100).astype(int)

    # Creating dummy columns from categorical data.
    df = pd.get_dummies(df, columns=['condition', 'province', 'Zip code', 'subtype'])

    # Removing features that we won't be using.
    df = df.drop(['city', 'Kitchen', 'Terrace', 'type'], axis=1)

    # Because 'get_dummies()' creates boolean values, we re-define our dataframe to be integers only.
    df = df.astype(int)
    return df

def cleanup(df, predict):
    df = pd.concat([df, pd.DataFrame(predict, index=[0])],ignore_index=True)
    df = df.fillna(0)
    df = cleaning(df)
    return df