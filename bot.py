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

# 🔑 بياناتك
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def get_updates(last_id):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id + 1}"
        res = requests.get(url, timeout=10).json()
        return res.get('result', [])
    except: return []

def draw_grid(input_path, output_path):
    with Image.open(input_path) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size
        rows, cols = 6, 6
        sw, sh = w // cols, h // rows
        for r in range(rows):
            for c in range(cols):
                x, y = c * sw, r * sh
                draw.rectangle([x, y, x + sw, y + sh], outline="yellow", width=2)
                draw.text((x + 5, y + 5), str((r * cols) + c + 1), fill="yellow")
        img.save(output_path)
        return sw, sh

def run_bot():
    send_msg("🚀 V44 متصل الآن.. جاري فتح الصفحة والتقاط الشبكة.")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=900,1800')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(12)
        
        # التقاط الشبكة الأولى
        driver.save_screenshot("raw.png")
        sw, sh = draw_grid("raw.png", "grid.png")
        with open("grid.png", 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "🎯 أرسل أرقام المربعات للضغط (مثال: 10,11)"}, files={'photo': f})

        last_update_id = 0
        while True:
            updates = get_updates(last_update_id)
            for update in updates:
                last_update_id = update['update_id']
                if 'message' in update and 'text' in update['message']:
                    cmd = update['message']['text']
                    send_msg(f"⏳ جاري تنفيذ النقرات: {cmd}")
                    
                    indices = cmd.replace(' ', '').split(',')
                    for idx in indices:
                        if idx.isdigit():
                            n = int(idx)
                            row, col = (n - 1) // 6, (n - 1) % 6
                            cx, cy = (col * sw) + (sw // 2), (row * sh) + (sh // 2)
                            # تنفيذ النقر عبر JS لضمان الدقة
                            driver.execute_script(f"document.elementFromPoint({cx}, {cy}).click();")
                    
                    time.sleep(3)
                    driver.save_screenshot("after.png")
                    with open("after.png", 'rb') as f:
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "✅ النتيجة بعد النقر"}, files={'photo': f})
            time.sleep(2)
            
    except Exception as e:
        send_msg(f"❌ خطأ: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
