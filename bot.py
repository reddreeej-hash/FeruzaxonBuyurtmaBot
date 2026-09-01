from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters
)

TOKEN = "8987995533:AAEU33YgqvQaMdeHtYv2h8oxjMTKSnrO9bE"
ADMIN_ID = 7696134951

ISM, TELEFON, SANA, SOAT, BUYURTMA, TORT = range(6)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "🍰 Feruzaxon Buyurtma Bot\n\n"
        "Assalomu alaykum!\n"
        "Buyurtma berish uchun ma'lumotlarni kiriting.\n\n"
        "👤 Ismingiz?"
    )
    return ISM


async def ism(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism"] = update.message.text
    await update.message.reply_text("📞 Telefon raqamingiz?")
    return TELEFON


async def telefon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telefon"] = update.message.text

    await update.message.reply_text(
        "📅 Buyurtma qaysi kunga kerak?\n\n"
        "📝 Misol: 17-sentabr\n\n"
        "Iltimos, kun va oyini yozing 😊"
    )

    return SANA


async def sana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sana"] = update.message.text

    await update.message.reply_text(
        "⏰ Soat nechida kerak?\n\n"
        "Misol: 15:30"
    )

    return SOAT


async def soat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["soat"] = update.message.text

    await update.message.reply_text(
        "🍰 Qanday buyurtma qilmoqchisiz?\n\n"
        "Masalan: shokoladli tort, to‘y torti yoki boshqa tur 😊"
    )

    return BUYURTMA


async def buyurtma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"] = update.message.text

    await update.message.reply_text(
        "🎂 Tort qanday bo‘lishini xohlaysiz?\n\n"
        "Masalan: rangi, dizayni yoki ustidagi yozuvi 😊"
    )

    return TORT


async def tort(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tort"] = update.message.text

    xabar = (
        "🎂 Buyurtmangiz:\n\n"
        f"👤 Ism: {context.user_data['ism']}\n"
        f"📞 Telefon: {context.user_data['telefon']}\n"
        f"📅 Sana: {context.user_data['sana']}\n"
        f"🍰 Buyurtma: {context.user_data['buyurtma']}\n"
        f"🎀 Tort: {context.user_data['tort']}\n\n"
        "Tasdiqlaysizmi?"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Tasdiqlash", callback_data="tasdiq"),
            InlineKeyboardButton("❌ Bekor qilish", callback_data="bekor")
        ]
    ]

    await update.message.reply_text(
        xabar,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return ConversationHandler.END


app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        ISM: [MessageHandler(filters.TEXT, ism)],
        TELEFON: [MessageHandler(filters.TEXT, telefon)],
        SANA: [MessageHandler(filters.TEXT, sana)],
        SOAT: [MessageHandler(filters.TEXT, soat)],
        BUYURTMA: [MessageHandler(filters.TEXT, buyurtma)],
        TORT: [MessageHandler(filters.TEXT, tort)],
    },
    fallbacks=[],
    allow_reentry=True
)

async def tasdiqlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    xabar = (
    "🎂 Yangi buyurtma!\n\n"
    f"👤 Ism: {context.user_data['ism']}\n"
    f"📞 Telefon: {context.user_data['telefon']}\n"
    f"📅 Sana: {context.user_data['sana']}\n"
    f"⏰ Soat: {context.user_data['soat']}\n"
    f"🍰 Buyurtma: {context.user_data['buyurtma']}\n"
    f"🎀 Tort: {context.user_data['tort']}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=xabar
    )

    await query.message.reply_text(
        "✅ Buyurtmangiz qabul qilindi!\n\n"
        "📞 Tez orada siz bilan bog‘lanamiz 😊"
    )


async def bekor_qilish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "❌ Buyurtma bekor qilindi.\n\n"
        "Qaytadan boshlash uchun /start bosing."
    )


app.add_handler(conv)
app.add_handler(CallbackQueryHandler(tasdiqlash, pattern="tasdiq"))
app.add_handler(CallbackQueryHandler(bekor_qilish, pattern="bekor"))

print("Feruzaxon Buyurtma Bot ishga tushdi")

from flask import Flask
import threading
import time

web = Flask(__name__)


@web.route("/")
def home():
    return "Bot ishlayapti"


@web.route("/health")
def health():
    return "OK"


def run_web():
    web.run(host="0.0.0.0", port=10000)


threading.Thread(target=run_web, daemon=True).start()


while True:
    try:
        app.run_polling(
            drop_pending_updates=True
        )
    except Exception as e:
        print("Bot xatosi:", e)
        time.sleep(5)
