"""
Custom exceptions for the Genio framework.
"""

class GenioError(Exception):
    """Base exception for all Genio errors."""
    pass

class GenioAuthError(GenioError):
    """Raised when authentication with Telegram fails."""
    pass

class GenioNetworkError(GenioError):
    """Raised when network operations fail."""
    pass

class GenioValidationError(GenioError):
    """Raised when input validation fails."""
    pass
