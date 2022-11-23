from typing import Tuple
import re
import requests


class CSGOItem:
    def __init__(self, item_id, asset_id):
        self.item_id = item_id
        self.asset_id = asset_id
        self.float = -1
        self.pattern = 'No special pattern'
        self.stickers = 'TBD'

    def get_float(self, link: str, asset_id: str):
        m, d = self.__parse_inspect_link(link)
        url = 'https://api.csgofloat.com/?m=4022305850956692180&a=27771119298&d=9971090550885451765'
        item_info = requests.get(url, params={
            'm': m,
            'a': asset_id,
            'd': d
        }).json()['iteminfo']
        self.float = float(item_info['floatvalue'])
        self.stickers = self.__parse_stickers(item_info)

    #Move to another class
    def __parse_stickers(self, item_info) -> []:
        stickers = []
        for sticker in item_info['stickers'].values():
            stickers.append(sticker['Name'])
        return stickers

    def __parse_inspect_link(self, link: str) -> Tuple[str, str]:
        m = re.search('M(\d+)', link).group(1)
        d = re.search('D(\d+)', link).group(1)
        return m, d
