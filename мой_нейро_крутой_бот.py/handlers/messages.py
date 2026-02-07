import os
from groq import Groq
from aiogram import Router, types
from config import GROQ_KEY 

router = Router()
client = Groq(api_key=GROQ_KEY)

@router.message()
async def echo_ai(message: types.Message):
    if not message.text:
        return

    bot_info = await message.bot.get_me()
    bot_username = f"@{bot_info.username}"

    # Проверки: личка, упоминание или ответ на сообщение бота
    is_private = message.chat.type == "private"
    is_mention = bot_username in message.text
    is_reply_to_me = message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id

    if is_private or is_mention or is_reply_to_me:
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        try:
            # Очищаю текст от ника бота
            prompt = message.text.replace(bot_username, "").strip()
            
            # Запрос к нейросети (использую пон Llama 3)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", # Мощная и бесплатная модель (100 проц не уверен но ок)
            )
            
            await message.reply(chat_completion.choices[0].message.content)
        except Exception as e:
            await message.answer(f"Ошибка ахеренная зовите майсера: {e}")
