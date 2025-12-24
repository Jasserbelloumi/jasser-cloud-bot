import os
import time
import random
import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# إعداد السجلات (Logging) لمعرفة الأخطاء بدقة
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# جلب البيانات من متغيرات البيئة (أمان عالي)
TOKEN = os.getenv("BOT_TOKEN", "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w")
CHAT_ID = os.getenv("CHAT_ID", "5653032481")

def notify(msg, img=None):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/"
        if img:
            with open(img, 'rb') as f:
                requests.post(url + "sendPhoto", data={'chat_id': CHAT_ID, 'caption': msg}, files={'photo': f}, timeout=10)
        else:
            requests.post(url + "sendMessage", json={'chat_id': CHAT_ID, 'text': msg}, timeout=10)
    except Exception as e:
        logger.error(f"Telegram Notify Error: {e}")

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # محاولة تشغيل الدرايفر بطريقة مستقرة
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def run_bot():
    driver = None
    try:
        logger.info("🚀 بدء تشغيل البوت الاحترافي...")
        driver = get_driver()
        wait = WebDriverWait(driver, 20)
        
        # 1. الدخول للموقع
        driver.get("https://www.like4like.org/register.php")
        
        # 2. الانتظار الذكي لتحميل الصفحة (بدلاً من sleep)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # 3. فحص وجود حقول التسجيل بدقة
        fields = ["username", "password", "email"]
        found = all([len(driver.find_elements(By.ID, f)) > 0 for f in fields])
        
        if found:
            notify("✅ تم العثور على حقول التسجيل بنجاح باستخدام الانتظار الذكي.")
            # ملء البيانات...
        else:
            driver.save_screenshot("debug.png")
            # فحص الكابتشا بطريقة أدق
            if len(driver.find_elements(By.CLASS_NAME, "g-recaptcha")) > 0:
                notify("🧩 تم اكتشاف reCAPTCHA (عنصر iframe).", "debug.png")
            else:
                notify("⚠️ الصفحة محملة ولكن الحقول غير موجودة (احتمال حظر IP).", "debug.png")

    except Exception as e:
        logger.error(f"General Error: {e}")
        notify(f"❌ حدث خطأ تقني: {str(e)}")
        if driver:
            driver.save_screenshot("crash_error.png")
            notify("📸 صورة الخطأ:", "crash_error.png")
    finally:
        if driver:
            driver.quit()
            logger.info("🔒 تم إغلاق المتصفح بنجاح.")

if __name__ == "__main__":
    run_bot()
