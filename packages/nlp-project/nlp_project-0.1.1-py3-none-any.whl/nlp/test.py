# for file system import
from imit_main import imit_signal as imit # for local file import
from nlp_main import nlp_signal as nlp # for local file import

# for install import
#from nlp.imit_main import imit_signal as imit # install import
#from nlp.nlp_main import nlp_signal as nlp # install import

import numpy as np
import pandas as pd
import sys

def getSignal(*args):
    try:
        return imit(*args)
    except Exception as e:
        print(e)


data = pd.read_csv('/home/defi/Desktop/portfolio/projects/python/pipeline_defi/indicators/indicators.csv') #  ../jupyter/spreadsheets/tuned-indicators.csv

def prep_data():
    train_data = pd.DataFrame()
    for col in data.columns:
        col_name = col.split(' ')[0]
        train_data[f'{col_name}'] = data[col]

    return train_data

df = prep_data()
print(df['exit_reason'].value_counts())

df.drop(['Unnamed:', 'open_date','pair'], inplace=True, axis=1)
df['short_kdj'] = df['short_kdj'].astype(int)
print(df.head())

# Filter what you want to test
#df = df[df['profit_abs'] > 0]
df = df[df['exit_reason'] == 'roi']
df = df[df['enter_reason'] == 'second_buy']
print(df.columns)
'''
df['new-actions'] = df.apply(lambda row: getSignal(  row['open'], row['high'], row['ema-26'], row['ema-12'], row['low'],
                                                row['mean-grad-hist'], row['close'], row['volume'], row['sma-25'],
                                                row['long_jcrosk'], row['short_kdj']
                                              ), axis=1
                    )
'''
df['new-actions'] = df.apply(lambda row: getSignal( row['sma-05'],row['sma-07'],row['sma-25']), axis=1
                    )


# Convert Series to list
#print(df.head())

#string_series = pd.Series(df['buy-imit-long_go_long'].tolist())
string_series = pd.Series(df['new-actions'].tolist())
# Function to create sliding windows
def sliding_windows(series=string_series, window_size=3):
    for i in range(len(series) - window_size + 1):
        yield series[i:i + window_size]

predictions = [np.nan] * len(string_series)  # Start with NaN, predictions will overwrite later
#test_off = df[(df['nlp-enter-long'] == 'do_nothing') & (df['nlp-enter-short'] == 'do_nothing')]
#print(len(test_off), len(df))
# Create sliding windows and predict
window_size = 3  # Sliding window size of 5
for i, window in enumerate(sliding_windows(series=string_series, window_size=3)):
    pred = nlp(window)  # Replace with your actual model's predict function
    predictions[i + window_size - 1] = pred

df['nlpreds'] = predictions
df['nlpreds'].bfill()
accuracy = 0 if len(df) == 0 else len(df[df['new-actions'] == df['nlpreds']]) * 100/len(df)
print(f'accuracy: --> {accuracy} %')
df['reward'] = df['profit_abs']
df.loc[:,'is_short'] = np.where(df['enter_reason'] == 'first_buy', 0, 1)

#df = df[df['nlpreds'] == 'do_nothing']

#print(df['nlp-enter-long'].value_counts())
print(' ')
#print(df['nlp-enter-short'].value_counts())
print(' ')
print(df['imit-exit-short'].value_counts())
print(' ')
print(df['imit-enter-short'].value_counts())
print(' ')
print(df['nlp-enter-short'].value_counts())
print(' ')
#rint(df['nlp-enter-long'].value_counts())
print(df.head())
print(' ')
print(df['nlpreds'].value_counts())
#print(df['nlp-exit-short'].value_counts())
#cols = ['actions', 'nlp-enter-long','nlp-enter-short','profit_abs']
print(df['new-actions'].value_counts())

df.to_csv('../jupyter/spreadsheets/rlhf_20241210.csv')