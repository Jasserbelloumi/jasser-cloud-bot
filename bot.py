import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 🔑 بياناتك
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_photo(photo_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(photo_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID, 'caption': "📸 لقطة شاشة لصفحة فيسبوك"}, files={'photo': f})
    except Exception as e:
        print(f"Error sending photo: {e}")

def run_bot():
    print("🚀 جاري تشغيل المتصفح والدخول إلى فيسبوك...")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1080,1920') # أبعاد واضحة
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # الدخول لموقع فيسبوك
        driver.get("https://www.facebook.com")
        time.sleep(5) # انتظار تحميل الصفحة
        
        # التقاط الصورة
        photo_name = "facebook_screen.png"
        driver.save_screenshot(photo_name)
        print("✅ تم التقاط الصورة.")
        
        # إرسال الصورة
        send_photo(photo_name)
        print("📤 تم إرسال الصورة إلى تليجرام.")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
