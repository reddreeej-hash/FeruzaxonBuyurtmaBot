from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

TOKEN = "8987995533:AAEU33YgqvQaMdeHtYv2h8oxjMTKSnrO9bE"
ADMIN_ID = 7696134951

ISM, TELEFON, SANA, BUYURTMA, TORT = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "🎂 Yangi buyurtma!\n\n"
        f"👤 Ism: {context.user_data['ism']}\n"
        f"📞 Telefon: {context.user_data['telefon']}\n"
        f"📅 Sana: {context.user_data['sana']}\n"
        f"🍰 Buyurtma: {context.user_data['buyurtma']}\n"
        f"🎀 Tort qanday bo‘lsin: {context.user_data['tort']}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=xabar
    )

    await update.message.reply_text(
        "✅ Rahmat! Buyurtmangiz qabul qilindi."
    )

    return ConversationHandler.END


app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        ISM: [MessageHandler(filters.TEXT, ism)],
        TELEFON: [MessageHandler(filters.TEXT, telefon)],
        SANA: [MessageHandler(filters.TEXT, sana)],
        BUYURTMA: [MessageHandler(filters.TEXT, buyurtma)],
        TORT: [MessageHandler(filters.TEXT, tort)],
    },
    fallbacks=[]
)

app.add_handler(conv)

print("Feruzaxon Buyurtma Bot ishga tushdi")
from flask import Flask
import threading

web = Flask(__name__)

@web.route("/")
def home():
    return "Bot ishlayapti"

def run_web():
    web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()
app.run_polling()
