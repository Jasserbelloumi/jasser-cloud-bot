import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# إعداداتك
API_KEY_2CAPTCHA = "efb4e119f4ffbfdad7696ad3dffa22f2"
SITE_KEY = "6Ldy_XMUAAAAAOB9b9_918X5S4S_4_6y_S_4_6y"

def run_bot():
    print("🚀 بدء عملية التسجيل السحابية...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # بيانات عشوائية
        user = f"jsr_{random.randint(10000, 99999)}"
        pwd = "Jasser@User2025"
        email = f"{user}@1secmail.com"

        print(f"📝 إنشاء حساب: {user}")
        driver.get("https://www.like4like.org/register/")
        time.sleep(3)

        # ملء الحقول
        driver.find_element(By.ID, "username").send_keys(user)
        driver.find_element(By.ID, "password").send_keys(pwd)
        driver.find_element(By.ID, "password_re").send_keys(pwd)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "email_re").send_keys(email)
        driver.find_element(By.ID, "agree").click()

        print("🧩 طلب حل الكابتشا من 2Captcha...")
        # إرسال طلب الكابتشا
        captcha_id = requests.post(
            "https://api.2captcha.com/createTask",
            json={
                "clientKey": API_KEY_2CAPTCHA,
                "task": {
                    "type": "NoCaptchaTaskProxyless",
                    "websiteURL": "https://www.like4like.org/register/",
                    "websiteKey": SITE_KEY
                }
            }
        ).json().get("taskId")

        if captcha_id:
            # انتظار الحل
            for _ in range(20):
                time.sleep(5)
                res = requests.post(
                    "https://api.2captcha.com/getTaskResult",
                    json={"clientKey": API_KEY_2CAPTCHA, "taskId": captcha_id}
                ).json()
                if res.get("status") == "ready":
                    token = res.get("solution").get("gRecaptchaResponse")
                    # وضع التوكن في الصفحة
                    driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{token}";')
                    print("✅ تم حل الكابتشا ووضع التوكن.")
                    driver.find_element(By.NAME, "register").click()
                    time.sleep(5)
                    print(f"🎉 تم إنهاء المحاولة للحساب: {user}")
                    break
                print("⏳ جاري الحل...")
        else:
            print("❌ فشل إنشاء مهمة الكابتشا (تأكد من الرصيد).")

    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    run_bot()
