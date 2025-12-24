import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def send_snap(driver, caption):
    path = "status.png"
    driver.save_screenshot(path)
    with open(path, 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)
        
        # التعامل مع صفحة 404 والكابتشا
        if "Error 404" in driver.page_source:
            send_snap(driver, "⚠️ اكتشفت صفحة الحماية 404. سأحاول إدخال نص والضغط على الكابتشا.")
            
            try:
                # 1. إدخال نص في الحقل الموجود
                text_area = driver.find_element(By.TAG_NAME, "textarea")
                text_area.send_keys("I want to register a new account")
                
                # 2. الانتقال للـ iframe الخاص بالكابتشا
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                if frames:
                    driver.switch_to.frame(frames[0])
                    checkbox = driver.find_element(By.ID, "recaptcha-anchor")
                    checkbox.click()
                    driver.switch_to.default_content()
                    
                time.sleep(5)
                # 3. الضغط على زر Submit
                submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                submit_btn.click()
                
                time.sleep(10)
                send_snap(driver, "📸 بعد محاولة تخطي صفحة 404")
            except Exception as e:
                send_msg(f"❌ فشل التفاعل التلقائي: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
