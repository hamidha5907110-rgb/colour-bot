import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os

# Fetch the token securely from Railway's environment variables
BOT_TOKEN = os.getenv("")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_animated_menu(message):
    msg = bot.send_message(message.chat.id, "Initialization started... ⏳")

    # Animation frames (progress bar effect)
    animation_frames = [
        "Loading modules... \n[🟩⬜️⬜️⬜️⬜️] 20%",
        "Connecting to server... \n[🟩🟩⬜️⬜️⬜️] 40%",
        "Applying colorful theme... \n[🟩🟩🟩⬜️⬜️] 60%",
        "Generating buttons... \n[🟩🟩🟩🟩⬜️] 80%",
        "Almost ready... \n[🟩🟩🟩🟩🟩] 99%"
    ]

    for frame in animation_frames:
        time.sleep(0.6) 
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=frame)

    # Create the colorful inline keyboard using the style parameter
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    # Define natively colored buttons 
    btn_red = InlineKeyboardButton("Red Alert", callback_data="red", style="danger")
    btn_green = InlineKeyboardButton("Go Green", callback_data="green", style="success")
    btn_blue = InlineKeyboardButton("Blue Sky", callback_data="blue", style="primary")
    btn_default = InlineKeyboardButton("Default Button", callback_data="neutral") 

    markup.add(btn_red, btn_green)
    markup.add(btn_blue, btn_default)

    final_text = "✨ **Welcome to the Colorful Hub!** ✨\n\nChoose an option below to see the native colored buttons:"
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=msg.message_id,
        text=final_text,
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    responses = {
        "red": "🚨 Danger action triggered!",
        "green": "🌿 Success action activated.",
        "blue": "🌊 Primary action selected.",
        "neutral": "Standard button pressed."
    }

    if call.data in responses:
        bot.answer_callback_query(call.id, text=responses[call.data], show_alert=True)

print("Bot is running and listening for messages...")
bot.infinity_polling()
