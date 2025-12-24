import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_snap(driver, caption):
    try:
        path = f"snap_{int(time.time())}.png"
        driver.save_screenshot(path)
        with open(path, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})
    except: pass

def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def run_bot():
    options = Options()
    # أهم إعدادات التنكر
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # بصمة جهاز ويندوز حقيقي
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    ]
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # حذف بصمة الـ Webdriver عبر الجافا سكربت
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # 1. الدخول لجوجل أولاً للتمويه
        driver.get("https://www.google.com")
        time.sleep(random.uniform(3, 5))
        
        # 2. التوجه للموقع
        driver.get("https://www.like4like.org/")
        time.sleep(random.uniform(5, 8))
        send_snap(driver, "🌐 دخلت الصفحة الرئيسية.. سأنتظر كبشري")

        # 3. محاولة الضغط على Register كبشر
        try:
            reg_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Register")
            ActionChains(driver).move_to_element(reg_link).pause(1).click().perform()
        except:
            driver.get("https://www.like4like.org/register.php")

        time.sleep(8)
        send_snap(driver, "📸 فحص صفحة التسجيل بعد التنكر")

        if "username" in driver.page_source:
            user = f"jasser_{random.randint(1000, 9999)}"
            human_type(driver.find_element(By.ID, "username"), user)
            send_snap(driver, f"✅ نجحت في كسر الحماية! جاري كتابة اليوزر: {user}")
        else:
            send_snap(driver, "⚠️ ما زال الحظر موجوداً (صفحة 404/الكابتشا)")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
