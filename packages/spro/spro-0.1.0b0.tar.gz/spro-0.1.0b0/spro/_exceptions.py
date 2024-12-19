# Base exception class
class SProError(Exception):
    """Base exception class for SPro SDK"""


# API-related exceptions
class APIError(SProError):
    """Raised when an API request fails"""


class InvalidEntityError(SProError):
    """Raised when an invalid entity is passed in the request"""


class InvalidAPIKeyError(SProError):
    """Raised when the API key is invalid or expired"""


class AuthenticationError(SProError):
    """Raised when there is an authentication failure"""


class ConfigurationError(SProError):
    """Raised when there's a configuration issue"""


class ValidationError(SProError):
    """Raised when input validation fails"""
