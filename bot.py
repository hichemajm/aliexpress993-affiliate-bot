import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from aliexpress_api import AliExpressAPI
from utils import extract_aliexpress_url, format_product_message

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize AliExpress API
ali_api = AliExpressAPI()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when command /start is issued."""
    welcome_text = """
🤖 *Welcome to AliExpress Discount Bot!*

Simply send me any AliExpress product link and I'll convert it to a discounted affiliate link with special offers!

💡 *How to use:*
1. Copy any AliExpress product URL
2. Send it to this chat
3. Get your discounted link!

💰 *Benefits:*
• Special discounts available
• Same product, better price
• Secure shopping experience

Start by sending me an AliExpress product link! 🛍️
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
📖 *Bot Help Guide*

*Available Commands:*
/start - Start the bot and see welcome message
/help - Show this help message

*How to Get Discounts:*
1. Go to AliExpress and find a product you like
2. Copy the product URL
3. Paste it here and send
4. I'll instantly provide a discounted affiliate link

*Note:* The discount varies by product and is provided through the affiliate program.

Need assistance? Contact the bot administrator.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and process AliExpress links."""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    logger.info(f"Received message from user {user_id}: {message_text}")
    
    # Extract AliExpress URL
    ali_url = extract_aliexpress_url(message_text)
    
    if not ali_url:
        await update.message.reply_text(
            "❌ I couldn't find a valid AliExpress product link in your message.\n\n"
            "Please send a valid AliExpress product URL starting with:\n"
            "• https://www.aliexpress.com/item/...\n"
            "• https://es.aliexpress.com/item/...\n"
            "• Or other AliExpress domains"
        )
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Processing your link...")
    
    try:
        # Get product information
        product_info = ali_api.get_product_info(ali_url)
        
        if not product_info:
            await processing_msg.edit_text(
                "❌ Sorry, I couldn't retrieve information for this product.\n"
                "Please make sure the link is valid and try again."
            )
            return
        
        # Generate affiliate link
        affiliate_link = ali_api.generate_affiliate_link(ali_url, product_info.get('product_id'))
        
        # Format response message
        message, image_url = format_product_message(product_info, affiliate_link)
        
        # Send product information with image
        if image_url:
            await update.message.reply_photo(
                photo=image_url,
                caption=message,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                message,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
        
        # Delete processing message
        await processing_msg.delete()
        
        logger.info(f"Successfully processed link for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await processing_msg.edit_text(
            "❌ An error occurred while processing your request.\n"
            "Please try again in a few moments."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors and handle exceptions."""
    logger.error(f"Exception while handling an update: {context.error}")

def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the Bot
    print("🤖 Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()