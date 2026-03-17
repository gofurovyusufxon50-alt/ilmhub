#!/usr/bin/env python3
# IlmHub Telegram Bot
# Token: 8714864664:AAGHYNzadoMCv6nrsy_agnf2LtEVRe21wk4

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# ============================================================
# SOZLAMALAR
# ============================================================
TOKEN = "8714864664:AAGHYNzadoMCv6nrsy_agnf2LtEVRe21wk4"
ADMIN_ID = 7945692959  # Sizning Telegram ID ingiz
ADMIN_IDS = [7945692959]

# Kurslar (saytdagi kurslar bilan mos)
COURSES = {
    "english_a1": {
        "name": "Ingliz tili A1 Beginner",
        "emoji": "🇬🇧",
        "price": 149000,
        "lessons": 10,
        "telegram_group": "",  # Guruh linki
    },
    "python": {
        "name": "Python dasturlash",
        "emoji": "🐍",
        "price": 199000,
        "lessons": 10,
        "telegram_group": "",
    },
    "figma": {
        "name": "Figma UI/UX dizayn",
        "emoji": "🎨",
        "price": 249000,
        "lessons": 10,
        "telegram_group": "",
    },
    "marketing": {
        "name": "Instagram marketing",
        "emoji": "📱",
        "price": 0,
        "lessons": 10,
        "telegram_group": "",
    },
}

