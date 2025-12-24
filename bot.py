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
    if img:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': msg}, files={'photo': open(img, 'rb')})
    else:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg})

def run_bot():
    notify("🚀 محاولة جديدة بدأت...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get("https://www.like4like.org/register/")
        time.sleep(10) # ننتظر قليلاً لضمان تحميل الصفحة
        
        if "username" in driver.page_source:
            notify("✅ الصفحة فتحت بنجاح وجاري التسجيل...")
            # هنا نكمل بقية الخطوات...
        else:
            driver.save_screenshot("view.png")
            notify("⚠️ لم أجد حقول التسجيل، انظر للصورة المرفقة:", "view.png")
            
    except Exception as e:
        notify(f"❌ خطأ: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
