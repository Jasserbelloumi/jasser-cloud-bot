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

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def human_type(element, text):
    """محاكاة الكتابة البشرية حرف بحرف"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3)) # تأخير عشوائي بين الحروف

def run_bot():
    send_msg("🕵️ جاري الدخول بوضع 'التخفي البشري' لتجنب الكابتشا...")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1080,1920')
    
    # 🕵️ حيل سحرية لإخفاء هوية البوت:
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # تنفيذ كود لإزالة علامة الـ webdriver من المتصفح
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => False})")

    try:
        driver.get("https://www.facebook.com")
        time.sleep(random.uniform(4, 7)) # انتظار عشوائي كأن الشخص يقرأ الصفحة
        
        # إدخال البريد بطريقة بشرية
        email_field = driver.find_element(By.ID, "email")
        human_type(email_field, "61583389620613")
        time.sleep(random.uniform(1, 3))
        
        # إدخال كلمة المرور بطريقة بشرية
        pass_field = driver.find_element(By.ID, "pass")
        human_type(pass_field, "jasser malo")
        time.sleep(random.uniform(1, 2))
        
        # النقر على زر الدخول
        login_btn = driver.find_element(By.NAME, "login")
        login_btn.click()
        
        send_msg("⏳ تم إرسال البيانات.. ننتظر لنرى هل تم خداع النظام!")
        time.sleep(10)
        
        driver.save_screenshot("result.png")
        with open("result.png", 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "📸 النتيجة بعد محاولة التخفي"}, files={'photo': f})

    except Exception as e:
        send_msg(f"❌ خطأ: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
