from typing import Tuple
import re
import requests
from .parser import Parser

class CSGOItem:
    def __init__(self, name, item_id, asset_id, price):
        self.inspect_link = None
        self.name = name
        self.item_id = item_id
        self.asset_id = asset_id
        self.price = price
        self.float = -1
        self.pattern = 'No special pattern'
        self.stickers = 'TBD'

    def get_float(self, link: str) -> None:
        self.inspect_link = link
        _, d = Parser.parse_inspect_link(link)
        url = 'https://api.csgofloat.com/'
        item_info = requests.get(url, params={
            'm': self.item_id,
            'a': self.asset_id,
            'd': d
        }).json()['iteminfo']
        self.float = float(item_info['floatvalue'])
        self.stickers = Parser.parse_stickers(item_info)

    def __str__(self):
        s = f'N:{self.name} float: {self.float} stickers: {self.stickers}'
        return s if self.inspect_link is None else f'{s} >> inspect link: {self.inspect_link}'


