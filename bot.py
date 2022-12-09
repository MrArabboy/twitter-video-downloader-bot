import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from twigram import download

try:
    from local_config import API_TOKEN
except:
    API_TOKEN = os.getenv("BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("<b>Send tweet video url</b>", parse_mode="HTML")


@dp.message_handler(lambda message: not message.text.startswith("https://twitter.com"))
async def wrong_video_url(message: types.Message):
    await message.reply("❌The url is not a tweet url")


@dp.message_handler(lambda message: message.text.startswith("https://twitter.com"))
async def get_video_url(message: types.Message):
    video = download(message.text)
    if video.get("status_code", 400) == 200:
        data = video["data"]
        try:
            await bot.send_video(
                chat_id=message.chat.id,
                video=data["urls"][0]["url"],
                caption=data["tweet_text"] + f"\n\nTweet Url : {data['tweet_url']}",
                parse_mode="HTML",
            )
        except:
            await message.reply(
                (
                    "You can download this video from following url 👇\n"
                    f"{data['urls'][0]['url']}"
                )
            )
    else:
        await message.reply("❌" + video.get("message", "Something went wrong!"))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
