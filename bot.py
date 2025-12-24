import time
import os
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
try:
    from PIL import Image, ImageDraw
except ImportError:
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def draw_grid_and_send(driver):
    try:
        driver.save_screenshot("raw.png")
        with Image.open("raw.png") as img:
            draw = ImageDraw.Draw(img)
            w, h = img.size
            rows, cols = 4, 4
            sw, sh = w // cols, h // rows
            for r in range(rows):
                for c in range(cols):
                    x, y = c * sw, r * sh
                    draw.rectangle([x, y, x+sw, y+sh], outline="red", width=3)
                    draw.text((x+10, y+10), str((r*cols)+c+1), fill="red")
            img.save("grid.png")
        
        with open("grid.png", 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': "🔢 اختر المربعات:"}, files={'photo': f})
    except Exception as e:
        send_msg(f"⚠️ فشل رسم الشبكة لكن سأرسل الصورة عادية: {str(e)}")
        with open("raw.png", 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID}, files={'photo': f})

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=500,1500')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        send_msg("🚀 بدأت المحاولة الآن... انتظر 20 ثانية.")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.like4like.org/register.php")
        time.sleep(12)

        # محاولة النقر
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            driver.switch_to.frame(frame)
            if "recaptcha" in driver.page_source:
                cb = driver.find_elements(By.ID, "recaptcha-anchor")
                if cb:
                    driver.execute_script("arguments[0].click();", cb[0])
                    driver.switch_to.default_content()
                    time.sleep(8)
                    break
            driver.switch_to.default_content()

        draw_grid_and_send(driver)

    except Exception as e:
        send_msg(f"❌ خطأ في السكربت:\n{traceback.format_exc()}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_bot()
