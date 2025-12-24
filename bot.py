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

def draw_grid_on_captcha(image_path):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size
        # رسم شبكة 4x4 (16 مربعاً)
        cols, rows = 4, 4
        sw, sh = w // cols, h // rows
        
        counter = 1
        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * sw, r * sh
                x2, y2 = x1 + sw, y1 + sh
                draw.rectangle([x1, y1, x2, y2], outline="yellow", width=3)
                # وضع الرقم في المنتصف ليكون واضحاً
                draw.text((x1 + sw//2 - 5, y1 + sh//2 - 5), str(counter), fill="yellow")
                counter += 1
        img.save("grid_final.png")

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1000,2000') # حجم كبير لضمان الرؤية
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)
        
        # البحث عن إطار الكابتشا والضغط عليه
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        captcha_frame = None
        for frame in iframes:
            if "recaptcha" in frame.get_attribute("src"):
                captcha_frame = frame
                break
        
        if captcha_frame:
            # النقر على المربع أولاً
            driver.switch_to.frame(captcha_frame)
            driver.execute_script("document.getElementById('recaptcha-anchor').click();")
            driver.switch_to.default_content()
            time.sleep(8)
            
            # التقاط صورة مركزة لمنطقة الكابتشا فقط
            driver.save_screenshot("raw_page.png")
            # رسم الشبكة على الصورة الناتجة
            draw_grid_on_captcha("raw_page.png")
            
            with open("grid_final.png", 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                              data={'chat_id': CHAT_ID, 'caption': "🔢 الأرقام الصفراء جاهزة. اختر المربعات المطلوبة:"}, files={'photo': f})
        else:
            send_msg("❌ لم يتم العثور على إطار الكابتشا.")

    except Exception as e:
        send_msg(f"⚠️ حدث خطأ: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
