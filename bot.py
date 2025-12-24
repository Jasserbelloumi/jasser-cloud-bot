import time
import os
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 🔑 تأكد من أن هذه البيانات صحيحة 100%
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={'chat_id': CHAT_ID, 'text': text}, timeout=10)
    except:
        pass

def send_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(photo_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f}, timeout=20)
    except Exception as e:
        send_msg(f"❌ فشل إرسال الصورة: {str(e)}")

def run_bot():
    # 1. إرسال رسالة تجربة فورية
    send_msg("🔔 البوت بدأ العمل الآن.. جاري تشغيل المحرك.")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1000,2000')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        send_msg("🌐 جاري فتح الموقع...")
        driver.get("https://www.like4like.org/register.php")
        time.sleep(12)
        
        # محاولة النقر على الكابتشا
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            try:
                driver.switch_to.frame(frame)
                checkbox = driver.find_elements(By.ID, "recaptcha-anchor")
                if checkbox:
                    driver.execute_script("arguments[0].click();", checkbox[0])
                    driver.switch_to.default_content()
                    send_msg("🖱️ تم النقر على المربع.. انتظار الصور.")
                    time.sleep(10)
                    break
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()

        # التقاط الصورة (بدون رسم شبكة مؤقتاً لضمان الإرسال)
        path = "screen.png"
        driver.save_screenshot(path)
        send_photo(path, "📸 لقطة الشاشة الحالية (بدون شبكة للتجربة)")

    except Exception as e:
        error_msg = traceback.format_exc()
        send_msg(f"⚠️ حدث خطأ أثناء التشغيل:\n{error_msg[:300]}")
    finally:
        if driver:
            driver.quit()
        send_msg("🏁 انتهت الجلسة.")

if __name__ == "__main__":
    run_bot()
