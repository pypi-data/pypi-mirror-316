"""
Utility functions and helpers for the Genio framework.
"""
import json
import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

def validate_token(token: str) -> bool:
    """
    Validate bot token format.
    """
    parts = token.split(':')
    return len(parts) == 2 and all(part.isalnum() for part in parts)

def build_api_url(token: str, method: str) -> str:
    """
    Build Telegram API URL for a given method.
    """
    base = f"https://api.telegram.org/bot{token}/"
    return urljoin(base, method)

def parse_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate Telegram API response.
    """
    if not response_data.get("ok"):
        error_code = response_data.get("error_code", "unknown")
        description = response_data.get("description", "No description provided")
        logger.error(f"API Error {error_code}: {description}")
        raise ValueError(f"API Error: {description}")
    return response_data.get("result", {})
