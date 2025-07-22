# File Storage Bot

This is a Telegram bot built with Pyrogram that allows users to store and manage files via Telegram. It also includes a simple Flask web service to confirm the bot is running.

## Features

- Store files by forwarding them to a storage channel.
- Generate shareable links for stored files.
- User management with ban/unban functionality.
- Broadcast messages to all users (owner only).
- Simple web endpoint to check bot status.

## Requirements

- Python 3.7+
- MongoDB instance for storing user data and configuration.
- Telegram API credentials (API_ID, API_HASH, BOT_TOKEN).
- Flask and Pyrogram libraries.

## Setup

1. Clone the repository.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables or configure MongoDB `variables` collection with:

- `API_ID`
- `API_HASH`
- `BOT_TOKEN`
- `OWNER_ID`
- `BOT_USERNAME`
- `STORAGE_CHANNEL_ID`
- `MONGODB_URI`

4. Run the bot:

```bash
python main.py
```

The bot will start and the Flask web service will be available at `http://0.0.0.0:8090/`.

## Deployment

To deploy this bot as a web service:

- Ensure all environment variables are set in your deployment environment.
- Use the provided `start.sh` script or run `python main.py` to start the bot.
- The Flask app runs on port 8090 and can be used for health checks or status.

Optionally, you can create a Dockerfile or deployment configuration for your platform.

## Notes

- The bot requires a MongoDB instance accessible via `MONGODB_URI`.
- The bot uses threading to run the Flask app and Pyrogram client concurrently.
- Make sure the storage channel ID is set correctly for file forwarding.

## License

MIT License
