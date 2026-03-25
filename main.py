import telebot
import openai
import requests
import os

# Lấy từ Variables Railway
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TOKEN"))

memory = {}

def search_web(query):
    return f"Kết quả tìm kiếm cho: {query}"

@bot.message_handler(func=lambda m: True)
def chat(message):
    user_id = message.chat.id
    
    if user_id not in memory:
        memory[user_id] = []

    text = message.text

    # TOOL: tìm web
    if text.startswith("/search"):
        result = search_web(text.replace("/search ", ""))
        bot.reply_to(message, result)
        return

    memory[user_id].append({"role": "user", "content": text})

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=memory[user_id]
    )

    reply = response.choices[0].message.content
    memory[user_id].append({"role": "assistant", "content": reply})

    bot.reply_to(message, reply)

bot.polling()
