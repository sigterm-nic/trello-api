from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator


class SingletonModel(models.Model):
    # TODO: cache this model
    _singleton = models.BooleanField(default=True, unique=True, editable=False)

    class Meta:
        abstract = True


# Create your models here.
class TrelloBoard(models.Model):
    trello_id = models.CharField(max_length=24, unique=True)
    name =  models.TextField()


class TrelloList(models.Model):
    trello_id = models.CharField(max_length=24, unique=True)
    name =  models.TextField()
    tboard = models.ForeignKey(TrelloBoard, to_field="trello_id", on_delete=models.CASCADE)


class TrelloCard(models.Model):
    trello_id = models.CharField(max_length=24, unique=True)
    name =  models.TextField()
    position = models.FloatField()
    tlist = models.ForeignKey(TrelloList, to_field="trello_id", on_delete=models.CASCADE)


class BoardSettings(SingletonModel):
    trello_api_token = models.CharField(max_length=64, unique=True, validators=[MinLengthValidator(64)])
    trello_api_key = models.CharField(max_length=32, unique=True, validators=[MinLengthValidator(32)])
    trello_board_id = models.CharField(max_length=24, unique=True, validators=[MinLengthValidator(24)])
