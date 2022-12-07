from typing import Tuple
from steam_market import steam_market, csgo_item
import tweepy
import os
import re
import time


class TwitterBot:
    def __init__(self) -> None:
        self.last_msg_id = self.set_last_message()
        self.client = self.auth()

    def set_last_message(self):
        return int(open('last_message').read())

    def auth(self) -> tweepy.Client:
        """
        Authenticate and create and  APIv2 client

        Returns:
        Authenticated client from tweepy
        """

        client = tweepy.Client(
            consumer_key=os.getenv('TB_API_KEY'),
            consumer_secret=os.getenv('TB_API_KEY_SECRET'),
            access_token=os.getenv('TB_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TB_ACCESS_TOKEN_SECRET')
        )
        return client

    def scan_messages(self) -> []:
        """
        Scan direct messages and make new query if new messages
        Returns:
            list of new messages
        """
        messages = self.client.get_direct_message_events().data
        new_messages = []
        for msg in messages:
            if msg.id == self.last_msg_id:
                break
            if re.fullmatch(r'^\d+ .+', str(msg)) is not None:
                new_messages.append(str(msg))

        else:
            self.last_msg_id = msg.id
            with open('last_message', 'w') as file:
                file.write(self.last_msg_id)

        return new_messages

    def process_new_messages(self, messages: []):
        for message in messages:
            print(message)
            sender_id, query = '', ''

            try:
               sender_id, query = self.parse_message(message)
            except AttributeError:
                print(f'Message {message} wasnt parsed')
                continue

            try:
                items = steam_market.send_query(query)
                if len(items) == 0:
                    pass
                    self.client.create_direct_message(participant_id=sender_id,
                                                      text='Query returned 0 items')
                else:
                    self.client.create_direct_message(participant_id=sender_id,
                                                      text=f'Query returned {len(items)} items. First is {list(items)[0]}')
                time.sleep(5)
            except AttributeError:
                print('Temp Wrong')
                #self.client.create_direct_message(participant_id=sender_id, text='Wrong query or bot is temporarely banned on SteamAPI')

    @staticmethod
    def parse_message(message: str) -> Tuple[str, str]:
        """

        Args:
            message: message to parse
        TODO: Bad input solution
        Returns: id of sender and query

        """
        sender_id = message.split(' ')[0]
        query = message.replace(sender_id, '').strip()
        return sender_id, query


def main():
    bot = TwitterBot()
    messages = bot.scan_messages()
    bot.process_new_messages(messages)


if __name__ == '__main__':
    main()
