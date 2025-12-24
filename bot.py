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
    notify("🚀 جاري محاولة تسجيل الحساب الآن...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    try:
        # الدخول للموقع عبر الرابط المباشر (جربنا أنه يعمل بعد الدخول للرئيسية)
        driver.get("https://www.like4like.org/register.php")
        time.sleep(5)

        user = f"jsr{random.randint(10000, 99999)}"
        pwd = "Jasser@User2025"
        email = f"{user}@1secmail.com"

        # ملء البيانات
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(user)
        driver.find_element(By.ID, "password").send_keys(pwd)
        driver.find_element(By.ID, "password_re").send_keys(pwd)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "email_re").send_keys(email)
        driver.find_element(By.ID, "agree").click()

        notify(f"📝 تم ملء البيانات:\n👤: {user}\n📧: {email}\nجاري الضغط على التسجيل...")
        
        # الضغط على زر التسجيل (نبحث عنه بالقيمة أو النص)
        try:
            submit_btn = driver.find_element(By.NAME, "submit")
            submit_btn.click()
            time.sleep(7)
        except:
            driver.save_screenshot("error_btn.png")
            notify("⚠️ لم أجد زر التسجيل!", "error_btn.png")

        # التقاط صورة للنتيجة النهائية
        driver.save_screenshot("result.png")
        notify("📸 انظر للنتيجة بعد محاولة التسجيل:", "result.png")

    except Exception as e:
        notify(f"❌ خطأ تقني: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
