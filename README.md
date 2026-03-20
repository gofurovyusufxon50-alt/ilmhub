# IlmHub — Online Ta'lim Platformasi

IlmHub - bu O'zbekistondagi #1 online ta'lim platformasi bo'lib, u orqali foydalanuvchilar professional kurslarni o'rganishlari va o'z bilimlarini daromadga aylantirishlari mumkin.

## Loyiha tarkibi

- **Veb-sayt**: `ilmhub.html` - Asosiy platforma (HTML/CSS/JS).
- **Telegram Bot**: `ilmhub_bot.py` - O'quvchilar va adminlar uchun yordamchi bot.

## Imkoniyatlar

- 📚 **Kurslar Katalogi**: Turli yo'nalishlardagi professional kurslar.
- 👤 **Shaxsiy Kabinet**: O'quvchining progressi, XP va yutuqlari.
- ⚙️ **Admin Panel**: Kurslarni boshqarish, buyurtmalarni ko'rish va sozlamalar.
- 🌍 **Ko'p tilli**: O'zbek, Rus va Ingliz tillari qo'llab-quvvatlanadi.
- 📱 **Responsive Design**: Barcha qurilmalarda (mobil, planshet, desktop) to'g'ri ko'rinadi.

## O'rnatish va Ishga tushirish

### Veb-sayt
Veb-saytni ishga tushirish uchun `ilmhub.html` faylini brauzerda ochish kifoya. Loyiha GitHub Pages orqali avtomatik ravishda host qilingan.

### Telegram Bot
Botni ishga tushirish uchun:
1. Python 3.x o'rnatilgan bo'lishi kerak.
2. Kerakli kutubxonalarni o'rnating: `pip install -r requirements.txt`.
3. `.env` faylini yarating va bot tokenini kiriting.
4. Botni ishga tushiring: `python ilmhub_bot.py`.

## Admin Panel
Admin panelga kirish uchun saytning pastki o'ng burchagidagi tishli g'ildirak (⚙️) belgisini bosing.
- **Standart parol**: `admin123456` (Birinchi kirishdan so'ng sozlamalarda o'zgartiring).

## Kamchiliklar va Tuzatishlar (Yaqinda qilingan)
- ✅ SEO va Meta teglar qo'shildi.
- ✅ Mobil qurilmalar uchun responsive dizayn yaxshilandi.
- ✅ Sample ma'lumotlar (kurslar, fikrlar) qo'shildi.
- ✅ Xavfsizlik bo'yicha tavsiyalar va `.env.example` qo'shildi.
