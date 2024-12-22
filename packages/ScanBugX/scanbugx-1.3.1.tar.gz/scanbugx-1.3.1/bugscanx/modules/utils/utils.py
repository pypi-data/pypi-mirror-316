import os
from colorama import Style

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