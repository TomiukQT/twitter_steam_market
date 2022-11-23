from typing import Tuple
import re
import requests


class CSGOItem:
    def __init__(self, name, item_id, asset_id, price):
        self.name = name
        self.item_id = item_id
        self.asset_id = asset_id
        self.price = price
        self.float = -1
        self.pattern = 'No special pattern'
        self.stickers = 'TBD'

    def get_float(self, link: str) -> None:
        _,d = self.__parse_inspect_link(link)
        url = 'https://api.csgofloat.com/'
        item_info = requests.get(url, params={
            'm': self.item_id,
            'a': self.asset_id,
            'd': d
        }).json()['iteminfo']
        self.float = float(item_info['floatvalue'])
        self.stickers = self.__parse_stickers(item_info)

    def __str__(self):
        return f'N:{self.name} float: {self.float} stickers: {self.stickers}'

    #TODO: Move to another class
    def __parse_stickers(self, item_info) -> []:
        stickers = []
        for sticker in item_info['stickers']:
            stickers.append(sticker['name'])
        return stickers

    def __parse_inspect_link(self, link: str) -> Tuple[str, str]:
        #m = re.search('M(\d+)', link).group(1)
        m = ''
        d = re.search('D(\d+)', link).group(1)
        return m, d
