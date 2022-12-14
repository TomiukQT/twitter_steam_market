from typing import Tuple
from steam_market import steam_market, csgo_item
import tweepy
import os
import re
import time


class TwitterBot:
    def __init__(self) -> None:
        self.last_msg_id = int(os.getenv("TB_LAST_MSG_ID"))
        self.client = self.auth()

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
        new_messages = []
        try:
            messages = self.client.get_direct_message_events().data
            if messages is None or len(messages) <= 0:
                return []

            for msg in messages:
                if msg.id == self.last_msg_id:
                    break
                if re.fullmatch(r'^\d+ .+', str(msg)) is not None:
                    new_messages.append(str(msg))

            if len(new_messages) > 0:
                self.last_msg_id = messages[0].id
                os.environ["TB_LAST_MSG_ID"] = str(messages[0].id)
        except Exception as e:
            print(f'Error at scanning messages: {e}')
        return new_messages

    def process_new_messages(self, messages: []):
        if messages is None or len(messages) == 0:
            return
        for message in messages:
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
                                                      text=f'Query "{query}" returned 0 items')
                else:
                    self.client.create_direct_message(participant_id=sender_id,
                                                      text=f'Query returned {len(items)} items. First is {list(items)[0]}')
            except Exception as e:
                print(f'Error at processing new messages {e}')

                #self.client.create_direct_message(participant_id=sender_id, text='Wrong query or bot is temporarely banned on SteamAPI')

    @staticmethod
    def parse_message(message: str) -> Tuple[str, str]:
        """

        Args:
            message: message to parse
        TODO: Bad input solution
        Returns: id of sender and query

        """
        if re.match(r'[0-9]+ name{[a-zA-Z0-9,_ ()|.-]+}', message) is None:
            raise AttributeError(f'Bad message: {message}')
        try:
            sender_id = message.split(' ')[0]
            query = message.replace(sender_id, '').strip()
        except Exception as e:
            print(f'Error at bot parsing message: {e}')
        return sender_id, query
