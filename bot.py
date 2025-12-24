import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def draw_precise_grid(input_path, output_path):
    with Image.open(input_path) as img:
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # تقسيم الكابتشا لـ 4 أعمدة و 4 صفوف (مربعات أصغر وأدق)
        cols, rows = 4, 4
        step_w, step_h = width // cols, height // rows
        
        counter = 1
        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * step_w, r * step_h
                x2, y2 = x1 + step_w, y1 + step_h
                
                # رسم المربع باللون الأصفر (أوضح) مع رقم صغير في الزاوية
                draw.rectangle([x1, y1, x2, y2], outline="yellow", width=2)
                draw.text((x1 + 5, y1 + 5), str(counter), fill="yellow")
                counter += 1
        img.save(output_path)

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # زيادة العرض والطول لضمان عدم قطع الكابتشا
    options.add_argument('--window-size=800,2000') 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(12)
        
        # محاولة النقر على الكابتشا
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            driver.switch_to.frame(frame)
            if "recaptcha" in driver.page_source:
                anchor = driver.find_elements(By.ID, "recaptcha-anchor")
                if anchor:
                    driver.execute_script("arguments[0].click();")
                    driver.switch_to.default_content()
                    time.sleep(8) # انتظار الصور
                    break
            driver.switch_to.default_content()

        # تصوير وإرسال الشبكة
        driver.save_screenshot("raw.png")
        draw_precise_grid("raw.png", "grid_view.png")
        
        with open("grid_view.png", 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': "🔢 انظر للأرقام الصفراء وأخبرني أين توجد الصور المطلوبة:"}, files={'photo': f})

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
