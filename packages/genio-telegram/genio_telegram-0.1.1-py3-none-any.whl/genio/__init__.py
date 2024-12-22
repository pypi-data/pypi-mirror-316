"""
Genio - A Gen Z-Inspired Telegram MTProto API Framework
"""

from .bot import GenioBot
from .types import Update, Message, Chat

__version__ = "0.1.0"
__all__ = ["GenioBot", "Update", "Message", "Chat"]
