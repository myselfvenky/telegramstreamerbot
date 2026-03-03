import os
import asyncio
import time

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ChatType
from aiogram.types import Message
from openai import AsyncOpenAI


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL") or "gpt-4o-mini"


def _make_draft_id() -> int:
    return int(time.time() * 1000) % 2_147_483_647 or 1


def _clip(text: str, max_len: int = 4096) -> str:
    if len(text) <= max_len:
        return text
    return "… " + text[-(max_len - 2) :]


async def _openai_stream_text(prompt: str):
    if not OPENAI_API_KEY:
        yield "OPENAI_API_KEY is missing."
        return

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    try:
        stream = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content
    except Exception as e:
        yield f"OpenAI error: {e}"


async def stream_ai_response(bot: Bot, chat_id: int, prompt: str) -> None:
    draft_id = _make_draft_id()
    text = ""
    last_send = 0.0
    min_interval_sec = 0.8

    await bot.send_message_draft(chat_id=chat_id, draft_id=draft_id, text="Thinking…")

    async for chunk in _openai_stream_text(prompt):
        text += chunk
        now = time.time()
        if now - last_send >= min_interval_sec:
            await bot.send_message_draft(
                chat_id=chat_id,
                draft_id=draft_id,
                text=_clip(text),
            )
            last_send = now

    await bot.send_message(chat_id=chat_id, text=_clip(text) or "Done.")


async def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing.")

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    router = Router()

    @router.message()
    async def handle_message(message: Message) -> None:
        if message.chat.type != ChatType.PRIVATE:
            await message.answer("DM me to stream responses.")
            return

        prompt = (message.text or "").strip()
        if not prompt:
            await message.answer("Send a prompt to start streaming.")
            return

        await stream_ai_response(bot=bot, chat_id=message.chat.id, prompt=prompt)

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