# Topshiriqlar (kurs ID -> dars raqami -> topshiriq matni)
TASKS = {
    "english_a1": {
        1: "📝 1-dars topshirig'i:\nO'zingizni inglizcha tanishtiring:\n- My name is...\n- I am ... years old\n- I am from...\n\nJavobingizni shu guruhga yozing! 💪",
        2: "📝 2-dars topshirig'i:\n1 dan 20 gacha inglizcha saning va yozing!\nMisol: One, two, three...",
        3: "📝 3-dars topshirig'i:\nAtrofingizga qarang, 5 ta narsaning rangini inglizcha yozing!\nMisol: My car is red 🚗",
        4: "📝 4-dars topshirig'i:\nOilangiz haqida inglizcha yozing:\n- I have ... brothers/sisters\n- My mother's name is...",
        5: "📝 5-dars topshirig'i:\nBugungi kunni inglizcha ayting:\n- Today is... (Monday/Tuesday...)\n- It is ... o'clock",
        6: "📝 6-dars topshirig'i:\nSevimli taomingizni inglizcha ayting!\nMisol: I like pizza and coca-cola 🍕",
        7: "📝 7-dars topshirig'i:\nUyingizni tavsiflab bering inglizcha:\n- I live in a ... (house/apartment)\n- My home has ... rooms",
        8: "📝 8-dars topshirig'i:\nKasbingizni yoki orzuingizni inglizcha ayting:\nMisol: I am a student. I want to be a doctor 👨‍⚕️",
        9: "📝 9-dars topshirig'i:\nBugungi ob-havoni inglizcha tavsiflab bering:\nMisol: Today is sunny and warm ☀️",
        10: "📝 10-dars topshirig'i (YAKUNIY):\nDo'konda xarid qilish dialogini yozing:\n- Siz: Excuse me, how much is this?\n- Sotuvchi: It's ... som\n- Siz: I'll take it, please!\n\n🎉 Tabriklaymiz! A1 kursini tugatdingiz!",
    }
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# START KOMANDASI
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📚 Kurslar ro'yxati", callback_data="courses")],
        [InlineKeyboardButton("💳 To'lov qilish", callback_data="payment")],
        [InlineKeyboardButton("📞 Yordam", callback_data="help")],
        [InlineKeyboardButton("👤 Mening kurslarim", callback_data="my_courses")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}! 👋\n\n"
        f"🎓 *IlmHub* — Online Ta'lim Platformasiga xush kelibsiz!\n\n"
        f"📱 Saytimiz: ilmhub.uz\n\n"
        f"Quyidagi bo'limlardan birini tanlang:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# ============================================================
# KURSLAR RO'YXATI
# ============================================================
async def show_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📚 *Bizning kurslar:*\n\n"
    keyboard = []
    
    for course_id, course in COURSES.items():
        price_text = "Bepul" if course['price'] == 0 else f"{course['price']:,} so'm"
        text += f"{course['emoji']} *{course['name']}*\n"
        text += f"💰 Narx: {price_text}\n"
        text += f"📖 Darslar: {course['lessons']} ta\n\n"
        keyboard.append([InlineKeyboardButton(
            f"{course['emoji']} {course['name']} — {price_text}",
            callback_data=f"course_{course_id}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

# ============================================================
# KURS DETAIL
# ============================================================
async def show_course_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    course_id = query.data.replace("course_", "")
    course = COURSES.get(course_id)
    if not course:
        return
    
    price_text = "🆓 BEPUL" if course['price'] == 0 else f"💰 {course['price']:,} so'm"
    
    keyboard = [
        [InlineKeyboardButton("💳 Sotib olish", callback_data=f"buy_{course_id}")],
        [InlineKeyboardButton("🔙 Kurslar", callback_data="courses")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{course['emoji']} *{course['name']}*\n\n"
        f"📖 Darslar soni: {course['lessons']} ta\n"
        f"💵 Narx: {price_text}\n\n"
        f"✅ Kurs ichida:\n"
        f"• Video darslar\n"
        f"• Testlar va topshiriqlar\n"
        f"• Telegram guruhiga kirish\n"
        f"• Sertifikat\n\n"
        f"Sotib olish uchun tugmani bosing:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# ============================================================
# SOTIB OLISH
# ============================================================
async def buy_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    course_id = query.data.replace("buy_", "")
    course = COURSES.get(course_id)
    if not course:
        return
    
    user = query.from_user
    
    if course['price'] == 0:
        # Bepul kurs
        await query.edit_message_text(
            f"🎉 *{course['name']}* kursiga muvaffaqiyatli yozildingiz!\n\n"
            f"📱 Saytda boshlang: https://gofurovyusufxon50-alt.github.io/ilmhub/ilmhub.html\n\n"
            f"Savollar bo'lsa /help yozing!",
            parse_mode='Markdown'
        )
        # Adminga xabar
        await notify_admin(context, f"🆓 Yangi o'quvchi!\n👤 {user.first_name} (@{user.username})\n📚 {course['name']}")
    else:
        keyboard = [
            [InlineKeyboardButton("💳 Click orqali to'lash", url="https://click.uz")],
            [InlineKeyboardButton("💳 Payme orqali to'lash", url="https://payme.uz")],
            [InlineKeyboardButton("📞 Admin bilan bog'lanish", url="https://t.me/ilmhub_admin")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data=f"course_{course_id}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"💳 *To'lov ma'lumotlari:*\n\n"
            f"📚 Kurs: {course['name']}\n"
            f"💰 Summa: *{course['price']:,} so'm*\n\n"
            f"To'lov usulini tanlang:\n"
            f"• Click yoki Payme orqali to'lang\n"
            f"• To'lovdan so'ng chekni adminga yuboring\n"
            f"• Admin 1 soat ichida kursni ochadi\n\n"
            f"📞 Admin: @ilmhub_admin",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        # Adminga xabar
        await notify_admin(context, f"💰 Yangi to'lov so'rovi!\n👤 {user.first_name} (@{user.username})\n📚 {course['name']}\n💵 {course['price']:,} so'm")

# ============================================================
# TOPSHIRIQLAR YUBORISH (admin buyrug'i)
# ============================================================
async def send_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: /task english_a1 3  ->  3-dars topshirig'ini yuboradi"""
    user = update.effective_user
    
    # Admin tekshirish
    if ADMIN_ID and user.id != ADMIN_ID:
        await update.message.reply_text("❌ Bu buyruq faqat admin uchun!")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "Ishlatish: /task [kurs_id] [dars_raqami]\n"
            "Misol: /task english_a1 3"
        )
        return
    
    course_id = context.args[0]
    try:
        lesson_num = int(context.args[1])
    except:
        await update.message.reply_text("❌ Dars raqami son bo'lishi kerak!")
        return
    
    task = TASKS.get(course_id, {}).get(lesson_num)
    if not task:
        await update.message.reply_text(f"❌ Topshiriq topilmadi: {course_id} dars {lesson_num}")
        return
    
    await update.message.reply_text(
        f"✅ Topshiriq yuborildi!\n\n{task}\n\n"
        f"(Bu xabarni guruhga forward qiling)"
    )

# ============================================================
# YANGI DARS E'LONI (admin buyrug'i)
# ============================================================
async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: /announce Yangi dars qo'shildi!"""
    user = update.effective_user
    
    if ADMIN_ID and user.id != ADMIN_ID:
        await update.message.reply_text("❌ Bu buyruq faqat admin uchun!")
        return
    
    if not context.args:
        await update.message.reply_text("Ishlatish: /announce [xabar matni]")
        return
    
    message = " ".join(context.args)
    
    await update.message.reply_text(
        f"📢 *E'lon:*\n\n{message}\n\n"
        f"🔗 Sayt: https://gofurovyusufxon50-alt.github.io/ilmhub/ilmhub.html",
        parse_mode='Markdown'
    )

# ============================================================
# MENING ID (admin ID ni topish uchun)
# ============================================================
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👤 Sizning ma'lumotlaringiz:\n"
        f"🆔 ID: `{user.id}`\n"
        f"👤 Ism: {user.first_name}\n"
        f"📱 Username: @{user.username or 'yo\'q'}",
        parse_mode='Markdown'
    )

# ============================================================
# YORDAM
# ============================================================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "📞 *Yordam kerakmi?*\n\n"
            "👤 Admin: @ilmhub_admin\n"
            "🌐 Sayt: ilmhub.uz\n\n"
            "Savol va takliflaringizni adminga yuboring!",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]])
        )

# ============================================================
# MENING KURSLARIM
# ============================================================
async def my_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "👤 *Mening kurslarim:*\n\n"
        "Hozircha sotib olingan kurslar yo'q.\n\n"
        "Kurs sotib olish uchun /start bosing!",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📚 Kurslar", callback_data="courses")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]
        ])
    )

