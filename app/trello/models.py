from django.db import models
from django.utils.functional import classproperty
from django.core.validators import MinLengthValidator

import trello.client as client
from trello.exceptions import NoBoardConfigurationError


class SingletonModel(models.Model):
    _singleton = models.BooleanField(default=True, unique=True, editable=False)

    class Meta:
        abstract = True


# Create your models here.
class TrelloSettings(SingletonModel):
    """Singleton data model to store Trello configuration parameters"""
    trello_api_token = models.CharField(max_length=64, unique=True, validators=[MinLengthValidator(64)])
    trello_api_key = models.CharField(max_length=32, unique=True, validators=[MinLengthValidator(32)])
    trello_board_id = models.CharField(max_length=24, unique=True, validators=[MinLengthValidator(24)])

    @classproperty
    def trello_config(cls):
        result = cls.objects.first()
        if not result:
            raise NoBoardConfigurationError
        return result


class TrelloBoard(models.Model):
    """Minimal data structure required to represent a board for our UI"""
    trello_id = models.CharField(max_length=24, unique=True, validators=[MinLengthValidator(24)])
    name =  models.TextField()

    @classmethod
    def fetch(cls):
        board_config = TrelloSettings.trello_config

        try:
            board = client.TrelloClient().request("get", f"boards/{board_config.trello_board_id}")
        except client.TrelloAPIError as err:
            raise

        return cls(trello_id=board["id"], name=board["name"])


class TrelloList(models.Model):
    """Minimal data structure required to represent a list for our UI"""
    trello_id = models.CharField(max_length=24, unique=True)
    name =  models.TextField()
    position = models.FloatField(default=0)
    tboard = models.ForeignKey(TrelloBoard, to_field="trello_id", on_delete=models.CASCADE)


    @classmethod
    def fetchall(cls, tboard: TrelloBoard):
        """Return a list of TrelloList instances for all lists associated with a board"""
        # TODO: filter on active lists

        try:
            all_lists = client.TrelloClient().request("get", f"boards/{tboard.trello_id}/lists")
        except client.TrelloAPIError as err:
            raise

        return [cls(trello_id=x["id"], name=x["name"], position=x["pos"], tboard=tboard) for x in all_lists]


class TrelloCard(models.Model):
    """Minimal data structure required to represent a card for our UI"""
    trello_id = models.CharField(max_length=24, unique=True)
    name =  models.TextField()
    position = models.FloatField()
    tlist = models.ForeignKey(TrelloList, to_field="trello_id", on_delete=models.CASCADE)

    @classmethod
    def fetchall(cls, tlist: TrelloList):
        """Return a list of TrelloCard instances for all lists assoctiated with a board"""

        try:
            all_cards = client.TrelloClient().request("get", f"lists/{tlist.trello_id}/cards")
        except client.TrelloAPIError as err:
            raise

        return [cls(trello_id=x["id"], name=x["name"], position=x["pos"], tlist=tlist) for x in all_cards]
