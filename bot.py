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
    notify("🕵️ جاري محاولة التسلل للموقع...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # خطوة تمويه: الدخول لجوجل
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # الدخول للموقع
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)

        # فحص المحتوى قبل أي شيء
        driver.save_screenshot("current_state.png")
        
        if "username" in driver.page_source:
            notify("✅ الصفحة جاهزة، بدأت عملية الإدخال...")
            user = f"jsr{random.randint(10000, 99999)}"
            pwd = "Jasser@User2025"
            email = f"{user}@1secmail.com"
            
            driver.find_element(By.ID, "username").send_keys(user)
            driver.find_element(By.ID, "password").send_keys(pwd)
            driver.find_element(By.ID, "password_re").send_keys(pwd)
            driver.find_element(By.ID, "email").send_keys(email)
            driver.find_element(By.ID, "email_re").send_keys(email)
            
            # الضغط على الموافقة عبر JS لضمان التنفيذ
            check = driver.find_element(By.ID, "agree")
            driver.execute_script("arguments[0].click();", check)
            
            notify(f"🔹 تم ملء بيانات الحساب: {user}\nجاري محاولة الإرسال...")
            
            submit = driver.find_element(By.NAME, "submit")
            driver.execute_script("arguments[0].click();", submit)
            time.sleep(10)
            
            driver.save_screenshot("final.png")
            notify("🏁 النتيجة النهائية بعد الضغط:", "final.png")
        else:
            notify("⚠️ لم أجد حقول التسجيل. انظر ماذا يظهر لي الآن:", "current_state.png")

    except Exception as e:
        driver.save_screenshot("crash.png")
        notify(f"🚨 حدث انهيار مفاجئ:\n{str(e)[:100]}", "crash.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
