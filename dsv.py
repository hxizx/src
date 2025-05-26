# All imports remain unchanged
import random
import string 
import requests
import os
import time
import json
from colorama import Fore, init
import datetime
from configparser import ConfigParser
import sys

init(autoreset=True)
__version__ = "Author: zenious.gg"
__github__= "https://discord.gg/zenious"

dir_path = os.path.dirname(os.path.realpath(__file__))
configur = ConfigParser()
configur.read(os.path.join(dir_path, f"config.ini"))
tokens_list = os.path.join(dir_path, f"tokens.txt")
proxies_file = os.path.join(dir_path, "proxies.txt")

proxy_enabled = configur.getboolean("proxy", "USE_PROXY", fallback=False)

def load_proxies(path):
    if not os.path.isfile(path): return []
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

proxy_list = load_proxies(proxies_file) if proxy_enabled else []

def get_random_proxy():
    if not proxy_list:
        return None
    raw = random.choice(proxy_list)
    parts = raw.strip().split(":")

    if len(parts) == 4:
        ip, port, user, pwd = parts
        proxy_url = f"http://{user}:{pwd}@{ip}:{port}"
    elif len(parts) == 2:
        ip, port = parts
        proxy_url = f"http://{ip}:{port}"
    else:
        print(f"{Fore.RED}[!] Invalid proxy format: {raw}")
        return None

    return {"http": proxy_url, "https": proxy_url}


integ_0 = 0
sys_url = "https://discord.com/api/v9/users/@me"
URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"

def s_sys_h():
    base = {
        "Content-Type": "application/json",
        "Origin": "https://discord.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    token = avail_tokens(tokens_list)[integ_0] if configur.getboolean("sys", "MULTI_TOKEN") else configur.get("sys", "TOKEN")
    base["Authorization"] = token
    return base


def sys_c_t():
    if configur.get("sys", "TOKEN") != "":
        pass
    elif configur.get("sys", "TOKEN") == "" and not configur.getboolean("sys", "MULTI_TOKEN"):
        print(f"{Lb}[!]{Fore.RED} No token found. You must paste your token inside the 'config.ini' file, in front of the value 'TOKEN'.")
        exit()
    elif configur.getboolean("sys", "MULTI_TOKEN") and not avail_tokens(tokens_list)[0]:
        print(f"{Lb}[!]{Fore.RED} No tokens found. You must paste your tokens inside the 'tokens.txt' file.")
        exit()
    elif configur.get("sys", "TOKEN") == "":
        print(f"{Lb}[!]{Fore.RED} Invalid config detected. Please re-check the config file, `config.ini` and your settings.")
        exit()

available_usernames = []
av_list = os.path.join(dir_path, f"available_usernames.txt")
sample_0 = r"_."

Lb = Fore.LIGHTBLACK_EX
Ly = Fore.LIGHTBLUE_EX
Delay = configur.getfloat("config", "default_delay")

def setconf():
    global string_0, digits_0, punctuation_0
    global sat_string, sat_digits, sat_multi_token, sat_punct
    sat_string = configur.getboolean("config", "string")
    sat_digits = configur.getboolean("config", "digits")
    sat_punct = configur.getboolean("config", "punctuation")
    sat_multi_token = configur.getboolean("sys", "MULTI_TOKEN")

    string_0 = string.ascii_lowercase if sat_string else ""
    digits_0 = string.digits if sat_digits else ""
    punctuation_0 = sample_0 if sat_punct else ""

    if not sat_string and not sat_digits and not sat_punct:
        punctuation_0 = sample_0
        digits_0 = string.digits
        string_0 = string.ascii_lowercase

def main():
    sys_c_t()
    os.system(f"title {__version__} - Connected as {requests.get(sys_url, headers=s_sys_h()).json()['username']}")
    s_sys_h()
    setconf()

    logo = []

    print(f"""{Fore.LIGHTBLUE_EX}
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
  {__version__} 
  {__github__}                     {Fore.LIGHTCYAN_EX}Connected as {requests.get(sys_url, headers=s_sys_h()).json()['username']}{Ly}#{Fore.LIGHTCYAN_EX}{requests.get(sys_url, headers=s_sys_h()).json()['discriminator']}{Ly}
""")

    for line in logo:
        print(Fore.LIGHTCYAN_EX + line)

    print(f"""{Fore.LIGHTBLUE_EX}
  [1] Generate and check usernames
  [2] Check list from 'usernames.txt'

  ─ Configuration ────────────────────────────────
  Digits: {sat_digits}
  String: {sat_string}
  Punctuation: {sat_punct}
  Multi-Token: {sat_multi_token}
  Delay: {Delay}s
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
""")
    proc0()

def setdelay():
    global Delay
    print(f"{Lb}[!]{Ly} Default delay is: {Delay}s (config.ini){Lb}")
    d_input = input(f"{Lb}[{Ly}Edit Delay (Press Enter to skip){Lb}]:> ")
    if d_input.strip() == "":
        return
    try:
        Delay = int(d_input)
    except ValueError:
        print(f"{Lb}[!]{Fore.RED}Error: You must enter a valid integer.")
        setdelay()

def proc0():
    m_input = input(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}Zenious.gg{Fore.LIGHTBLACK_EX}]:> {Fore.LIGHTBLUE_EX}").lower()
    if m_input == "exit":
        sys.exit(0)
    elif m_input == "2":
        setdelay()
        opt2load()
    elif m_input == "1":
        setdelay()
        opt1load()
    else:
        proc0()

