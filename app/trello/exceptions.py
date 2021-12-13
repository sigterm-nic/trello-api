"""Custom exceptions for the application"""
class NoBoardConfigurationError(Exception):
    """Raised when a board has not been configured via the admin portal"""

class TrelloAPIError(Exception):
    """Raised when API request status code > 400"""