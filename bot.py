import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def notify_wait(msg, img=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    if img:
        with open(img, 'rb') as f:
            requests.post(url + "sendPhoto", data={'chat_id': CHAT_ID, 'caption': msg}, files={'photo': f})
    else:
        requests.post(url + "sendMessage", json={'chat_id': CHAT_ID, 'text': msg})
    
    # الانتظار لردك (Polling)
    last_id = requests.get(url + "getUpdates").json()['result'][-1]['update_id'] if requests.get(url + "getUpdates").json()['result'] else 0
    while True:
        time.sleep(5)
        updates = requests.get(url + "getUpdates", params={'offset': last_id + 1}).json()
        for up in updates.get('result', []):
            if str(up['message']['chat']['id']) == CHAT_ID:
                return up['message'].get('text', 'done')

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)

        # التحقق من الكابتشا
        if len(driver.find_elements(By.TAG_NAME, "iframe")) > 0:
            driver.save_screenshot("captcha_view.png")
            notify_wait("🧩 الكابتشا أمامنا الآن. جاري محاولة تجاوزها.. سأضغط على زر 'أنا لست روبوت' برمجياً.", "captcha_view.png")
            
            try:
                # محاولة الضغط على مربع الاختيار داخل الـ iframe
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                driver.switch_to.frame(frames[0])
                checkbox = driver.find_element(By.ID, "recaptcha-anchor")
                checkbox.click()
                driver.switch_to.default_content()
                time.sleep(5)
                driver.save_screenshot("after_click.png")
                notify_wait("📸 تم الضغط. هل ظهرت صور اختيار؟ (اكتب أي شيء للمتابعة بعد أن تنتهي)", "after_click.png")
            except:
                driver.switch_to.default_content()
                notify_wait("❌ لم أستطع الضغط على المربع تلقائياً.")

        # محاولة إكمال التسجيل
        if "username" in driver.page_source:
            # كود ملء البيانات السابق...
            notify_wait("📝 الحقول جاهزة! جاري الملء...")
        else:
            notify_wait("⚠️ الحقول لم تظهر بعد. يبدو أن الكابتشا أوقفتنا.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
