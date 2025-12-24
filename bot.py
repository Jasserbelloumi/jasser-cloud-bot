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

def send_snap(driver, caption):
    path = "action_view.png"
    driver.save_screenshot(path)
    with open(path, 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=412,1600') # أطول لرؤية كل شيء
    options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)
        
        # إذا واجهنا رسالة الخطأ الحمراء
        if "CAPTCHA wasn't entered correctly" in driver.page_source or "Error 404" in driver.page_source:
            send_snap(driver, "🧩 الكابتشا تطلب حلاً يدوياً. سأحاول فتح نافذة الصور...")
            
            try:
                # محاولة النقر على المربع مرة أخرى بقوة
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                for i, frame in enumerate(frames):
                    driver.switch_to.frame(frame)
                    if "recaptcha" in driver.page_source:
                        anchor = driver.find_elements(By.ID, "recaptcha-anchor")
                        if anchor:
                            driver.execute_script("arguments[0].click();", anchor[0])
                            time.sleep(5)
                            driver.switch_to.default_content()
                            send_snap(driver, "📸 هل ظهرت صور الاختيار الآن؟")
                            break
                    driver.switch_to.default_content()
            except: pass

        # سيبقى البوت يعمل لمدة دقيقتين ليعطيك فرصة لتوجيهه
        time.sleep(60) 
        send_snap(driver, "⏳ انتهى وقت الانتظار. هل نكرر المحاولة؟")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
