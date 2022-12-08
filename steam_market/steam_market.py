import re

import requests
import os

from common import get_nested
import time


from .csgo_item import CSGOItem  # "myapp" case


curAbbrev = {
    'USD': 1,
    'GBP': 2,
    'EUR': 3,
    'CHF': 4,
    'RUB': 5,
    'KRW': 16,
    'CAD': 20,
}


def get_item(appid, name, currency='EUR'):
    r"""
    Function from: https://github.com/MatyiFKBT/PySteamMarket
    Gets item listings from the `Steam Marketplace`.
    @appid ID of game item belongs to.
    @name: Name of item to lookup.

    @currency: Abbreviation of currency to return listing prices in.
    Accepted currencies:`USD,GBP,EUR,CHF,RUB,KRW,CAD`

    Defaults to `EUR`.
    Please lookup the proper abbreviation for your currency of choice.

    Returns a json object
    Example:
    ```
    {
        "success": true,
        "lowest_price": "0,92€",
        "volume": "15",
        "median_price": "0,80€"
    }
    ```
    """
    url = 'https://steamcommunity.com//market/priceoverview'
    market_item = requests.get(url, params={
        'appid': appid,
        'market_hash_name': name,
        'currency': curAbbrev[currency]
    })
    return market_item.json()


def get_csgo_item_listing(name: str, currency: str = 'EUR') -> []:
    r"""
        Function inspired fom: https://github.com/MatyiFKBT/PySteamMarket
        Gets item price history from the `Steam Marketplace`.
        @appid ID of game item belongs to.
        @name: Name of item to lookup.
        @currency: Abbreviation of currency to return listing prices in.
        Accepted currencies:`USD,GBP,EUR,CHF,RUB,KRW,CAD`

        Defaults to `EUR`.
        Please lookup the proper abbreviation for your currency of choice.

        Returns a json object
        Example:
        ```
        {

        }
        ```
        #float: 'https://api.csgofloat.com/?m=4022305850956692180&a=27771119298&d=9971090550885451765'
        # https://api.csgofloat.com/?m=3136147247424375927&a=19190892996&d=9387202219111148413
        """
    url = f'https://steamcommunity.com/market/listings/730/{name}/render/'
    params = {'query': '',
        'start': '0',
        'count': '100',
        'country': 'US',
        'language': 'english',
        'currency': curAbbrev[currency],
        'filter': ''}

    csgo_items = {}
    first = True
    while True:
        time.sleep(20)
        if not first:
            params['start'] = str(int(params['start']) + 100)
        item_listing = requests.get(url, params=params)
        if item_listing is None or item_listing is []:
            break
        listing_info = item_listing.json()['listinginfo']
        for key in listing_info.keys():
            asset_id = listing_info[key]['asset']['id']
            price = (listing_info[key]['converted_price'] + listing_info[key]['converted_fee']) / 100
            inspect_link = get_nested(listing_info, key, 'asset', 'market_actions', 0, 'link')
            csgo_items[key] = CSGOItem(name, key, asset_id, price)
            csgo_items[key].get_float(inspect_link)
        first = False

    return csgo_items


def send_query(query: str) -> []:
    """
    TODO: Revamp stickers filtering.
    Args:
        query:

    Returns:

    """
    try:
        params = parse_query(query)
        csgo_items = get_csgo_item_listing(params['name'])
        # filter items based on params
        for item_id, item in csgo_items.copy().items():
            float_low, float_high = params['float']
            if not (float_low <= item.float <= float_high):
                csgo_items.pop(item_id)
                continue
            stickers_count_low, stickers_count_high = params['stickers_count']
            if not (stickers_count_low <= len(item.stickers) <= stickers_count_high):
                csgo_items.pop(item_id)
                continue
            for sticker in params['stickers']:
                for sticker_on_item in item.stickers:
                    if sticker in sticker_on_item:
                        break
            else:
                if len(params['stickers']) != 0:
                    csgo_items.pop(item_id)
                    continue
        return csgo_items.values()
    except NameError as e:
        print(e)
        return []
    except Exception as e:
        print(e)
        return []


def parse_query(query: str) -> {}:
    """
    Parse query from user
    Query params: param_name={param_value(s)}
    Message template: name{skin_name} float{low,high} stickers{name or substring of sticker} stickers_count={low,high}
    Message example: name{AK 47 | Redline (Field-Tested)} float{0.4,1} stickers{Katowice 2014} stickers_count={1}
    Args:
        query: query

    Returns: dict of params if at least name provided else None

    """
    params = {
        'name': '',
        'float': (0, 1),
        'stickers': [],
        'stickers_count': (0, 4)
    }
    matches = re.findall(r'([a-z_]+){([a-zA-Z0-9,_ ()|.-]+)}', query)
    for match in matches:
        key, value = match[0], match[1]
        if key not in params.keys():
            print(f'Unknown param {key}')
            continue
        params[key] = parse_param(key, value)
    if params['name'] == '':
        raise NameError('Name is missing') #TODO Change exception
    return params


def parse_param(key: str, value: str):
    match key:
        case 'name':
            return value
        case 'float' | 'stickers_count':
            return tuple(map(lambda x: float(x), value.strip().split(',')))
        case 'stickers':
            return value.split(',')
        case _:
            return None
