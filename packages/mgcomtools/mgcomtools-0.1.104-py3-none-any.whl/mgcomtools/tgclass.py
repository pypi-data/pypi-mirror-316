import requests

class TelegramClass:
    """
        Initializes the TelegramClass with the provided token and chat ID.

        :param token: The bot's API token provided by Telegram.
        :param chat_id: The unique identifier for the target chat or user.
    """
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send(self, message, parse_mode='HTML'):
        """ Sends a message to the specified chat using the Telegram API. """
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode
        }
        requests.post(url, params=payload)