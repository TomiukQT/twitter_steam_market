import requests
import os

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


def get_item_history(appid: int, name: str, currency: str = 'EUR') -> []:
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
            "success": true,
            "price_prefix": "",
            "price": "€",
            "prices": "[
            ["Aug 10 2014 01: +0",11.605,"1159"],
            ["Aug 11 2014 01: +0",11.65,"1100"],
            ...,
            ]"
        }
        ```
        """
    url = 'https://steamcommunity.com/market/listings/730/Recoil%20Case'
    #url = 'https://steamcommunity.com/market/pricehistory'
    #cookie = {'steamLoginSecure': os.environ.get('STEAM_LOGIN_COOKIES')}

    #market_item_history = requests.get(url, cookies=cookie, params={
    #    'appid': appid,
    #    'market_hash_name': name,
    #    'currency': curAbbrev[currency]
   # })

   float: 'https://api.csgofloat.com/?m=4022305850956692180&a=27771119298&d=9971090550885451765'
   list: 'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20The%20Empress%20(Field-Tested)/render/?query=&start=0&count=100&country=US&language=english&currency=1&filter='
    ' => 0,
    'count' = > 100,
    'currency' = > 1,
    'market_hash_name' = > "AK-47 | The Empress (Field-Tested)"
    'filter' = > ''
    'https://steamcommunity.com/market/listings/730/AK-47 | The Empress (Field-Tested)/render/?query=&start=0&count=100&country=US&language=english&currency=1&filter='
    market_item_history = requests.get(url)
    return market_item_history.json()
https://api.csgofloat.com/?m=3136147247424375927&a=19190892996&d=9387202219111148413
