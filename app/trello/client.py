from typing import Dict

from django.conf import settings
import requests

from .exceptions import NoBoardConfigurationError, TrelloAPIError
import trello.models as tm


class TrelloClient:
    """Trello API client"""

    def __init__(self):
        self._get_credentials()

    def _get_credentials(self):
        """Read Trello API details from the database and update class variables"""
        # read from DB
        config = tm.TrelloSettings.trello_config

        # handle no config
        if config is None:
            raise NoBoardConfigurationError

        self.trello_api_key = config.trello_api_key
        self.trello_api_token = config.trello_api_token

    def request(self, method: str, api_path: str, parameters: Dict = None) -> Dict:
        headers = {
            "Accept": "application/json"
        }
        # TODO: No header security
        parameters = {} if parameters is None else parameters
        parameters.update({
            "key": self.trello_api_key,
            "token": self.trello_api_token
        })
        with requests.Session() as session:
            result = session.request(method, f"{settings.TRELLO_API}{api_path}", params=parameters, headers=headers)


        try:
            result.raise_for_status()
        except requests.RequestException as err:
            raise TrelloAPIError from err

        return result.json()