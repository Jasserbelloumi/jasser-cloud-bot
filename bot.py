import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # 🌍 إضافة بروكسي مجاني للتمويه (فرنسا/ألمانيا)
    # ملاحظة: البروكسيات المجانية قد تكون بطيئة أو تتوقف
    proxies = [
        "51.158.154.173:3128", 
        "162.19.171.169:3128"
    ]
    options.add_argument(f'--proxy-server={random.choice(proxies)}')
    
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # محاولة الدخول لصفحة التسجيل
        driver.get("https://www.like4like.org/register.php")
        time.sleep(15)
        
        driver.save_screenshot("step1.png")
        
        # إذا ظهرت صفحة 404، نضغط على Home Page كما اقترحت
        if "404" in driver.page_source or "reCAPTCHA" in driver.page_source:
            notify("🛡️ حظر الـ IP مستمر. سأضغط الآن على 'Home Page' للتمويه...", "step1.png")
            try:
                home_btn = driver.find_element(By.LINK_TEXT, "Home Page")
                home_btn.click()
                time.sleep(7)
                driver.save_screenshot("step2.png")
                notify("🏠 أنا الآن في الصفحة الرئيسية. سأحاول العودة لصفحة التسجيل كبشري.", "step2.png")
                
                # العودة للتسجيل بعد التمويه
                driver.get("https://www.like4like.org/register.php")
                time.sleep(10)
                driver.save_screenshot("step3.png")
            except:
                notify("❌ فشلت في العثور على زر Home Page.")

        # التحقق النهائي
        if "username" in driver.page_source:
            notify("✅ نجح الاختراق! الحقول ظهرت أخيراً.")
        else:
            notify("⚠️ لا يزال الموقع يكتشف البروكسي/السيرفر.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
