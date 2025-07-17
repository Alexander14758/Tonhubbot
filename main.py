#from dotenv import load_dotenv
#load_dotenv()

#import os
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token: str, mini_app_url: Optional[str] = None, channel_url: Optional[str] = None):
        """Initialize the Telegram bot with the provided token, mini app URL, and channel URL."""
        self.token = token
        self.mini_app_url = mini_app_url
        self.channel_url = channel_url
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up command handlers for the bot."""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        try:
            user_name = update.effective_user.first_name
            welcome_message = f"Hello {user_name} 👋\n\nWelcome to Tonhub"
            
            keyboard = []

            # Add channel button if URL is provided
            if self.channel_url:
                keyboard.append([
                    InlineKeyboardButton("Subscribe to Tonhub Channel", url=self.channel_url)
                ])

            # Add mini app button if URL is provided
            if self.mini_app_url:
                welcome_message += "\n\nStay connected, explore powerful features, and unlock new possibilities all in one place ☯:"
                keyboard.append([
                    InlineKeyboardButton("🚀 Open Mini App", web_app=WebAppInfo(url=self.mini_app_url))
                ])
            else:
                welcome_message += "\n\nAvailable commands:\n/start - Show this welcome message"
            
            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
            
            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
            logger.info(f"Start command processed for user: {user_name}")
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text("Sorry, something went wrong. Please try again.")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors that occur during bot operation."""
        logger.error(f"Update {update} caused error: {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text("Sorry, an error occurred. Please try again.")
    
    def run(self):
        """Start the bot with long polling."""
        logger.info("Starting Telegram Bot...")
        self.application.run_polling()

def main():
    """Main function to start the bot."""
    bot_token = "8169042800:AAFA5lD2EnP_tOkot3CNEXsahgNFXGwS_sc"
    mini_app_url = "https://harmonious-zabaione-589654.netlify.app"
    channel_url = "https://t.me/tonhub"

    bot = TelegramBot(bot_token, mini_app_url, channel_url)
    bot.run()

if __name__ == "__main__":
    main()
