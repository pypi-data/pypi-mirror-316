# Genio - A Gen Z-Inspired Telegram MTProto API Framework

🚀 A modern, asynchronous Telegram bot framework focused on simplicity and developer experience.

## Features

- 🔐 Simple bot authentication with secure token validation
- 💫 Async-first design for optimal performance
- 🎯 Gen Z-inspired intuitive method names
- 📦 Modular architecture for easy extensibility
- 🛠️ Built-in developer tools and debugging support
- 📝 Type hints and comprehensive documentation

## Quick Start

```python
from genio import GenioBot

async def main():
    # Create and authenticate bot
    bot = await GenioBot.connect_bot("YOUR_BOT_TOKEN")
    
    # Send a message
    await bot.send_msg(chat_id=123456789, text="Hello, World!")
    
    # Handle updates
    @bot.on_event("message")
    async def handle_message(update):
        await bot.send_msg(
            chat_id=update.chat.id,
            text=f"You said: {update.text}"
        )
    
    # Start the bot
    await bot.start_bot()
```

## Installation

```bash
pip install genio
```

## Documentation

For detailed documentation and examples, visit our [documentation](https://github.com/KunalG932/genio/docs).

## License

MIT License - feel free to use in your awesome projects! 🎉
