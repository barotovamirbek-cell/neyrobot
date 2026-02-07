import google.generativeai as genai
from aiogram import Router, types
from config import GEMINI_KEY

# Инициализация пенисногороутасука
router = Router()

# Настройка нейросети
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@router.message()
async def echo_ai(message: types.Message):
    # Игнорирование сообщений без текста (картинки, стикеры и т.д.)
    if not message.text:
        return

    
    bot_info = await message.bot.get_me()
    bot_username = f"@{bot_info.username}"

    # Проверки: личкагея, упоминание или ответ на сообщение бота окак это мой нейропук да тот кто это читает хуле тут забыл говно
    is_private = message.chat.type == "private"
    is_mention = message.text.startswith(bot_username)
    is_reply_to_me = message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id

    if is_private or is_mention or is_reply_to_me:
        # Отображение статуса "печатает..." нихуя себе я об этом шас узнал
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        try:
            # Очистка текста от упоминания бота (@имя_бота), чтобы ИИ не тупил
            prompt = message.text.replace(bot_username, "").strip()
            
            # Если после удаления ника пусто — не отвечаем
            if not prompt and not is_reply_to_me:
                return

            # Запрос к нейросети
            response = model.generate_content(prompt)
            
            # Ответ пользователю
            await message.reply(response.text)
            
        except Exception as e:
            await message.answer(f"⚠️ Произошла ошибка: {e}")
