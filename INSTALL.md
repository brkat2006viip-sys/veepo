دليل التثبيت المحلي

1) تثبيت Python 3.12
   - Ubuntu 22.04/24.04:
     sudo apt update
     sudo apt install -y python3.12 python3.12-venv python3.12-dev build-essential

   - أو استخدم pyenv أو التنزيل من python.org

2) إنشاء بيئة افتراضية
   cd /path/to/telegram-ai-bot
   python3.12 -m venv .venv
   source .venv/bin/activate

3) تثبيت المتطلبات
   pip install --upgrade pip
   pip install -r requirements.txt

4) إعداد ملف .env
   - انسخ .env.example إلى .env
   - عدّل TELEGRAM_BOT_TOKEN وFERNET_KEY وAGENTROUTER_API_URL حسب الحاجة.
   - لإنشاء FERNET_KEY:
       python - <<'PY'
       from utils.security import generate_fernet_key
       print(generate_fernet_key())
       PY
     ثم ضع القيمة في .env

5) تهيئة قاعدة البيانات
   عند تشغيل التطبيق سيقوم بإنشاء قاعدة SQLite تلقائيًا:
     python main.py
   أو تشغيل:
     python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"

6) تشغيل البوت محليًا
   python main.py
   - تحقق من أن البوت متصل عبر تلغرام ويتلقى /start

7) تشغيل البوت كخدمة systemd (تلقائي بعد إعادة التشغيل)

1) تحديث النظام
   sudo apt update && sudo apt upgrade -y

2) تثبيت Git وPython
   sudo apt install -y git python3.12 python3.12-venv

3) استنساخ المشروع
   sudo mkdir -p /opt/telegram-ai-bot
   sudo chown $USER:$USER /opt/telegram-ai-bot
   git clone <your-repo-url> /opt/telegram-ai-bot

4) إعداد البيئة
   cd /opt/telegram-ai-bot
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt

5) إعداد .env
   cp .env.example .env
   # ثم عدّل .env وأدخل TELEGRAM_BOT_TOKEN وFERNET_KEY وAGENTROUTER_API_URL

6) اختبار التشغيل
   python main.py
   - راجع logs/bot.log أو المخرجات في التيرمنال

7) إعداد systemd
   - ضع الملف `telegram-ai-bot.service.example` كـ `/etc/systemd/system/telegram-ai-bot.service`
   - عدّل المسارات واسم المستخدم.
   sudo systemctl daemon-reload
   sudo systemctl enable telegram-ai-bot
   sudo systemctl start telegram-ai-bot
   sudo systemctl status telegram-ai-bot

8) سجلات وتشغيل وأوامر مفيدة
   - مشاهدة السجلات:
     sudo journalctl -u telegram-ai-bot -f
   - إعادة التشغيل:
     sudo systemctl restart telegram-ai-bot
   - التحديث:
     cd /opt/telegram-ai-bot
     git pull
     source .venv/bin/activate
     pip install -r requirements.txt
     sudo systemctl restart telegram-ai-bot

النسخ الاحتياطي والاستعادة
- النسخ الاحتياطي:
    tar czf backup_$(date +%F).tar.gz data uploads .env
- الاستعادة:
    tar xzf backup_YYYY-MM-DD.tar.gz -C /opt/telegram-ai-bot

ملاحظات أمان
- لا تحتفظ بمفاتيح API في ملفات غير مشفّرة.
- امنع الوصول العام إلى مجلد data/uploads/temp.
- استخدم حساب محدود الصلاحيات لتشغيل الخدمة systemd.
