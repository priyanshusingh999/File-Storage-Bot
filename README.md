# File Storage Bot

A Telegram bot to store and manage files easily. This bot allows users to upload files, generate shareable links, and manage access through commands.

👉 [Demo Bot Link](https://t.me/FileStorageX_Bot?start=_tgr_cu4Iz5llOWE1)

## Features

- Store files in a Telegram channel
- Generate shareable links for stored files
- User access control with ban/unban functionality
- Broadcast messages to users (owner only)
- Join channel verification before usage

## Installation

1. Clone the repository or download the project files.

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Set the following environment variables or configure them in the database as per your setup:

- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API Hash
- `BOT_TOKEN` - Your Telegram Bot Token
- `OWNER_ID` - Telegram user ID of the bot owner
- `BOT_USERNAME` - Your bot's username
- `STORAGE_CHANNEL_ID` - Telegram channel ID where files will be stored

## Usage

Run the bot with:

```bash
python main.py
```

The bot will start and listen for commands and file uploads.

## Commands

- `/start` - Welcome message
- `/help` - Show help message
- `/about` - About the bot
- `/broadcast` - Broadcast message to all users (owner only)
- `/genlink` - Generate multi-media shareable link
- `/users` - Show total users (owner only)
- `/ban` - Ban a user (owner only)
- `/unban` - Unban a user (owner only)
- `/db_channel` - Set storage channel ID

## Developer

Created by @codebaseera
