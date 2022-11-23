import requests
import os

from common import get_nested
from tqdm import tqdm

try:
    from .csgo_item import CSGOItem  # "myapp" case
except:
    from csgo_item import CSGOItem  # "__main__" case

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
    item_listing = requests.get(url, params={
        'query': '',
        'start': '0',
        'count': '100',
        'country': 'US',
        'language': 'english',
        'currency': curAbbrev[currency],
        'filter': '',
    })
    print(name)
    print(item_listing.url)
    item_listing_json = item_listing.json()
    item_listing_json.pop('results_html')
    item_listing_json.pop('hovers')
    item_listing_json.pop('currency')
    item_listing_json.pop('app_data')

    csgo_items = {}

    inspect_links = {}
    assets = get_nested(item_listing_json, 'assets', '730', '2')
    for key in assets.keys():
        item_info = assets[key]
        inspect_links[key] = get_nested(item_info, 'actions', 0, 'link')

    listing_info = item_listing_json['listinginfo']
    for key in tqdm(listing_info.keys(), desc='Getting float from items'):
        asset_id = listing_info[key]['asset']['id']
        price = (listing_info[key]['converted_price'] + listing_info[key]['converted_fee']) / 100
        inspect_link = get_nested(listing_info, key, 'asset', 'market_actions', 0, 'link')
        print(inspect_link)
        csgo_items[key] = CSGOItem(name, key, asset_id, price)
        csgo_items[key].get_float(inspect_link)

    return csgo_items