# ============================================================
# ORQAGA
# ============================================================
async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📚 Kurslar ro'yxati", callback_data="courses")],
        [InlineKeyboardButton("💳 To'lov qilish", callback_data="payment")],
        [InlineKeyboardButton("📞 Yordam", callback_data="help")],
        [InlineKeyboardButton("👤 Mening kurslarim", callback_data="my_courses")],
    ]
    await query.edit_message_text(
        "🎓 *IlmHub* — Bosh menyu\n\nBo'limni tanlang:",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def payment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "💳 *To'lov usullari:*\n\n"
        "• Click: click.uz\n"
        "• Payme: payme.uz\n"
        "• Karta: Admin orqali\n\n"
        "To'lovdan so'ng chekni adminga yuboring:\n"
        "@ilmhub_admin",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]])
    )

# ============================================================
# ADMIN GA XABAR
# ============================================================
async def notify_admin(context: ContextTypes.DEFAULT_TYPE, message: str):
    if ADMIN_ID:
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Admin xabar yuborishda xato: {e}")

# ============================================================
# NOMA'LUM XABAR
# ============================================================
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Kechirasiz, bu buyruqni tushunmadim 🤔\n\n"
        "Boshlash uchun /start yozing!"
    )

# ============================================================
# MAIN
# ============================================================
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Komandalar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("task", send_task))
    app.add_handler(CommandHandler("announce", announce))
    app.add_handler(CommandHandler("help", lambda u,c: u.message.reply_text("Yordam: /start")))
    
    # Callback handlers
    app.add_handler(CallbackQueryHandler(show_courses, pattern="^courses$"))
    app.add_handler(CallbackQueryHandler(show_course_detail, pattern="^course_"))
    app.add_handler(CallbackQueryHandler(buy_course, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(help_cmd, pattern="^help$"))
    app.add_handler(CallbackQueryHandler(my_courses, pattern="^my_courses$"))
    app.add_handler(CallbackQueryHandler(back_main, pattern="^back_main$"))
    app.add_handler(CallbackQueryHandler(payment_info, pattern="^payment$"))
    
    # Noma'lum xabarlar
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    
    print("🤖 IlmHub Bot ishga tushdi!")
    print("Botni to'xtatish uchun: Ctrl+C")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
