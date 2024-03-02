import os
import logging
import dotenv

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from LangchainInterface import LangchainInterface

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Runs on /start
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! This is LTA Smart Agent. One day I'll be able to answer your queries about anything transport related!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Runs on /help
    await update.message.reply_text("I can't do anything yet! Come back later?")


async def normal_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # forward message to langchain, wait for reply from langchain
    answer = lc.query_agent(update.message.text)

    # reply user
    await update.message.reply_text(answer)


lc = LangchainInterface()


def main() -> None:
    dotenv.load_dotenv()
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_API_KEY")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, normal_message)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
