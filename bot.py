import time
import os
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw, ImageFont

# 🔑 بياناتك الصحيحة
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def draw_grid_and_send(image_path):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        width, height = img.size
        # تقسيم 4x4
        rows, cols = 4, 4
        sw, sh = width // cols, height // rows
        
        counter = 1
        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * sw, r * sh
                x2, y2 = x1 + sw, y1 + sh
                # رسم المربع الأصفر
                draw.rectangle([x1, y1, x2, y2], outline="yellow", width=4)
                # كتابة الرقم في الزاوية
                draw.text((x1 + 15, y1 + 15), str(counter), fill="yellow")
                counter += 1
        
        grid_path = "grid_final.png"
        img.save(grid_path)
        with open(grid_path, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': "🔢 الشبكة جاهزة بالأبعاد المطلوبة:"}, files={'photo': f})

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # 📏 الأبعاد التي طلبت تثبيتها
    options.add_argument('--window-size=900,1800')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)

        # البحث عن الكابتشا والنقر
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            driver.switch_to.frame(frame)
            if "recaptcha" in driver.page_source:
                cb = driver.find_elements(By.ID, "recaptcha-anchor")
                if cb:
                    driver.execute_script("arguments[0].click();", cb[0])
                    driver.switch_to.default_content()
                    time.sleep(10)
                    break
            driver.switch_to.default_content()

        # التقاط الصورة ومعالجتها
        raw_path = "raw_screen.png"
        driver.save_screenshot(raw_path)
        draw_grid_and_send(raw_path)

    except Exception as e:
        send_msg(f"❌ خطأ: {str(e)}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
