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

def send_snap(driver, caption):
    try:
        path = "stealth_check.png"
        driver.save_screenshot(path)
        with open(path, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})
    except: pass

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # 📱 محاكاة هاتف أندرويد حقيقي (Samsung S23)
    user_agent = "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=412,915") # أبعاد هاتف
    
    # إخفاء ملامح الأتمتة
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # حقن كود لجعل المتصفح يقسم أنه ليس "بوت"
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => False });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['ar-DZ', 'ar', 'en-US', 'en'] });
        """
    })

    try:
        # 1. الدخول للرئيسية كأنك تتصفح عادي
        driver.get("https://www.like4like.org/")
        time.sleep(random.uniform(5, 10))
        send_snap(driver, "📱 محاكاة هاتف: دخلت الصفحة الرئيسية")

        # 2. محاكاة ضغطة بشرية على "Register"
        driver.get("https://www.like4like.org/register.php")
        time.sleep(12)
        
        # فحص النتيجة
        if "username" in driver.page_source:
            send_snap(driver, "🔥 نجح التخفي! الحقول ظهرت يا جاسر")
            # هنا سنكمل عملية الملء لاحقاً بعد التأكد من الظهور
        else:
            send_snap(driver, "⚠️ لا زالت صفحة الحماية تظهر رغم التخفي")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
