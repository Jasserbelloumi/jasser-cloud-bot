import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# بياناتك
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

def notify_and_wait(msg, img=None):
    """إرسال إشعار وانتظار رد من المستخدم عبر تليجرام"""
    try:
        if img:
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                              data={'chat_id': CHAT_ID, 'caption': msg}, files={'photo': f})
        else:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={'chat_id': CHAT_ID, 'text': msg})
        
        print("⏳ بانتظار ردك على تليجرام للمتابعة...")
        # الحصول على آخر رسالة قبل بدء الانتظار لتجنب الردود القديمة
        last_update_id = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()['result'][-1]['update_id'] if requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()['result'] else 0
        
        while True:
            time.sleep(5)
            updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_update_id + 1}).json()
            for update in updates.get('result', []):
                if str(update['message']['chat']['id']) == CHAT_ID:
                    return update['message'].get('text', 'done')
    except Exception as e:
        print(f"Error in TG communication: {e}")
        return "error"

def run_bot():
    print("🚀 تشغيل البوت بنظام التحكم عن بعد...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1200,800')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.like4like.org/register.php")
        time.sleep(10)

        # التحقق من وجود صفحة 404 أو الكابتشا التي أرسلت صورتها
        if "reCAPTCHA" in driver.page_source or "g-recaptcha" in driver.page_source or "Error 404" in driver.page_source:
            driver.save_screenshot("problem.png")
            notify_and_wait("⚠️ واجهت صفحة الحماية/404. يرجى حل الكابتشا إذا ظهرت أو كتابة أي شيء للمتابعة بعد أن أغير لك الإعدادات:", "problem.png")
        
        # ملء البيانات (محاولة عمياء بعد ردك)
        user = f"jsr{random.randint(1000, 9999)}"
        pwd = "Jasser@User2025"
        email = f"{user}@1secmail.com"

        try:
            wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(user)
            driver.find_element(By.ID, "password").send_keys(pwd)
            driver.find_element(By.ID, "password_re").send_keys(pwd)
            driver.find_element(By.ID, "email").send_keys(email)
            driver.find_element(By.ID, "email_re").send_keys(email)
            driver.execute_script("document.getElementById('agree').click();")
            
            driver.save_screenshot("filling.png")
            notify_and_wait(f"📝 ملأت البيانات:\n👤 {user}\n📧 {email}\nهل أضغط تسجيل؟ (ارسل أي رسالة للضغط)", "filling.png")
            
            driver.execute_script("document.getElementsByName('submit')[0].click();")
            time.sleep(10)
            
            driver.save_screenshot("final_result.png")
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': "🏁 تمت العملية، تفقد الصورة النهائية."})
            with open("final_result.png", 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})

        except Exception as e:
            driver.save_screenshot("error.png")
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': f"❌ فشل الإدخال: {str(e)[:100]}"}, files={'photo': open("error.png", 'rb')})

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
