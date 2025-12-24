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
        
        if "Error 404" in driver.page_source:
            send_snap(driver, "🔍 محاولة تجاوز الحظر بالضغط المباشر (JS)...")
            
            try:
                # 1. إدخال النص في الحقل
                text_area = driver.find_element(By.TAG_NAME, "textarea")
                text_area.send_keys("Accessing registration page")
                
                # 2. الانتقال للـ iframe والضغط عبر جافا سكربت
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                if frames:
                    driver.switch_to.frame(frames[0])
                    # استخدام جافا سكربت للضغط لتجنب "Intercepted Click"
                    driver.execute_script("document.getElementById('recaptcha-anchor').click();")
                    driver.switch_to.default_content()
                
                time.sleep(5)
                # 3. الضغط على Submit عبر جافا سكربت أيضاً
                submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                driver.execute_script("arguments[0].click();", submit_btn)
                
                time.sleep(10)
                send_snap(driver, "📸 النتيجة بعد الضغط المباشر")
                
            except Exception as e:
                send_msg(f"❌ فشل الضغط حتى مع JS: {str(e)[:100]}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
