import pandas as pd

def cleaning():
    df = pd.read_csv('./data/merged_data.csv')

    '''Holds the code to clean and pre-process our scraped data before training our ML model on it.'''

    # Filling NaN values with 0.
    df['landplot'] = df['landplot'].fillna(0)
    df['facades'] = df['facades'].fillna(0)
    df['living_area'] = df['living_area'].fillna(0)
    #df = df.fillna(0)
    # Reduces zip codes to 2 digits for broader scope.
    df['zip'] = (df['zip']/100).astype(int)

    # Creating dummy columns from categorical data.
    df = pd.get_dummies(df, columns=['building_state', 'province', 'zip', 'subtype'], dtype=int)
    # Removing features that we won't be using.
    df = df.drop(['city', 'kitchen', 'terrace', 'terrace_area', 'type'], axis=1)

    # Because 'get_dummies()' creates boolean values, we re-define our dataframe to be integers only.
    df.to_csv('./data/processed_data.csv')

def cleanup(df, predict):
    df = pd.concat([df, pd.DataFrame(predict, index=[0])],ignore_index=True)
    df = df.fillna(0)
    df = cleaning(df)
    return df

cleaning()