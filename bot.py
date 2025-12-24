import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# 🔑 بيانات البوت الخاصة بك
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

# 📧 بيانات تسجيل الدخول التي قدمتها
EMAIL_DATA = "61583389620613"
PASSWORD_DATA = "jasser malo"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def send_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(photo_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})
    except Exception as e:
        print(f"Error: {e}")

def run_bot():
    send_msg("🚀 بدأت محاولة تسجيل الدخول إلى فيسبوك...")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1080,1920')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.facebook.com")
        time.sleep(5)
        
        # 1. استخراج حقل البريد وإدخال الرقم
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(EMAIL_DATA)
        
        # 2. استخراج حقل كلمة المرور وإدخال النص
        pass_input = driver.find_element(By.ID, "pass")
        pass_input.send_keys(PASSWORD_DATA)
        
        # 3. الضغط على زر تسجيل الدخول
        try:
            # محاولة الضغط عبر الاسم أو المعرف المشهور لزر الدخول
            login_button = driver.find_element(By.NAME, "login")
            login_button.click()
        except:
            # إذا فشل، نضغط Enter في حقل كلمة المرور
            pass_input.send_keys(Keys.ENTER)
        
        send_msg("⏳ تم إدخال البيانات والضغط على تسجيل الدخول.. انتظار النتيجة.")
        time.sleep(8) # انتظار تحميل الصفحة بعد الدخول
        
        # التقاط الصورة النهائية
        photo_name = "login_result.png"
        driver.save_screenshot(photo_name)
        send_photo(photo_name, "📸 نتيجة محاولة تسجيل الدخول")

    except Exception as e:
        send_msg(f"❌ حدث خطأ أثناء العملية: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
