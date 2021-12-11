from operator import mod
from django.db import models

# Create your models here.
class TrelloBoard(models.Model):
    trello_id = models.CharField(max_length=24, unique=True)
    name =  models.TextField()
    desc = models.TextField('description')


class TrelloList(models.Model):
    trello_id = models.CharField(max_length=24, unique=True)
    name =  models.TextField()
    tboard = models.ForeignKey(TrelloBoard, to_field="trello_id", on_delete=models.CASCADE)
    desc = models.TextField('description')


class TrelloCard(models.Model):
    trello_id = models.CharField(max_length=24, unique=True)
    name =  models.TextField()
    desc = models.TextField('description')
    position = models.FloatField()
    tlist = models.ForeignKey(TrelloList, to_field="trello_id", on_delete=models.CASCADE)
