import time
import os
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw

# 🔑 بياناتك الخاصة
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text}, timeout=10)
    except: pass

def send_photo(photo_path, caption):
    try:
        with open(photo_path, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f}, timeout=30)
    except Exception as e:
        send_msg(f"❌ فشل إرسال الصورة: {str(e)}")

def draw_grid(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            draw = ImageDraw.Draw(img)
            w, h = img.size
            rows, cols = 4, 4
            sw, sh = w // cols, h // rows
            for r in range(rows):
                for c in range(cols):
                    x, y = c * sw, r * sh
                    # رسم المربعات الصفراء
                    draw.rectangle([x, y, x + sw, y + sh], outline="yellow", width=4)
                    # رسم الأرقام
                    draw.text((x + 10, y + 10), str((r * cols) + c + 1), fill="yellow")
            img.save(output_path)
            return True
    except Exception as e:
        send_msg(f"⚠️ خطأ في الرسم: {str(e)}")
        return False

def run_bot():
    send_msg("🚀 بدأت المحاولة V39... جاري تحضير المتصفح بالأبعاد المطلوبة.")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=900,1800') # الأبعاد التي طلبتها
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.like4like.org/register.php")
        time.sleep(12)
        
        # البحث عن الكابتشا وتفعيلها
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        found_captcha = False
        for frame in iframes:
            try:
                driver.switch_to.frame(frame)
                if "recaptcha" in driver.page_source:
                    anchor = driver.find_elements(By.ID, "recaptcha-anchor")
                    if anchor:
                        driver.execute_script("arguments[0].click();", anchor[0])
                        found_captcha = True
                        driver.switch_to.default_content()
                        send_msg("🖱️ تم الضغط على المربع.. انتظار 10 ثوانٍ للصور.")
                        time.sleep(10)
                        break
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()

        # التقاط ومعالجة الصورة
        raw_img = "raw.png"
        final_img = "grid_result.png"
        driver.save_screenshot(raw_img)
        
        if draw_grid(raw_img, final_img):
            send_photo(final_img, "🔢 الشبكة الصفراء جاهزة بالأبعاد المطلوبة!")
        else:
            send_photo(raw_img, "📸 أرسلت الصورة بدون شبكة بسبب خطأ في الرسم.")

    except Exception as e:
        send_msg(f"❌ خطأ تقني: {str(e)}")
    finally:
        if driver: driver.quit()
        send_msg("🏁 انتهت الجلسة.")

if __name__ == "__main__":
    run_bot()
