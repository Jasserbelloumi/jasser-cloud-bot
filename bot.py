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
    # مسار حفظ الصورة
    path = "long_status.png"
    # تصوير الصفحة كاملة بأبعادها الطويلة
    driver.save_screenshot(path)
    with open(path, 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # 📱 إعدادات الأبعاد لتصبح عمودية وطويلة (412 عرض × 1500 طول)
    options.add_argument('--window-size=412,1500')
    options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(12)
        
        # التقاط صورة عمودية طويلة للموقف الحالي
        send_snap(driver, "📱 لقطة شاشة عمودية (طراز هاتف طويل)")
        
        if "Error 404" in driver.page_source:
            try:
                # محاولة ملء النص والضغط برمجياً
                text_area = driver.find_element(By.TAG_NAME, "textarea")
                text_area.send_keys("Requesting access to sign up")
                
                # التعامل مع الكابتشا داخل الإطار
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                if frames:
                    driver.switch_to.frame(frames[0])
                    driver.execute_script("document.getElementById('recaptcha-anchor').click();")
                    driver.switch_to.default_content()
                
                time.sleep(5)
                submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                driver.execute_script("arguments[0].click();", submit_btn)
                
                time.sleep(10)
                send_snap(driver, "📸 نتيجة المحاولة (لقطة عمودية)")
                
            except Exception as e:
                send_msg(f"❌ خطأ: {str(e)[:50]}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
