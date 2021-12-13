from django.contrib import admin

# Register your models here.
from .models import TrelloSettings

@admin.register(TrelloSettings)
class BoardAdmin(admin.ModelAdmin):
    # TODO: figure out how to cleanly implement singleton data model, as this
    # breaks in the admin gui when trying to add a second BoardSettings instance
    fields = (
        "trello_api_token", "trello_api_key", "trello_board_id"
    )

    fields = (
        "trello_api_token", "trello_api_key", "trello_board_id"
    )

