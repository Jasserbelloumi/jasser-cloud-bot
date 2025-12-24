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

def send_full_snap(driver, caption):
    # إجبار المتصفح على أبعاد ضخمة جداً لرؤية النافذة العائمة
    driver.set_window_size(600, 2500)
    time.sleep(2)
    path = "full_view.png"
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

        # 1. البحث عن إطار الكابتشا والنقر عليه
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            try:
                driver.switch_to.frame(frame)
                checkbox = driver.find_elements(By.ID, "recaptcha-anchor")
                if checkbox:
                    driver.execute_script("arguments[0].click();", checkbox[0])
                    driver.switch_to.default_content()
                    time.sleep(7) # انتظار ظهور الصور
                    break
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()

        # 2. الآن، أهم خطوة: جعل نافذة الكابتشا تظهر بالكامل عبر التمرير (Scrolling)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(2)
        
        # 3. إرسال الصورة الكاملة
        send_full_snap(driver, "📸 لقطة شاشة مكبرة وعميقة. هل تظهر الصور كاملة الآن؟")

    except Exception as e:
        send_msg(f"❌ خطأ: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
