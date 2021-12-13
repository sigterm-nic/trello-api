"""Test Trello Models"""
import random
import string

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import pytest

from trello.models import TrelloSettings, TrelloBoard, TrelloList, TrelloCard

def create_token(length: int):
    """Generate psuedo-random password"""
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(length)
    )

@pytest.mark.django_db
def test_trello_board_model():
    board = TrelloBoard(name="My Board", trello_id="")
    board.save()
    assert board.name == "My Board"
    assert board.trello_id == ""


@pytest.mark.django_db
def test_board_settings_model_token_validation():
    with pytest.raises(ValidationError, match=r"Ensure this value has at least 32 characters.*"):
        TrelloSettings(trello_api_key=create_token(16), trello_api_token=create_token(64), trello_board_id=create_token(24)).full_clean()

    with pytest.raises(ValidationError, match=r"Ensure this value has at least 64 characters."):
        TrelloSettings(trello_api_key=create_token(32), trello_api_token=create_token(32), trello_board_id=create_token(24)).full_clean()


@pytest.mark.django_db
def test_board_settings_model_singleton():
    TrelloSettings(trello_api_key=create_token(32), trello_api_token=create_token(64), trello_board_id=create_token(24)).save()
    with pytest.raises(IntegrityError):
        TrelloSettings(trello_api_key=create_token(32), trello_api_token=create_token(64), trello_board_id=create_token(24)).save()


# @pytest.mark.django_db
# def test_trello_board_model_fetch():
#     valid_api_reponse_snippet = {
#         "": ""
#     }