import pandas as pd
import numpy as np
import seaborn
from sklearn.preprocessing import MinMaxScaler
def drop_null(df):
    for i in ['objid', 'ra', 'dec', 'u', 'g', 'r', 'i', 'z', 'run', 'rerun', 'camcol',
       'field', 'specobjid', 'redshift', 'plate', 'mjd', 'fiberid']:
        df[i] = df[i].fillna(round(df[i].dropna().astype('float64').mean(),2))
    return df
def duplicated_remove(df):
    df = df.drop(['rerun'], axis=1)
    dups = df.duplicated()
    df.drop_duplicates(inplace=True)
    # We have to reset indexes because our dataframe still having previous indexes after dropping rows
    df=df.reset_index(drop=True)
    return df

def Normalize(df):
    min_max=MinMaxScaler()
    df=min_max.fit_transform(df)
    return df

