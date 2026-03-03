# Telegram Streamer Bot

A Telegram bot that streams AI responses using OpenAI's API. This bot listens for private messages and streams the AI's response back to the user in real-time.

## Features

- **Real-time Streaming**: Streams OpenAI responses directly to Telegram.
- **Private Chat Support**: Works in private chats with the bot.
- **Customizable Model**: Supports configuring the OpenAI model (default: `gpt-4o-mini`).

## Prerequisites

- Python 3.8+
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- An OpenAI API Key

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd stsense
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the following environment variables before running the bot. You can set them in your terminal or use a `.env` file (if you add `python-dotenv` support).

- `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token.
- `OPENAI_API_KEY`: Your OpenAI API Key.
- `OPENAI_MODEL`: (Optional) The OpenAI model to use (default: `gpt-4o-mini`).

## Usage

1. Run the bot:

   ```bash
   export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
   export OPENAI_API_KEY="your_openai_api_key"
   python app.py
   ```

2. Open your bot in Telegram and send a message. The bot will stream the response back to you.

---

## Recommended Tool

**<Img src="https://devskarma.com/og-image.png" alt="DevsKarma Logo"/>**
**[DevsKarma](https://devskarma.com)** - A realtime collaboration platform for developers. Check it out to enhance your developer energy!
