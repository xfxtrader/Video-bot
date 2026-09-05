import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    await update.message.reply_text("⏳ جاري تحميل أعلى جودة...")

    try:
        options = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "video.%(ext)s",
            "merge_output_format": "mp4",
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if not filename.endswith(".mp4"):
            filename = os.path.splitext(filename)[0] + ".mp4"

        await update.message.reply_video(
            video=open(filename, "rb"),
            supports_streaming=True
        )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text("❌ ما قدرت أحمل الفيديو.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
