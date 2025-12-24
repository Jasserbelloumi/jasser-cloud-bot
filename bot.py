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

def notify_and_wait(msg, img=None):
    try:
        if img:
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': msg}, files={'photo': f})
        else:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg})
        
        last_id = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()['result'][-1]['update_id'] if requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()['result'] else 0
        while True:
            time.sleep(5)
            updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_id + 1}).json()
            for up in updates.get('result', []):
                if str(up['message']['chat']['id']) == CHAT_ID:
                    return up['message'].get('text', 'done')
    except: return "done"

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # 🕵️ تغيير الهوية إلى ويندوز حقيقي (أكثر استقراراً من الهاتف في التخفي)
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument("--window-size=1920,1080")
    
    # إخفاء بصمة الأتمتة
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # الدخول للموقع
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)
        
        driver.save_screenshot("check.png")
        if "reCAPTCHA" in driver.page_source or "404" in driver.page_source:
            notify_and_wait("🛡️ الموقع كشف الـ IP! سأحاول الضغط على Home Page.. ارسل أي رسالة للمتابعة بعد الضغط", "check.png")
            try:
                driver.find_element(By.LINK_TEXT, "Home Page").click()
                time.sleep(5)
                driver.save_screenshot("home.png")
                notify_and_wait("🏠 أنا الآن في الرئيسية، هل أحاول الدخول للتسجيل مجدداً؟", "home.png")
                driver.get("https://www.like4like.org/register.php")
                time.sleep(10)
            except: pass

        # محاولة أخيرة للملء
        if "username" in driver.page_source:
            user = f"jsr_{random.randint(1000, 9999)}"
            driver.find_element(By.ID, "username").send_keys(user)
            driver.save_screenshot("success.png")
            notify_and_wait(f"✅ مذهل! الحقول ظهرت وكتبت اليوزر: {user}", "success.png")
        else:
            driver.save_screenshot("failed.png")
            notify_and_wait("❌ لا يزال الحظر قائماً. نحتاج لاستخدام Proxy خارجي.", "failed.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
