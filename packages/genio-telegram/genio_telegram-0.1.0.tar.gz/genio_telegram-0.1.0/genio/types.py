"""
Type definitions for Telegram objects.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

@dataclass
class User:
    """Represents a Telegram user."""
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            id=data["id"],
            is_bot=data["is_bot"],
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            username=data.get("username"),
            language_code=data.get("language_code")
        )

@dataclass
class Chat:
    """Represents a Telegram chat."""
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chat':
        return cls(
            id=data["id"],
            type=data["type"],
            title=data.get("title"),
            username=data.get("username"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            description=data.get("description")
        )

@dataclass
class File:
    """Represents a Telegram file."""
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'File':
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            file_size=data.get("file_size"),
            file_path=data.get("file_path")
        )

@dataclass
class PhotoSize(File):
    """Represents a photo size."""
    width: int
    height: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PhotoSize':
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            width=data["width"],
            height=data["height"],
            file_size=data.get("file_size")
        )

@dataclass
class Message:
    """Represents a Telegram message."""
    message_id: int
    chat: Chat
    date: int
    text: Optional[str] = None
    from_user: Optional[User] = None
    reply_to_message: Optional['Message'] = None
    photo: Optional[List[PhotoSize]] = None
    caption: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        reply_msg = None
        if "reply_to_message" in data:
            reply_msg = cls.from_dict(data["reply_to_message"])
            
        photo_sizes = None
        if "photo" in data:
            photo_sizes = [PhotoSize.from_dict(photo) for photo in data["photo"]]
            
        return cls(
            message_id=data["message_id"],
            chat=Chat.from_dict(data["chat"]),
            date=data["date"],
            text=data.get("text"),
            from_user=User.from_dict(data["from"]) if "from" in data else None,
            reply_to_message=reply_msg,
            photo=photo_sizes,
            caption=data.get("caption")
        )

@dataclass
class CallbackQuery:
    """Represents a callback query from an inline keyboard."""
    id: str
    from_user: User
    chat_instance: str
    message: Optional[Message] = None
    data: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CallbackQuery':
        return cls(
            id=data["id"],
            from_user=User.from_dict(data["from"]),
            chat_instance=data["chat_instance"],
            message=Message.from_dict(data["message"]) if "message" in data else None,
            data=data.get("data")
        )

@dataclass
class Update:
    """Represents a Telegram update."""
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Update':
        return cls(
            update_id=data["update_id"],
            message=Message.from_dict(data["message"]) if "message" in data else None,
            edited_message=Message.from_dict(data["edited_message"]) if "edited_message" in data else None,
            callback_query=CallbackQuery.from_dict(data["callback_query"]) if "callback_query" in data else None
        )
