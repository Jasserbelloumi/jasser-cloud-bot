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

def get_last_command():
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        res = requests.get(url).json()
        if res['result']:
            return res['result'][-1]['message']['text'], res['result'][-1]['update_id']
    except: pass
    return None, None

def draw_grid(input_path, output_path):
    with Image.open(input_path) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size
        rows, cols = 6, 6  # شبكة 36 مربعاً كما طلبنا
        sw, sh = w // cols, h // rows
        for r in range(rows):
            for c in range(cols):
                x, y = c * sw, r * sh
                draw.rectangle([x, y, x + sw, y + sh], outline="yellow", width=2)
                draw.text((x + 5, y + 5), str((r * cols) + c + 1), fill="yellow")
        img.save(output_path)
        return sw, sh # نحتاج حجم المربع لحساب إحداثيات النقر

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=900,1800')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)
        
        # 1. تفعيل الكابتشا والتقاط الصورة المرقمة
        driver.save_screenshot("raw.png")
        sw, sh = draw_grid("raw.png", "grid.png")
        with open("grid.png", 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
        
        send_msg("🎯 أرسل أرقام المربعات مفصولة بفاصلة (مثال: 14,15,20)")

        # 2. حلقة الاستماع للأوامر والضغط
        last_id = 0
        while True:
            text, up_id = get_last_command()
            if text and up_id > last_id:
                last_id = up_id
                if text.lower() == 'done': break
                
                nums = text.split(',')
                for n in nums:
                    try:
                        n = int(n.strip())
                        # حساب موقع النقر بناءً على رقم المربع (1-36)
                        row = (n - 1) // 6
                        col = (n - 1) % 6
                        click_x = (col * sw) + (sw // 2)
                        click_y = (row * sh) + (sh // 2)
                        
                        # تنفيذ النقرة باستخدام JavaScript
                        driver.execute_script(f"document.elementFromPoint({click_x}, {click_y}).click();")
                        send_msg(f"✅ تم النقر على المربع {n}")
                    except: pass
                
                time.sleep(2)
                driver.save_screenshot("result.png")
                with open("result.png", 'rb') as f:
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "الصورة بعد النقر"}, files={'photo': f})
            
            time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
