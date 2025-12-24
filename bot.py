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

def send_live_snap(driver, caption="📸 لقطة حية"):
    """دالة لإرسال لقطة شاشة فورية"""
    try:
        filename = f"snap_{int(time.time())}.png"
        driver.save_screenshot(filename)
        with open(filename, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})
    except: pass

def notify_and_wait(msg):
    """إرسال رسالة والانتظار لردك"""
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg})
    last_id = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()['result'][-1]['update_id'] if requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()['result'] else 0
    while True:
        time.sleep(3)
        updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_id + 1}).json()
        for up in updates.get('result', []):
            if str(up['message']['chat']['id']) == CHAT_ID:
                return up['message'].get('text', '').lower()

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # المرحلة 1: الدخول
        driver.get("https://www.like4like.org/register.php")
        send_live_snap(driver, "1️⃣ محاولة الدخول الأولى")
        time.sleep(5)
        
        # المرحلة 2: إذا وجد صفحة 404
        if "Error 404" in driver.page_source:
            send_live_snap(driver, "⚠️ واجهت صفحة 404، سأحاول الضغط على Home")
            try:
                home_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Home")
                home_link.click()
                time.sleep(5)
                send_live_snap(driver, "🏠 بعد الضغط على Home")
            except: pass

        # المرحلة 3: التفاعل معك
        cmd = notify_and_wait("🔄 أنا الآن جاهز، ماذا أفعل؟ (اكتب 'go' للملء أو 'snap' لصورة جديدة)")
        
        if cmd == "snap":
            send_live_snap(driver, "📸 لقطة بطلب منك")
        
        # محاولة ملء الحقول مع تصوير كل حقل
        user = f"jsr{random.randint(1000, 9999)}"
        try:
            user_field = driver.find_element(By.ID, "username")
            user_field.send_keys(user)
            send_live_snap(driver, f"✍️ كتبت اليوزر: {user}")
            
            # يمكنك إضافة إرسال لقطة بعد كل حقل هنا بنفس الطريقة
            
        except:
            send_live_snap(driver, "❌ لم أجد الحقول في هذه الصفحة")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
