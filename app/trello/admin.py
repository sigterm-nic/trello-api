from django.contrib import admin
from django.db import IntegrityError

# Register your models here.
from .models import BoardSettings

@admin.register(BoardSettings)
class BoardAdmin(admin.ModelAdmin):
    # TODO: figure out how to cleanly implement singleton data model, as this
    # breaks in the admin gui when trying to add a second BoardSettings instance
    fields = (
        "trello_api_token", "trello_api_key", "trello_board_name"
    )

    fields = (
        "trello_api_token", "trello_api_key", "trello_board_name"
    )

