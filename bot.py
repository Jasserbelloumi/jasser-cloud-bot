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

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"
API_KEY_2CAPTCHA = "efb4e119f4ffbfdad7696ad3dffa22f2" # تأكد من صحة المفتاح

def notify(msg, img=None):
    try:
        if img:
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': msg}, files={'photo': f})
        else:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def solve_captcha(site_key, url):
    print("🧩 جاري طلب حل الكابتشا...")
    s = requests.Session()
    res = s.get(f"http://2captcha.com/in.php?key={API_KEY_2CAPTCHA}&method=userrecaptcha&googlekey={site_key}&pageurl={url}").text
    if 'OK|' not in res: return None
    captcha_id = res.split('|')[1]
    for _ in range(20):
        time.sleep(5)
        res = s.get(f"http://2captcha.com/res.php?key={API_KEY_2CAPTCHA}&action=get&id={captcha_id}").text
        if 'OK|' in res: return res.split('|')[1]
    return None

def run_bot():
    notify("🛡️ جاري محاولة كسر حماية الموقع...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # تمويه إضافي لمنع اكتشاف الـ WebDriver
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        url = "https://www.like4like.org/register.php"
        driver.get(url)
        time.sleep(8)

        # التحقق من وجود كابتشا الحماية (reCAPTCHA)
        if "g-recaptcha" in driver.page_source or "captcha" in driver.page_source:
            notify("🧩 تم اكتشاف كابتشا حماية، جاري الحل...")
            site_key = "6Ldy_XMUAAAAAOB9b9_918X5S4S_4_6y_S_4_6y" # المستخرج من Like4Like
            token = solve_captcha(site_key, url)
            
            if token:
                driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{token}";')
                driver.execute_script("document.querySelector('form').submit();")
                time.sleep(10)
                notify("✅ تم تخطي حماية الكابتشا بنجاح!")
            else:
                notify("❌ فشل حل الكابتشا (رصيد غير كافٍ أو وقت طويل)")

        # الآن نحاول البحث عن حقول التسجيل
        if "username" in driver.page_source:
            notify("📝 دخلنا لصفحة التسجيل الحقيقية! جاري الإدخال...")
            # (نفس منطق ملء البيانات السابق...)
        else:
            driver.save_screenshot("after_bypass.png")
            notify("⚠️ لا زال هناك حاجز. انظر الصورة:", "after_bypass.png")

    except Exception as e:
        notify(f"🚨 خطأ: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
