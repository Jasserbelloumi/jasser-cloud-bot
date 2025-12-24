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
    path = "captcha_check.png"
    driver.save_screenshot(path)
    with open(path, 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=500,1600')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)

        # 🎯 محاولة النقر بكل الطرق الممكنة
        found = False
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for index, frame in enumerate(iframes):
            try:
                driver.switch_to.frame(frame)
                # البحث عن المربع بالمعرف الشهير لـ recaptcha
                checkbox = driver.find_elements(By.ID, "recaptcha-anchor")
                if checkbox:
                    # النقر باستخدام جافا سكريبت لضمان التنفيذ
                    driver.execute_script("arguments[0].click();", checkbox[0])
                    found = True
                    driver.switch_to.default_content()
                    break
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()

        if found:
            time.sleep(8) # انتظار ظهور صور التحدي
            send_snap(driver, "✅ تم النقر بنجاح! هل ظهرت الصور الآن؟")
        else:
            send_snap(driver, "❌ لم أجد مربع الكابتشا للنقر عليه.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
