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
    # نضبط المتصفح ليكون طويلاً جداً لضمان عدم قطع أي جزء
    original_size = driver.get_window_size()
    driver.set_window_size(500, 2000) 
    
    path = "full_captcha_view.png"
    driver.save_screenshot(path)
    with open(path, 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                      data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})
    
    # إعادة الحجم الأصلي بعد التصوير
    driver.set_window_size(original_size['width'], original_size['height'])

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=500,1500')
    options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)
        
        # محاولة إظهار الكابتشا إذا لم تكن ظاهرة
        try:
            frames = driver.find_elements(By.TAG_NAME, "iframe")
            for frame in frames:
                if "recaptcha" in frame.get_attribute("src"):
                    driver.switch_to.frame(frame)
                    anchor = driver.find_elements(By.ID, "recaptcha-anchor")
                    if anchor:
                        driver.execute_script("arguments[0].click();", anchor[0])
                    driver.switch_to.default_content()
                    time.sleep(5) # انتظار ظهور صور التحدي
        except: pass

        # تصوير الصفحة كاملة مع التركيز على منطقة الكابتشا
        send_snap(driver, "📸 لقطة شاشة كاملة (انظر أسفل الصفحة لرؤية الكابتشا كاملة)")

        # انتظار إضافي في حال كانت الصور تتحمل ببطء
        time.sleep(15)
        send_snap(driver, "🔄 تحديث الصورة (للتأكد من ظهور المربعات كاملة)")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
