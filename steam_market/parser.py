import re
from typing import Tuple


class Parser:
    @staticmethod
    def parse_stickers(item_info) -> []:
        stickers = []
        for sticker in item_info['stickers']:
            stickers.append(sticker['name'])
        return stickers

    @staticmethod
    def parse_inspect_link(link: str) -> Tuple[str, str]:

        m = ''
        d = re.search('D(\d+)', link).group(1)
        return m, d


