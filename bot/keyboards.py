from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📂 مشروع جديد", callback_data="new_project"),
        InlineKeyboardButton("📜 مشاريعي", callback_data="my_projects"),
        InlineKeyboardButton("🤖 اختيار النموذج", callback_data="choose_model"),
        InlineKeyboardButton("🔑 مفتاح API", callback_data="api_key"),
        InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings"),
        InlineKeyboardButton("📊 حالة المهمة", callback_data="task_status"),
        InlineKeyboardButton("❓ المساعدة", callback_data="help"),
        InlineKeyboardButton("👤 حسابي", callback_data="account"),
    )
    return kb

def cancel_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("إلغاء", callback_data="cancel"))
    return kb
