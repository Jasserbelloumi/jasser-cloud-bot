import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def notify(msg, img=None):
    try:
        if img:
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': msg}, files={'photo': f})
        else:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def run_bot():
    notify("🔄 محاولة الدخول عبر الصفحة الرئيسية لتجنب خطأ 404...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # تحديث الـ User-Agent لنسخة أحدث
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    try:
        # الدخول للصفحة الرئيسية أولاً
        driver.get("https://www.like4like.org/")
        time.sleep(5)

        # البحث عن زر Register والضغط عليه
        try:
            register_btn = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "REGISTER")))
            register_btn.click()
            time.sleep(5)
        except:
            driver.get("https://www.like4like.org/register.php") # محاولة الرابط البديل بصيغة php

        # تفقد هل ظهرت الحقول؟
        if "username" in driver.page_source:
            notify("✅ تم الوصول لصفحة التسجيل بنجاح! جاري ملء البيانات...")
            # هنا نضع منطق الملء...
            user = f"jsr_{random.randint(1000, 9999)}"
            driver.find_element(By.ID, "username").send_keys(user)
            # ... (باقي الكود)
        else:
            driver.save_screenshot("check.png")
            notify("⚠️ لا يزال الموقع يظهر صفحة مختلفة. انظر للصورة:", "check.png")

    except Exception as e:
        notify(f"❌ خطأ تقني جديد: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