def validate_names(opt, usernames):
    global available_usernames, integ_0
    if opt == 2:
        for username in usernames:
            check_username(username)
    elif opt == 1:
        check_username(usernames)

def check_username(username):
    global integ_0, proxy_list
    body = {"username": username}
    max_retries = len(proxy_list) if proxy_enabled and proxy_list else 1
    attempts = 0

    while attempts < max_retries:
        proxy = get_random_proxy()
        try:
            time.sleep(Delay)
            endpoint = requests.post(URL, headers=s_sys_h(), json=body, proxies=proxy, timeout=10)
            json_endpoint = endpoint.json()

            if endpoint.status_code == 429:
                print(f"{Lb}[!]{Fore.YELLOW} Rate limit hit.")
                proxy_removed = True

                if proxy and "http" in proxy:
                    failed = proxy["http"].replace("http://", "")
                    if failed in proxy_list:
                        proxy_list.remove(failed)
                        proxy_removed = True
                        print(f"{Lb}[x]{Fore.RED} Removed rate-limited proxy: {failed}")

                if sat_multi_token and len(avail_tokens(tokens_list)) > 1:
                    integ_0 = (integ_0 + 1) % len(avail_tokens(tokens_list))
                    user_info = requests.get(sys_url, headers=s_sys_h()).json()
                    print(f"{Lb}[!]{Ly} Switched token: {user_info['username']}#{user_info['discriminator']}")
                elif not proxy_removed:
                    sleep_time = json_endpoint.get("retry_after", 10)
                    print(f"{Lb}[!]{Fore.RED} Sleeping for {sleep_time}s")
                    time.sleep(sleep_time)

                attempts += 1
                continue

            if json_endpoint.get("taken") is not None:
                if json_endpoint["taken"] is False:
                    print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} '{username}' available.")
                    save(username)
                    available_usernames.append(username)
                else:
                    print(f"{Lb}[-]{Fore.RED} '{username}' taken.")
            else:
                print(f"{Lb}[?]{Fore.RED} Error validating '{username}': {json_endpoint.get('message')}")
            return
        except requests.RequestException as e:
            print(f"{Lb}[!]{Fore.YELLOW} Proxy failed: {e}")
            if proxy and "http" in proxy and proxy["http"].replace("http://", "") in proxy_list:
                failed = proxy["http"].replace("http://", "")
                proxy_list.remove(failed)
                print(f"{Lb}[x]{Fore.RED} Removed dead proxy: {failed}")
            attempts += 1

    print(f"{Lb}[x]{Fore.RED} All proxies failed for '{username}'. Skipping.")

def avail_tokens(path):
    with open(path, 'r') as at:
        tokens = at.read().splitlines()
    return tokens

def exit():
    input(f"{Fore.BLUE}Press Enter to exit.")
    sys.exit(0)

def checkavail():
    if len(available_usernames) < 1:
        print(f"{Lb}[!]{Fore.RED} Error: No available usernames found.")
        exit()
    return

def opt2load():
    list_path = os.path.join(dir_path, f"usernames.txt")
    print(f"{Lb}[!]{Ly}Checking 'usernames.txt'...")
    try:
        with open(list_path) as file:
            usernames = [line.strip() for line in file]
        validate_names(2, usernames)
        checkavail()
        print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} usernames saved in: '{av_list}'")
        exit()
    except FileNotFoundError:
        print(f"{Lb}[!]{Fore.RED} Error: usernames.txt not found in directory: {dir_path}")
        exit()

def opt1load():
    try:
        opt1_input = int(input(f"{Lb}[{Ly}How many letters in a username{Lb}]:> "))
        if not (2 <= opt1_input <= 32):
            print(f"{Lb}[!]{Fore.RED} Error: Username length must be 2–32.")
            return opt1load()
        opt2_input = int(input(f"{Lb}[{Ly}How many usernames to generate{Lb}]:> "))
        opt1func(opt2_input, opt1_input)
    except ValueError:
        print(f"{Lb}[!]{Fore.RED} Error: You must enter a valid integer.")
        opt1load()

def save(content: str):
    with open(av_list, "a") as file:
        file.write(f"\n{content}")

def opt1func(v1, v2):
    for i in range(v1):
        name = get_names(v2)
        validate_names(1, name)
        time.sleep(Delay)
    checkavail()
    print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} usernames saved in: '{av_list}'")
    exit()

def get_names(length: int) -> str:
    return ''.join(random.sample(string_0 + digits_0 + punctuation_0, length))

if __name__ == "__main__":
    main()
