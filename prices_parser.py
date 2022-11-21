import re
import pandas as pd


def parse_date(dates):
    dates.map()
    return


def parse_item_history(item_history: {}):
    prices = item_history['prices']
    df = pd.DataFrame(prices, columns=['date', 'price', 'amount'])
    df['date'] = pd.to_datetime(df['date'], format='%b %d %Y %S: +0').dt.date
    return df

