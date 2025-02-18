import logging
from datetime import time
from zoneinfo import ZoneInfo

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    CallbackContext
)

# ----------------------------
# 1) Logging & Config
# ----------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "7661495024:AAGcEQ_x1ljQCKozSrrE6IktyBY4TcnDxAc"
GROUP_CHAT_ID = -4604999645  # Make sure this is correct

YES_GIF = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDJwYjRjeG81cjRud2xnNGNnbGN4Ym1rOXRldW1lM2NxcGU5dTdwdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0Iy2vqY7cTFR3RGE/giphy.gif"
NO_GIF = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjE5M2JwZmU0emMzenQxNTB1bWw1Z2I0dGxxeGRocHdxeGkyN3cxeCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohc1gk8L7YJ62wOiY/giphy.gif"

# ----------------------------
# 2) Core Functions (No 'update' needed)
# ----------------------------
async def do_morning(bot):
    """
    Sends the morning reminder to GROUP_CHAT_ID
    """
    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Good morning! Time to do 50 pushups, 50 squats, and 1 km run."
    )
    await bot.send_animation(
        chat_id=GROUP_CHAT_ID,
        animation="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWkwZjM2OWtpY3ZmdWM4MzQ4eXN4bWs4cWt0bHNqcmY3YmNtZDdzdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohc0YUJvdtHXX9QRi/giphy.gif",
        caption=(
            "Pain is more than a teacher, it's a lover—it holds you close, becomes familiar, "
            "and whispers that it's all you deserve. Embrace it long enough and you'll "
            "forget life without it."
        )
    )
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="WORKOUT_YES"),
            InlineKeyboardButton("No", callback_data="WORKOUT_NO"),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Have you done your workout? Click Yes or No:",
        reply_markup=markup
    )

async def do_night(bot):
    """
    Sends the night reminder to GROUP_CHAT_ID
    """
    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Good evening! Time to do 50 pushups, 50 squats, and 1 km run."
    )
    await bot.send_animation(
        chat_id=GROUP_CHAT_ID,
        animation="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWkwZjM2OWtpY3ZmdWM4MzQ4eXN4bWs4cWt0bHNqcmY3YmNtZDdzdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohc0YUJvdtHXX9QRi/giphy.gif",
        caption="Pain is a teacher—it shows us our limits and pushes us to grow."
    )
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="WORKOUT_YES"),
            InlineKeyboardButton("No", callback_data="WORKOUT_NO"),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Have you done your workout tonight?",
        reply_markup=markup
    )

# ----------------------------
# 3) Commands (If you want manual triggers)
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Says hello on /start"""
    await update.message.reply_text("Hello! I’m Saitama bot.")

async def morning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual /morning command"""
    await do_morning(context.bot)

async def night_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual /night command"""
    await do_night(context.bot)

# ----------------------------
# 4) Scheduled Job Callbacks
# ----------------------------
async def morning_job(context: CallbackContext):
    """Runs every day at 7:00 AM IST"""
    await do_morning(context.bot)

async def night_job(context: CallbackContext):
    """Runs every day at 9:00 PM IST"""
    await do_night(context.bot)

# ----------------------------
# 5) Button Handler
# ----------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responds to inline button clicks for Yes/No"""
    query = update.callback_query
    user = query.from_user
    await query.answer()  # Acknowledge click

    if query.data == "WORKOUT_YES":
        caption = (
            f"{user.first_name} completed their workout! "
            "Live without searching for meaning and taste the freedom of the unknown."
        )
        await context.bot.send_animation(
            chat_id=GROUP_CHAT_ID,
            animation=YES_GIF,
            caption=caption
        )

    elif query.data == "WORKOUT_NO":
        caption = (
            f"{user.first_name} hasn't done the workout yet. "
            "The pain of regret is greater than the pain of discipline. Get moving!"
        )
        await context.bot.send_animation(
            chat_id=GROUP_CHAT_ID,
            animation=NO_GIF,
            caption=caption
        )

# ----------------------------
# 6) Main / Entry Point
# ----------------------------
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("morning", morning_command))
    application.add_handler(CommandHandler("night", night_command))

    # Button clicks
    application.add_handler(CallbackQueryHandler(button_handler))

    # Schedule daily tasks via JobQueue (IST time)
    # Ensure that tzdata is installed so ZoneInfo works
    ist = ZoneInfo("Asia/Kolkata")

    # For 7:00 AM & 9:00 PM
    application.job_queue.run_daily(
        morning_job,
        time(hour=7, minute=0, tzinfo=ist),
        name="morning_reminder"
    )
    application.job_queue.run_daily(
        night_job,
        time(hour=21, minute=0, tzinfo=ist),
        name="night_reminder"
    )

    # Start bot
    application.run_polling()

if __name__ == "__main__":
    main()
