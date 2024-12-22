"""
Core bot class for the Genio framework.
"""
import asyncio
import logging
from typing import Optional, Callable, Dict, Any, List, Union
import aiohttp
import json
from pathlib import Path

from .types import Update, Message, User, Chat, CallbackQuery, PhotoSize, File
from .exceptions import GenioAuthError, GenioNetworkError, GenioValidationError
from .utils import validate_token, build_api_url, parse_response

logger = logging.getLogger(__name__)

class GenioBot:
    """
    Main bot class for interacting with Telegram's API.
    """
    def __init__(self):
        self.token: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._base_url: Optional[str] = None
        self._is_running: bool = False
        self._me: Optional[User] = None

    @classmethod
    async def connect_bot(cls, token: str) -> 'GenioBot':
        """
        Create and authenticate a new bot instance.
        
        Args:
            token: Telegram bot token
            
        Returns:
            Authenticated GenioBot instance
        """
        if not validate_token(token):
            raise GenioValidationError("Invalid bot token format")
            
        bot = cls()
        await bot._authenticate(token)
        return bot

    async def _authenticate(self, token: str) -> None:
        """
        Authenticate the bot with Telegram's API.
        """
        self.token = token
        self._base_url = f"https://api.telegram.org/bot{token}"
        self._session = aiohttp.ClientSession()
        
        try:
            async with self._session.get(f"{self._base_url}/getMe") as resp:
                if resp.status != 200:
                    raise GenioAuthError("Failed to authenticate bot")
                data = await resp.json()
                if not data.get("ok"):
                    raise GenioAuthError("Invalid bot token")
                self._me = User.from_dict(data["result"])
        except Exception as e:
            await self._session.close()
            raise GenioAuthError(f"Authentication failed: {str(e)}")

    async def send_msg(
        self, 
        chat_id: Union[int, str], 
        text: str, 
        parse_mode: Optional[str] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Dict] = None,
        **kwargs
    ) -> Message:
        """
        Send a message to a chat.
        
        Args:
            chat_id: Telegram chat ID
            text: Message text
            parse_mode: Text parsing mode (HTML/Markdown)
            reply_to_message_id: Message to reply to
            reply_markup: Inline keyboard or custom reply keyboard
            **kwargs: Additional message parameters
            
        Returns:
            Sent message object
        """
        payload = {
            "chat_id": chat_id,
            "text": text,
            **kwargs
        }
        
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)
        
        async with self._session.post(f"{self._base_url}/sendMessage", json=payload) as resp:
            data = await resp.json()
            if not data.get("ok"):
                raise GenioNetworkError(f"Failed to send message: {data.get('description')}")
            return Message.from_dict(data["result"])

    async def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[str, Path],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Dict] = None,
        **kwargs
    ) -> Message:
        """
        Send a photo to a chat.
        
        Args:
            chat_id: Telegram chat ID
            photo: Photo file path or file_id
            caption: Photo caption
            parse_mode: Caption parsing mode
            reply_to_message_id: Message to reply to
            reply_markup: Inline keyboard or custom reply keyboard
            **kwargs: Additional parameters
            
        Returns:
            Sent message object
        """
        payload = {
            "chat_id": chat_id,
            **kwargs
        }
        
        if caption:
            payload["caption"] = caption
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)

        if isinstance(photo, str) and photo.startswith("http"):
            payload["photo"] = photo
            async with self._session.post(f"{self._base_url}/sendPhoto", json=payload) as resp:
                data = await resp.json()
        else:
            files = {"photo": open(photo, "rb") if isinstance(photo, (str, Path)) else photo}
            async with self._session.post(f"{self._base_url}/sendPhoto", data=payload, files=files) as resp:
                data = await resp.json()
                
        if not data.get("ok"):
            raise GenioNetworkError(f"Failed to send photo: {data.get('description')}")
        return Message.from_dict(data["result"])

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: bool = False,
        **kwargs
    ) -> bool:
        """
        Answer a callback query from an inline keyboard button.
        
        Args:
            callback_query_id: Query ID
            text: Text to show to user
            show_alert: Show as alert instead of notification
            **kwargs: Additional parameters
            
        Returns:
            True on success
        """
        payload = {
            "callback_query_id": callback_query_id,
            **kwargs
        }
        
        if text:
            payload["text"] = text
        if show_alert:
            payload["show_alert"] = show_alert
            
        async with self._session.post(f"{self._base_url}/answerCallbackQuery", json=payload) as resp:
            data = await resp.json()
            if not data.get("ok"):
                raise GenioNetworkError(f"Failed to answer callback query: {data.get('description')}")
            return True

    async def fetch_updates(
        self,
        offset: Optional[int] = None,
        limit: int = 100,
        timeout: int = 30,
        allowed_updates: Optional[List[str]] = None
    ) -> List[Update]:
        """
        Fetch new updates from Telegram.
        
        Args:
            offset: Update ID to start from
            limit: Maximum number of updates to fetch
            timeout: Long polling timeout
            allowed_updates: List of allowed update types
            
        Returns:
            List of updates
        """
        params = {
            "timeout": timeout,
            "limit": limit
        }
        
        if offset:
            params["offset"] = offset
        if allowed_updates:
            params["allowed_updates"] = json.dumps(allowed_updates)
            
        try:
            async with self._session.get(f"{self._base_url}/getUpdates", params=params) as resp:
                data = await resp.json()
                if not data.get("ok"):
                    raise GenioNetworkError(f"Failed to fetch updates: {data.get('description')}")
                return [Update.from_dict(update) for update in data["result"]]
        except Exception as e:
            raise GenioNetworkError(f"Network error while fetching updates: {str(e)}")

    def on_event(self, event_type: str) -> Callable:
        """
        Decorator for registering event handlers.
        
        Args:
            event_type: Type of event to handle
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            if event_type not in self._event_handlers:
                self._event_handlers[event_type] = []
            self._event_handlers[event_type].append(func)
            return func
        return decorator

    async def _handle_update(self, update: Update) -> None:
        """
        Handle a single update.
        """
        if update.message:
            handlers = self._event_handlers.get("message", [])
            for handler in handlers:
                try:
                    await handler(update.message)
                except Exception as e:
                    logger.error(f"Error in message handler: {str(e)}")
                    
        if update.callback_query:
            handlers = self._event_handlers.get("callback_query", [])
            for handler in handlers:
                try:
                    await handler(update.callback_query)
                except Exception as e:
                    logger.error(f"Error in callback query handler: {str(e)}")
                    
        if update.edited_message:
            handlers = self._event_handlers.get("edited_message", [])
            for handler in handlers:
                try:
                    await handler(update.edited_message)
                except Exception as e:
                    logger.error(f"Error in edited message handler: {str(e)}")

    async def start_bot(self, poll_interval: float = 0.1) -> None:
        """
        Start the bot and begin processing updates.
        
        Args:
            poll_interval: Interval between update checks in seconds
        """
        self._is_running = True
        last_update_id = None
        
        try:
            while self._is_running:
                try:
                    updates = await self.fetch_updates(offset=last_update_id)
                    
                    for update in updates:
                        if update.update_id:
                            last_update_id = update.update_id + 1
                        await self._handle_update(update)
                    
                    await asyncio.sleep(poll_interval)
                except Exception as e:
                    logger.error(f"Error in update loop: {str(e)}")
                    await asyncio.sleep(5)  # Wait before retrying
        finally:
            if self._session:
                await self._session.close()

    async def stop_bot(self) -> None:
        """
        Stop the bot gracefully.
        """
        self._is_running = False
        if self._session:
            await self._session.close()

    @property
    def me(self) -> Optional[User]:
        """
        Get information about the bot user.
        """
        return self._me
