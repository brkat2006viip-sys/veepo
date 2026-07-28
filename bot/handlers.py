import os
import logging
import tempfile
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import CommandStart, Text
from aiogram import Bot
from aiogram.types import FSInputFile

from bot.keyboards import main_menu, cancel_kb
from services.project_processor import ProjectProcessor
from app.crud import save_user_setting, create_project, log_operation

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, db, db_user):
    await message.answer("مرحبًا! أنا وكيلك البرمجي بالذكاء الاصطناعي. اختر من القائمة:", reply_markup=main_menu())
    if db_user:
        await log_operation(db, db_user.id, None, "start", f"/start by @{db_user.username}")

@router.callback_query()
async def menu_callback(query: CallbackQuery, bot: Bot, db, db_user):
    data = query.data or ""
    if data == "new_project":
        await query.message.answer("أرسل ملف ZIP للمشروع الآن (أو اكتب اسم المشروع لإنشاء مشروع جديد فارغ).", reply_markup=cancel_kb())
        await query.answer()
        # mark state? we will handle by content type
    elif data == "my_projects":
        # list projects
        await query.message.answer("قائمة مشاريعي: (قيد التطوير إرسال كمثال)")
        await query.answer()
    elif data == "api_key":
        await query.message.answer("أرسل مفتاح AgentRouter الخاص بك الآن (ستُخزن مشفّرة).", reply_markup=cancel_kb())
        await query.answer()
    elif data == "help":
        await query.message.answer("تعليمات الاستخدام:\n- أرسل ZIP لتحليل مشروع.\n- استخدم الأزرار للتنقّل.")
        await query.answer()
    else:
        await query.answer()

@router.message(F.content_type == ContentType.DOCUMENT)
async def handle_document(message: Message, bot: Bot, db, db_user):
    doc = message.document
    if not doc.file_name.lower().endswith(".zip"):
        await message.reply("الملف المرسل ليس ZIP. رجاءً أرسل أرشيف ZIP.")
        return
    # download
    temp_dir = tempfile.mkdtemp(prefix="tg_project_")
    file_path = os.path.join(temp_dir, doc.file_name)
    await doc.download(destination=file_path)
    await message.answer("تم استلام الأرشيف، جاري تحليله...")
    processor = ProjectProcessor(db=db, user=db_user)
    project = await processor.create_from_zip(file_path)
    await message.answer(f"تم إنشاء مشروع: {project.name}\nتشغيل تحليل...")
    analysis = await processor.analyze_project(project.path)
    # save project record
    db_project = await create_project(db, db_user.id, project.name, project.path, project.zip_path)
    await log_operation(db, db_user.id, db_project.id, "upload_zip", f"Uploaded {doc.file_name}")
    # send simple report
    report = f"ملفات: {analysis.file_count}\nسطر كود تقريبي: {analysis.loc}\nلغات: {analysis.languages}"
    await message.answer(report)
    await message.answer("هل تريد أن أرسل الملفات إلى AgentRouter لمعالجة أو تنفيذ تعليمات؟ (أرسل /process أو اكتب تعليمات.)")
    # cleanup temp (processor may have moved things)
    try:
        import shutil
        shutil.rmtree(temp_dir)
    except Exception:
        logger.exception("Failed to cleanup temp dir")
