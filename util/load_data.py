
import pandas as pd
import sys
sys.path.append('../')


from config.constants import *


# Create a function to load data
def load_data():
    XAUUSD = {}
    XAUUSD['D1'] = pd.read_csv(
        PATH_DATA + SYMBOL['XAUUSD']['D1'] + '.csv', index_col='Time', parse_dates=True)
    XAUUSD['H4'] = pd.read_csv(
        PATH_DATA + SYMBOL['XAUUSD']['H4'] + '.csv', index_col='Time', parse_dates=True)
    XAUUSD['H1'] = pd.read_csv(
        PATH_DATA + SYMBOL['XAUUSD']['H1'] + '.csv', index_col='Time', parse_dates=True)
    XAUUSD['M30'] = pd.read_csv(
        PATH_DATA + SYMBOL['XAUUSD']['M30'] + '.csv', index_col='Time', parse_dates=True)
    XAUUSD['M15'] = pd.read_csv(
        PATH_DATA + SYMBOL['XAUUSD']['M15'] + '.csv', index_col='Time', parse_dates=True)
    XAUUSD['M5'] = pd.read_csv(
        PATH_DATA + SYMBOL['XAUUSD']['M5'] + '.csv', index_col='Time', parse_dates=True)
    XAUUSD['M1'] = pd.read_csv(
        PATH_DATA + SYMBOL['XAUUSD']['M1'] + '.csv', index_col='Time', parse_dates=True)
    return XAUUSD
