import time
import random
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# بياناتك
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})

def send_snap(driver, caption="📸"):
    path = "live.png"
    driver.save_screenshot(path)
    with open(path, 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        send_msg("🚀 البوت متصل الآن! أرسل /url [الرابط] للبدء.")
        
        last_update_id = 0
        # محاولة تنظيف الرسائل القديمة
        try:
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
            if r['result']: last_update_id = r['result'][-1]['update_id']
        except: pass

        while True:
            try:
                updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_update_id + 1, 'timeout': 20}).json()
                for update in updates.get('result', []):
                    last_update_id = update['update_id']
                    if 'message' not in update or 'text' not in update['message']: continue
                    
                    msg = update['message']['text']
                    
                    if msg == "/snap":
                        send_snap(driver, "لقطة حية بطلبك")
                    elif msg.startswith("/url "):
                        target = msg.split(" ")[1]
                        driver.get(target)
                        time.sleep(5)
                        send_snap(driver, f"فتحت الرابط: {target}")
                    elif msg.startswith("/code "):
                        exec_code = msg.replace("/code ", "")
                        try:
                            # تنفيذ كود بايثون مباشرة على المتصفح
                            exec(exec_code)
                            send_msg("✅ نُفذ الكود بنجاح")
                        except Exception as e:
                            send_msg(f"❌ خطأ في الكود: {str(e)}")
                    elif msg == "/help":
                        send_msg("الأوامر:\n/url [رابط]\n/snap\n/code [بايثون]")
                
            except Exception as e:
                print(f"Loop error: {e}")
            time.sleep(2)
            
    except Exception as e:
        send_msg(f"🚨 فشل بدء المتصفح: {str(e)}")

if __name__ == "__main__":
    run_bot()
