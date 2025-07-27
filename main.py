from pyrogram.client import Client
from pyrogram import filters
from functools import wraps
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, db, BOT_USERNAME, STORAGE_CHANNEL_ID
import base64


bot = Client("file_storage_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def check_user_access():
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message: Message):
            if db['banuser'].find_one({"user_id": message.from_user.id}):
                await message.reply_text("❌ You are banned from using this bot.")
                return

            try:
                chat_member = await client.get_chat_member("@codebaseera", message.from_user.id)
                if chat_member.status in ["kicked", "left"]:
                    raise UserNotParticipant
            except UserNotParticipant:
                msg = "<b>🚫 To use this bot, please join our channel first.</b>"
                keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔔 Join Channel", url="https://t.me/codebaseera")]])
                await message.reply_text(msg, reply_markup=keyboard)
                return

            return await func(client, message)
        return wrapper
    return decorator


def encode_data(channel_id, start_id, end_id):
    raw = f"{channel_id}|{start_id}|{end_id}"
    return base64.urlsafe_b64encode(raw.encode()).decode()

# Decode utility
def decode_data(encoded):
    decoded = base64.urlsafe_b64decode(encoded).decode()
    channel_id, start, end = decoded.split("|")
    return int(channel_id), int(start), int(end)


@bot.on_message(filters.command("start") & filters.private)
@check_user_access()
async def broadcast_command(client, message: Message):
    user_data = {"user_id": message.from_user.id,"username": message.from_user.username,"name": message.from_user.first_name}
    db['userinfo'].update_one({"user_id": user_data["user_id"]},{"$set": user_data},upsert=True)

    if len(message.command) > 1:
        try:
            code = message.command[1]

            decoded = base64.urlsafe_b64decode(code.encode()).decode()

            if "|" in decoded:
                # Multi-message link
                channel_id, start_id, end_id = decode_data(code)
                await message.reply_text(f"📤 Sending messages {start_id} to {end_id}...", quote=True)
                for msg_id in range(start_id, end_id + 1):
                    try:
                        await client.copy_message(
                            chat_id=message.chat.id,
                            from_chat_id=channel_id,
                            message_id=msg_id
                        )
                    except Exception as e:
                        print(f"❌ Failed to send message {msg_id}")
                return
            else:
                # Single message link
                decoded_msg_id = int(decoded)
                await client.copy_message(
                    chat_id=message.from_user.id,
                    from_chat_id=STORAGE_CHANNEL_ID,
                    message_id=decoded_msg_id
                )
                return

        except Exception as e:
            print("Decoding error:", e)
            return await message.reply_text("❌ Invalid or expired link.")

    start_text = (f"<b>Hello! {message.from_user.first_name},\n\n""Welcome to the File Storage Bot!\n\n""Use /help to see what I can do.</b>")
    start_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("❇️ JOIN CHANNEL ❇️", url="https://t.me/codebaseera")],[InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/r_ajput999"),InlineKeyboardButton("👨‍💻 GitHub", url="https://github.com/priyanshusingh999")]])
    await message.reply_text(start_text, reply_markup=start_keyboard)


@bot.on_message(filters.command("help") & filters.private)
@check_user_access()
async def broadcast_command(client, message: Message):
    await message.reply_text("<b>🛠 Available Commands:\n\n/start - Welcome message\n/help - Show this help\n/about - About me\n/broadcast - use only owner🔒\n/genlink - create multi media link\n/users - use only owner🔒\n/ban - use only owner🔒\n/unban - use only owner🔒</b>")


@bot.on_message(filters.command("about") & filters.private)
@check_user_access()
async def broadcast_command(client, message: Message):
    await message.reply_text("<b>👨‍💻 About Me:\n\nI'm a File Storage Bot\ncreated by @codebaseera.\n\n I can help you store and manage your files easily.</b>")


@bot.on_message(filters.command("users") & filters.private & filters.user(OWNER_ID))
@check_user_access()
async def broadcast_command(client, message: Message):
    user_count = db["userinfo"].count_documents({"user_id": {"$exists": True}})
    await message.reply_text(f" 👥 Total Users: {user_count}")


@bot.on_message(filters.command("broadcast") & filters.private & filters.user(OWNER_ID))
@check_user_access()
async def broadcast(client, message: Message):
    message_parts = message.text.split(maxsplit=1)
    if len(message_parts) < 2:
        await message.reply_text("❌ Please provide a message to broadcast.")
        return

    broadcast_text = message_parts[1].strip()

    user_cursor = db["userinfo"].find({"user_id": {"$exists": True}}, {"user_id": 1})
    total, success, failed = 0, 0, 0

    for user in user_cursor:
        user_id = user.get("user_id")
        total += 1
        try:
            await client.send_message(user_id, broadcast_text)
            success += 1
        except Exception as e:
            print(f"❌ Failed to send message to {user_id}: {e}")
            failed += 1

    summary = (f"✅ Broadcast completed!\n\n"f"👥 Total Users: {total}\n"f"✅ Sent: {success}\n"f"❌ Failed: {failed}")
    await message.reply_text(summary)


@bot.on_message(filters.command("ban") & filters.private & filters.user(OWNER_ID))
@check_user_access()
async def ban_user(client, message: Message):
    message_parts = message.text.split(maxsplit=1)
    if len(message_parts) < 2:
        await message.reply_text("❌ Please provide a user ID to ban.\n\nUsage: `/ban 123456789`")
        return
    try:
        user_id = int(message_parts[1].strip())
    except ValueError:
        return await message.reply_text("❌ Invalid user ID format. Please send a numeric ID.")

    user = db["userinfo"].find_one({"user_id": user_id}, {"_id": 0, "user_id": 1, "username": 1, "name": 1})
    if not user:
        return await message.reply_text("❌ User not found in userinfo collection.")

    if db["banuser"].find_one({"user_id": user_id}):
        return await message.reply_text("⚠️ This user is already banned.")

    db["banuser"].insert_one(user)
    db["userinfo"].update_one({"user_id": user_id}, {"$set": {"banned": True}})
    await message.reply_text(f"✅ User `{user_id}` banned successfully.")


@bot.on_message(filters.command("unban") & filters.private & filters.user(OWNER_ID))
@check_user_access()
async def unban_user(client, message: Message):
    message_parts = message.text.split(maxsplit=1)
    if len(message_parts) < 2:
        await message.reply_text("❌ Please provide a user ID to unban.\n\nUsage: `/unban 123456789`")
        return
    try:
        user_id = int(message_parts[1].strip())
    except ValueError:
        return await message.reply_text("❌ Invalid user ID format. Please send a numeric ID.")
    
    banned_user = db["banuser"].find_one({"user_id": user_id})
    if not banned_user:
        return await message.reply_text("ℹ️ This user is not in the banned list.")

    db["banuser"].delete_one({"user_id": user_id})
    db["userinfo"].update_one({"user_id": user_id}, {"$set": {"banned": False}})
    await message.reply_text(f"✅ User `{user_id}` unbanned successfully.")


@bot.on_message(filters.private & (filters.photo | filters.video | filters.document | filters.audio | filters.voice | filters.video_note))
@check_user_access()
async def forward_to_storage(client, message: Message):
    try:
        # 📤 Forward to storage channel
        forwarded_msg = await message.forward(chat_id=STORAGE_CHANNEL_ID)  # 👈 Replace with your channel ID
        stored_message_id = forwarded_msg.id  # Message ID in the channel

        # 🔐 Encode message_id into a shareable code
        encoded_msg_id = base64.urlsafe_b64encode(str(stored_message_id).encode()).decode()

        # 🔗 Create shareable /start link
        link = f"https://t.me/{BOT_USERNAME}?start={encoded_msg_id}"

        # ✅ Confirm & send link to user
        await message.reply_text(
            f"✅ Your file linked successfully.\n\n🔗<b>Share link:</b> {link}")

    except Exception as e:
        print("Forward Error:", e)
        await message.reply_text("❌ Failed to save your file. Please try again later.")


@bot.on_message(filters.command("db_channel") & filters.private)
@check_user_access()
async def set_storage_channel(client, message: Message):
    message_parts = message.text.split(maxsplit=1)
    if len(message_parts) < 2:
        await message.reply_text("❌ Please provide a channel ID to set as storage channel.\n")
        return
    channel_id = message_parts[1].strip()
    try:
        channel_id = int(channel_id)
    except ValueError:
        return await message.reply_text("❌ Invalid channel ID format. Please send a numeric ID.")

    db["userinfo"].update_one({"user_id": message.from_user.id}, {"$set": {"storage_channel_id": channel_id}})
    await message.reply_text(f"✅ Storage channel set to {channel_id}.")


@bot.on_message(filters.command("genlink") & filters.private)
@check_user_access()
async def generate_link(client, message: Message):
    args = message.command[1:]

    # If user provides 3 args: channel_id, start_id, end_id
    if len(args) == 3:
        try:
            channel_id = int(args[0])
            start_id = int(args[1])
            end_id = int(args[2])
        except ValueError:
            return await message.reply_text("❌ Invalid input. Use:\n/genlink <channel_id> <start_id> <end_id>")
    # If user provides 2 args: start_id, end_id (and has a saved storage_channel)
    elif len(args) == 2:
        user_data = db["userinfo"].find_one({"user_id": message.from_user.id})
        if not user_data or "storage_channel_id" not in user_data:
            return await message.reply_text("❌ No storage channel found. Use /db_channel <channel_id> to set it.")
        try:
            channel_id = user_data["storage_channel_id"]
            start_id = int(args[0])
            end_id = int(args[1])
        except ValueError:
            return await message.reply_text("❌ Invalid input. Use:\n/genlink <start_id> <end_id>")
    else:
        return await message.reply_text("❌ Usage:\n/genlink <channel_id> <start_id> <end_id>\nOR\n/genlink <start_id> <end_id> (after setting channel with /db_channel)")

    try:
        code = encode_data(channel_id, start_id, end_id)
        bot_username = (await client.get_me()).username
        link = f"https://t.me/{bot_username}?start={code}"
        await message.reply_text(
            f"✅ Share link created:\n\n🔗 {link}",
            disable_web_page_preview=True
        )
    except Exception as e:
        await message.reply_text(f"❌ Error while generating link: {e}")


if __name__ == "__main__":
    bot.run()