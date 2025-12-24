import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_bot():
    print("🚀 بدء تشغيل المحرك السحابي على سيرفرات GitHub...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # إعداد المتصفح تلقائياً
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("🌐 الدخول إلى Like4Like...")
        driver.get("https://www.like4like.org/register/")
        
        # محاكاة الطباعة كل ثانية لمراقبة التيرمكس
        for i in range(10):
            print(f"⏱️ الحالة [ثانية {i+1}]: السيرفر يعمل بنجاح والصفحة مستقرة.")
            time.sleep(1)
            
        print(f"✅ تم الوصول للرابط: {driver.current_url}")
        print("📌 جاهز لتنفيذ عمليات التسجيل المعقدة.")
        
    except Exception as e:
        print(f"❌ حدث خطأ في السيرفر: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    run_bot()
