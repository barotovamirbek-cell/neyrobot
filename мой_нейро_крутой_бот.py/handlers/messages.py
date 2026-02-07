@router.message()
async def echo_ai(message: types.Message):
    if not message.text:
        return

    # Проверка: сообщение в личке ИЛИ бота упомянули ИЛИ ответили на его сообщение
    is_private = message.chat.type == "private"
    is_mention = message.text.startswith(f"@{ (await message.bot.get_me()).username }")
    is_reply_to_me = message.reply_to_message and message.reply_to_message.from_user.id == (await message.bot.get_me()).id

    if is_private or is_mention or is_reply_to_me:
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        try:
            # Очищаем текст от упоминания бота, чтобы нейросеть не путалась
            prompt = message.text.replace(f"@{ (await message.bot.get_me()).username }", "").strip()
            
            response = model.generate_content(prompt)
            await message.reply(response.text)
        except Exception as e:
            await message.answer(f"Ошибка: {e}")
