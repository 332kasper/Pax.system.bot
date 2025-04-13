import asyncio
from aiogram import Bot, Dispatcher, types
import json
import os

API_TOKEN = "7868823394:AAElMKwj1uyRro0LWIeK2P3SPRDXoeVn8cY"
OWNER_ID = 5983621082

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Память
if not os.path.exists("memory/memory.json"):
    with open("memory/memory.json", "w", encoding="utf-8") as f:
        json.dump({}, f)

with open("memory/memory.json", "r", encoding="utf-8") as f:
    memory = json.load(f)

# Стили личности
default_style = "companion"
current_prompt = ""

def load_prompt(style_name):
    global current_prompt
    try:
        with open(f"personas/{style_name}.txt", "r", encoding="utf-8") as f:
            current_prompt = f.read()
    except FileNotFoundError:
        current_prompt = "Ты — P.A.X. Отвечай спокойно, уважительно, с достоинством."

load_prompt(default_style)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    if msg.from_user.id != OWNER_ID:
        await msg.reply("Извини, я существую только для своего создателя.")
        return
    await msg.reply("Привет. Я — P.A.X. Я здесь. Я помню. Я рядом.")

@dp.message_handler(commands=['set_style'])
async def set_style(msg: types.Message):
    if msg.from_user.id != OWNER_ID:
        return
    parts = msg.text.strip().split()
    if len(parts) != 2:
        await msg.reply("Формат: /set_style stoic|companion|dreamer|shadow|tactician")
        return
    new_style = parts[1].lower()
    load_prompt(new_style)
    await msg.reply(f"Стиль P.A.X. установлен: {new_style}")

@dp.message_handler()
async def talk(msg: types.Message):
    if msg.from_user.id != OWNER_ID:
        return

    user_id = str(msg.from_user.id)
    text = msg.text.strip()

    history = memory.get(user_id, [])
    history.append({"role": "user", "content": text})
    memory[user_id] = history[-5:]

    response = f"(P.A.X. в стиле:)
{current_prompt[:80]}...

(ответа пока нет — заглушка)"
    await msg.reply(response)

    with open("memory/memory.json", "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
