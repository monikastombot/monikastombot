from vkbottle.bot import Bot, Message

bot = Bot("vk1.a.0pDVa8Iu0ef6Kz9uphtu2Cs-Ia_5m9iyBvE4aWkPYkhtcivdgzJi4D3Qkw6HRZfg7Jh9pN5He34AbxlK6gfmPNjbnIH-yKeo1veUraMccrh4Veg9g5blECLffWyzfyJ0_YkGsTlTnU0IOf6WTElSkLaTO93C6yNDyTyWjUCy-CODMAwaTo1SgT1JkSF_PuyugWixfF30OqyJ5HD4EiGtyQ")  # Вставьте сюда токен сообщества

@bot.on.message(text=["привет", "старт", "начать"])
async def start_handler(message: Message):
    await message.answer("Здравствуйте! Вас приветствует бот клинического исследования. Для участия подтвердите согласие. Напишите: Согласен")

@bot.on.message(text="согласен")
async def consent_handler(message: Message):
    await message.answer("Спасибо за согласие! Выберите вашу роль: Пациент или Врач.")

@bot.on.message(text="пациент")
async def patient_handler(message: Message):
    await message.answer("Вы выбрали режим Пациента. Готовы пройти анкету? (напишите: анкета)")

@bot.on.message(text="анкета")
async def questionnaire_handler(message: Message):
    await message.answer("Вопрос 1: Опишите ваши жалобы.")
    # тут можно начинать логику для опросов, графики, шкалы, SOS и т.д.

@bot.on.message(text="врач")
async def doctor_handler(message: Message):
    await message.answer("Выбрана роль Врач. Введите уникальный код пациента для загрузки данных.")

bot.run_forever()
