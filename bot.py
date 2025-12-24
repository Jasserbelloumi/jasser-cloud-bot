import time
import os
import requests
import traceback
import sys

# محاولة تثبيت المكتبات الناقصة تلقائياً
try:
    from PIL import Image, ImageDraw
except ImportError:
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image, ImageDraw

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
            # الأبعاد التي طلبتها 900x1800 مقسمة لـ 16 مربعاً
            sw, sh = w // 4, h // 4
            for r in range(4):
                for c in range(4):
                    x, y = c * sw, r * sh
                    draw.rectangle([x, y, x + sw, y + sh], outline="yellow", width=5)
                    draw.text((x + 20, y + 20), str((r * 4) + c + 1), fill="yellow")
            img.save(output_path)
            return True
    except Exception as e:
        send_msg(f"⚠️ خطأ في معالجة الصورة: {str(e)}")
        return False

def run_bot():
    send_msg("🎬 محاولة V40: جاري التشغيل بالأبعاد الثابتة...")
    
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=900,1800')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)
        
        # تفعيل الكابتشا
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            try:
                driver.switch_to.frame(frame)
                anchor = driver.find_elements(By.ID, "recaptcha-anchor")
                if anchor:
                    driver.execute_script("arguments[0].click();", anchor[0])
                    driver.switch_to.default_content()
                    send_msg("🖱️ تم الضغط.. جاري الانتظار لالتقاط الصورة.")
                    time.sleep(12)
                    break
                driver.switch_to.default_content()
            except: driver.switch_to.default_content()

        # التقاط الصورة ومعالجتها
        driver.save_screenshot("raw.png")
        if draw_grid("raw.png", "grid.png"):
            send_photo("grid.png", "🔢 الشبكة الصفراء جاهزة بالأبعاد المطلوبة!")
        else:
            send_photo("raw.png", "📸 الصورة الأصلية (فشل الرسم)")

    except Exception as e:
        send_msg(f"❌ خطأ تقني حرج: {str(e)}")
    finally:
        if driver: driver.quit()
        send_msg("🔚 انتهت العملية.")

if __name__ == "__main__":
    run_bot()
