import os
import sys
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bugscanx.modules.handler import run_host_checker, run_sub_scan, run_ip_scan, run_sub_finder, run_ip_lookup, run_txt_toolkit, run_open_port, run_dns_info, run_osint, run_help_menu

def install_requirements():
    required_packages = {
        'requests': 'requests',
        'colorama': 'colorama',
        'ipaddress': 'ipaddress',
        'pyfiglet': 'pyfiglet',
        'ssl': 'ssl',
        'beautifulsoup4': 'bs4',
        'dnspython': 'dns',
        'multithreading': 'multithreading',
        'loguru': 'loguru'
    }
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"\033[33m Package '{package}' is not installed. Installing...\033[0m")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"\033[32m Package '{package}' installed successfully.\033[0m")

install_requirements()

import pyfiglet
from colorama import Fore, Style, init
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, default=None):
    full_prompt = f"{prompt} [{default}] " if default else f"{prompt} "
    response = input(full_prompt + Style.BRIGHT).strip()
    print(Style.RESET_ALL, end="")
    if response:
        return response
    else:
        return default if default is not None else ""

def text_to_ascii_banner(text, font="doom", color=Fore.WHITE, shift=5, version=""):
    try:
        ascii_banner = pyfiglet.figlet_format(text, font=font)
        shifted_banner = "\n".join((" " * shift) + line for line in ascii_banner.splitlines())
        version_text = f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}{version}"
        return f"{version_text}\n{color}{shifted_banner}{Style.RESET_ALL}"
    except pyfiglet.FontNotFound:
        pass

def banner():
    clear_screen()
    print(text_to_ascii_banner("BugScanX ", font="doom", color=Style.BRIGHT + Fore.MAGENTA, version=1.3))
    print(Fore.MAGENTA + "   Owner: " + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Ayan Rajpoot ™")
    print(Fore.BLUE + "   Support: " + Style.BRIGHT + Fore.LIGHTBLUE_EX + "https://t.me/BugScanX")
    print(Fore.WHITE + Style.DIM +"\n This is a test version. Report bugs on Telegram for quick fixes")
    print(Style.RESET_ALL)

def main_menu():
    while True:
        banner()
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Please select an option:"+ Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n [1] ⚡  Host Scanner(pro mode)")
        print(Fore.LIGHTYELLOW_EX + " [2] 🌐  Subdomains Scanner ")
        print(Fore.LIGHTYELLOW_EX + " [3] 📡  CIDR Scanner")
        print(Fore.LIGHTYELLOW_EX + " [4] 🔍  Subdomains Finder")
        print(Fore.LIGHTYELLOW_EX + " [5] 🔎  IP to domains")
        print(Fore.LIGHTYELLOW_EX + " [6] ✂️   TXT Toolkit")
        print(Fore.LIGHTYELLOW_EX + " [7] 🔓  Open Port Checker")
        print(Fore.LIGHTYELLOW_EX + " [8] 📜  DNS Records")
        print(Fore.LIGHTYELLOW_EX + " [9] 💡  OSINT ")
        print(Fore.LIGHTYELLOW_EX + " [10]❓  Help")
        print(Fore.LIGHTRED_EX + Style.BRIGHT + " [11]⛔  Exit\n" + Style.RESET_ALL)

        choice = get_input(Fore.CYAN + " ⮞  Enter your choice (1-11): ").strip()

        if choice == '1':
            clear_screen()
            print(text_to_ascii_banner("HOST Scanner", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_host_checker()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "2":
            clear_screen()
            print(text_to_ascii_banner("Sub Scanner", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_sub_scan()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "3":
            clear_screen()
            print(text_to_ascii_banner("CIDR Scanner  ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_ip_scan()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "4":
            clear_screen()
            print(text_to_ascii_banner("Subfinder ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_sub_finder()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "5":
            clear_screen()
            print(text_to_ascii_banner("IP LookUP ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_ip_lookup()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice =="6":
            clear_screen()
            print(text_to_ascii_banner("TxT Toolkit ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_txt_toolkit()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "7":
            clear_screen()
            print(text_to_ascii_banner("Open Port ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_open_port()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "8":
            clear_screen()
            print(text_to_ascii_banner("DNS Records ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_dns_info()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "9":
            clear_screen()
            print(text_to_ascii_banner("OSINT ", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_osint()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "10":
            clear_screen()
            print(text_to_ascii_banner("Help Menu", font="doom", color=Style.BRIGHT+Fore.MAGENTA))
            run_help_menu()
            input(Fore.YELLOW + "\n Press Enter to return to the main menu...")

        elif choice == "11":
            print(Fore.RED + Style.BRIGHT + "\n Shutting down the toolkit. See you next time!")
            sys.exit()

        else:
            print(Fore.RED + Style.BRIGHT + "\n Invalid choice. Please select a valid option.")
            input(Fore.YELLOW + Style.BRIGHT + "\n Press Enter to return to the main menu...")
            main_menu() 

if __name__ == "__main__":
    main_menu()
