import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw, ImageFont

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def draw_grid_on_image(image_path):
    # فتح الصورة ورسم الشبكة
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # تقسيم العرض والطول (شبكة 4x4 للكابتشا)
        rows, cols = 4, 4
        step_w = width // cols
        step_h = height // rows
        
        counter = 1
        for r in range(rows):
            for c in range(cols):
                # تحديد زوايا المربع
                x1, y1 = c * step_w, r * step_h
                x2, y2 = x1 + step_w, y1 + step_h
                
                # رسم المربع والرقم
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                draw.text((x1 + 10, y1 + 10), str(counter), fill="red")
                counter += 1
        img.save("grid_screenshot.png")

def send_grid_snap(driver, caption):
    driver.set_window_size(600, 1500)
    # نركز فقط على منطقة الكابتشا (تقريبياً)
    driver.save_screenshot("temp.png")
    
    # رسم الشبكة
    draw_grid_on_image("temp.png")
    
    with open("grid_screenshot.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                      data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})

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

        # الضغط على الكابتشا لإظهار الصور
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            driver.switch_to.frame(frame)
            if "recaptcha" in driver.page_source:
                checkbox = driver.find_elements(By.ID, "recaptcha-anchor")
                if checkbox:
                    driver.execute_script("arguments[0].click();", checkbox[0])
                    driver.switch_to.default_content()
                    time.sleep(8)
                    break
            driver.switch_to.default_content()

        # إرسال الصورة المرقمة
        send_grid_snap(driver, "🔢 اختر أرقام المربعات المطلوبة (مثلاً: 1, 5, 9)")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
