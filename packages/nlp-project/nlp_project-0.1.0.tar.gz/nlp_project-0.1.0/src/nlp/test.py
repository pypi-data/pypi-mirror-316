# for file system import
#from imit_main import imit_signal as imit # for local file import
#from nlp_main import nlp_signal as nlp # for local file import

# for install import
from nlp.imit_main import imit_signal as imit # install import
from nlp.nlp_main import nlp_signal as nlp # install import

import numpy as np
import pandas as pd
import sys

def getSignal(*args):
    try:
        return imit(*args)
    except Exception as e:
        print(e)


data = pd.read_csv('/home/defi/Desktop/portfolio/projects/python/pipeline_defi/indicators/indicators.csv') # ../jupyter/spreadsheets/tuned-indicators.csv

def prep_data():
    train_data = pd.DataFrame()
    for col in data.columns:
        col_name = col.split(' ')[0]
        train_data[f'{col_name}'] = data[col]

    return train_data
df = prep_data()
print(df.head())

df.drop(['Unnamed:'], inplace=True, axis=1)
df['short_kdj'] = df['short_kdj'].astype(int)
#df = df[df['profit_abs'] < 0]
#df = df[df['exit_reason'] == 'trailing_stop_loss']
#df = df[df['enter_reason'] == 'second_buy']
print(df.columns)

df['actions'] = df.apply(lambda row: getSignal(  row['open'], row['high'], row['ema-26'], row['ema-12'], row['low'],
                                                row['mean-grad-hist'], row['close'], row['volume'], row['sma-25'],
                                                row['long_jcrosk'], row['short_kdj']
                                              ), axis=1)


# Convert Series to list
#print(df.head())

#string_series = pd.Series(df['buy-imit-long_go_long'].tolist())
string_series = pd.Series(df['actions'].tolist())
# Function to create sliding windows
def sliding_windows(series=string_series, window_size=3):
    for i in range(len(series) - window_size + 1):
        yield series[i:i + window_size]

predictions = [np.nan] * len(string_series)  # Start with NaN, predictions will overwrite later
test_off = df[(df['nlp-enter-long'] == 'do_nothing') & (df['nlp-enter-short'] == 'do_nothing')]
print(len(test_off), len(df))
# Create sliding windows and predict
window_size = 3  # Sliding window size of 5
for i, window in enumerate(sliding_windows(series=string_series, window_size=3)):
    pred = nlp(window)  # Replace with your actual model's predict function
    predictions[i + window_size - 1] = pred

df['nlpreds'] = predictions
#df['grads-compare'] = df['long-entery-gradient'] > df['short-entry-gradient']
accuracy = len(df[df['nlpreds'] == df['actions']]) * 100/len(df)
print(f'accuracy: --> {accuracy} %')
df['reward'] = df['profit_abs']
df.loc[:,'is_short'] = np.where(df['enter_reason'] == 'first_buy', 0, 1)

#df = df[df['nlpreds'] == 'do_nothing']

print(df['nlp-enter-long'].value_counts())
print(' ')
print(df['nlp-enter-short'].value_counts())
print(' ')
#print(df['buy_imit_long'].value_counts())
print(' ')
#print(df['buy_imit_short'].value_counts())
print(' ')
#print(df['grads-compare'].astype(int).value_counts())
print(' ')
print(df['nlpreds'].value_counts())
#print(df['nlp-exit-short'].value_counts())
cols = ['actions', 'nlp-enter-long','nlp-enter-short','profit_abs']
print(df[actions].value_counts())
df.to_csv('../jupyter/spreadsheets/rlhf_011224.csv')