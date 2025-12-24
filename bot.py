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

# 🔑 البيانات الخاصة بك
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=900,1800')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        send_msg("🚦 بدأت العملية: جاري تشغيل المتصفح...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        send_msg("🌐 جاري الدخول إلى صفحة التسجيل...")
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)
        
        send_msg("🔎 البحث عن مربع الكابتشا للنقر عليه...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        found = False
        for frame in iframes:
            try:
                driver.switch_to.frame(frame)
                checkbox = driver.find_elements(By.ID, "recaptcha-anchor")
                if checkbox:
                    driver.execute_script("arguments[0].click();", checkbox[0])
                    found = True
                    driver.switch_to.default_content()
                    break
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()

        if found:
            send_msg("✅ تم النقر! انتظر 10 ثوانٍ لظهور الصور...")
            time.sleep(10)
        else:
            send_msg("⚠️ لم أجد المربع، سأصور الصفحة على أي حال.")

        # التقاط الصورة ورسم الشبكة
        path = "final_step.png"
        driver.save_screenshot(path)
        
        # رسم الشبكة الصفراء بالأرقام
        with Image.open(path) as img:
            draw = ImageDraw.Draw(img)
            w, h = img.size
            # رسم 16 مربعاً (4*4)
            sw, sh = w // 4, h // 4
            for r in range(4):
                for c in range(4):
                    x, y = c * sw, r * sh
                    draw.rectangle([x, y, x+sw, y+sh], outline="yellow", width=3)
                    draw.text((x+10, y+10), str((r*4)+c+1), fill="yellow")
            img.save("grid_final.png")

        with open("grid_final.png", 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': "🔢 الشبكة المرقمة جاهزة!"}, files={'photo': f})
            
    except Exception as e:
        send_msg(f"❌ حدث خطأ فني:\n{traceback.format_exc()}")
    finally:
        if driver:
            driver.quit()
            send_msg("🏁 انتهت المحاولة وإغلاق المتصفح.")

if __name__ == "__main__":
    run_bot()
