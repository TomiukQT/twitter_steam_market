import requests
import os
from csgo_item import CSGOItem
from common import get_nested

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


def get_item_listing(appid: int, name: str, currency: str = 'EUR') -> []:
    r"""
        Function inspired from: https://github.com/MatyiFKBT/PySteamMarket
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
    url = f'https://steamcommunity.com/market/listings/{appid}/{name}/render/'
    item_listing = requests.get(url, params={
        'query': '',
        'start': '0',
        'count': '100',
        'country': 'US',
        'language': 'english',
        'currency': curAbbrev[currency],
        'filter': '',
        })
    print(item_listing.url)
    item_listing_json = item_listing.json()
    item_listing_json.pop('results_html')
    item_listing_json.pop('hovers')
    item_listing_json.pop('currecy')
    item_listing_json.pop('app_data')

    csgo_items = {}

    inspect_links = {}
    assets = get_nested(item_listing_json, 'assets', '730', '2')
    for key in assets.keys():
        item_info = assets[key]
        inspect_links[key] = get_nested(item_info, key, 'actions', '0', 'link')

    listing_info = item_listing_json['listinginfo']
    for key in listing_info.keys():
        item_
        csgo_items[key] = CSGOItem(key, listing_info[key]['asset']['id'])



    return item_listing_json

