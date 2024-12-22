import time
import socket
import requests
import threading
from pathlib import Path
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from bugscanx.modules.utils.utils import get_input, clear_screen

DEFAULT_TIMEOUT = 5
EXCLUDE_LOCATIONS = ["https://jio.com/BalanceExhaust", "http://filter.ncell.com.np/nc"]
FILE_WRITE_LOCK = threading.Lock()

def get_hosts_from_file(file_path):
    try:
        return [line.strip() for line in Path(file_path).read_text().splitlines() if line.strip()]
    except Exception as e:
        print(Fore.RED + f"Error reading file: {e}")
        return []

def get_http_method():
    methods = ['GET', 'POST', 'PATCH', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'HEAD']
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\ud83c\udf10 Available HTTP methods: " + ", ".join(methods))
    method = get_input(Fore.CYAN + "\n » Select an HTTP method (default: HEAD): ", "HEAD").upper()
    return method if method in methods else "HEAD"

def file_manager(start_dir, max_up_levels=None, max_invalid_attempts=3):
    current_dir = Path(start_dir).resolve()
    levels_up = 0
    invalid_attempts = 0

    while True:
        files = [f for f in current_dir.iterdir() if f.is_file() and f.suffix == '.txt']
        directories = [d for d in current_dir.iterdir() if d.is_dir()]

        if not files and not directories:
            print(Fore.RED + "⚠ No .txt files or directories found.")
            return None

        print(Fore.CYAN + f"\n🗁 Contents of '{current_dir}':")
        items = directories + files
        for idx, item in enumerate(items, 1):
            prefix = "🗀 " if item.is_dir() else "📄 "
            color = Fore.YELLOW if item.is_dir() else Fore.WHITE
            print(f"{idx}. {prefix}{color}{item.name}{Style.RESET_ALL}")

        print(Fore.LIGHTBLUE_EX + "\n0. ↑ Move up a directory" + Style.RESET_ALL)

        selection = get_input(Fore.CYAN + "  ⮞  Enter the number or filename: ").strip()

        if selection == '0':
            if max_up_levels is not None and levels_up >= max_up_levels:
                print(Fore.RED + "⚠ Maximum directory level reached.")
            elif current_dir.parent == current_dir:
                print(Fore.RED + "⚠ Already at the root directory.")
            else:
                current_dir = current_dir.parent
                levels_up += 1
            continue

        try:
            index = int(selection) - 1
            if 0 <= index < len(items):
                selected_item = items[index]
                if selected_item.is_dir():
                    current_dir = selected_item
                    levels_up = 0
                else:
                    return selected_item
        except (ValueError, IndexError):
            file_path = current_dir / selection
            if file_path.is_file() and file_path.suffix == '.txt':
                return file_path

        print(Fore.RED + "⚠ Invalid selection. Please try again.")
        invalid_attempts += 1
        if invalid_attempts >= max_invalid_attempts:
            print(Fore.RED + "⚠ Too many invalid attempts. Exiting.")
            return None

def get_scan_inputs():
    selected_file = file_manager(Path('.'), max_up_levels=3)
    if not selected_file:
        print(Fore.RED + "⚠ No valid file selected.")
        return None, None, None, None, None

    hosts = get_hosts_from_file(selected_file)
    if not hosts:
        print(Fore.RED + "⚠ No valid hosts found in the file.")
        return None, None, None, None, None

    ports = get_input(Fore.CYAN + "  ⮞  Enter port list (default: 80): ", "80").strip().split(',')
    output_file = get_input(Fore.CYAN + "  ⮞  Enter output file name: ", f"results_{selected_file.name}").strip()
    threads = int(get_input(Fore.CYAN + "  ⮞  Enter number of threads (default: 50): ", "50") or 50)
    http_method = get_http_method()
    return hosts, ports, output_file, threads, http_method

def format_row(code, server, port, ip_address, host, use_colors=True):
    color = lambda text, clr: f"{clr}{text}{Style.RESET_ALL}" if use_colors else text
    return (
        f"{color(code, Fore.GREEN):<4} "
        f"{color(server, Fore.CYAN):<20} "
        f"{color(port, Fore.YELLOW):<5} "
        f"{color(ip_address, Fore.MAGENTA):<15} "
        f"{color(host, Fore.LIGHTBLUE_EX)}"
    )

def check_http_response(host, port, method):
    url = f"{'https' if port in ['443', '8443'] else 'http'}://{host}:{port}"
    try:
        response = requests.request(method, url, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
        if any(exclude in response.headers.get('Location', '') for exclude in EXCLUDE_LOCATIONS):
            return None
        return (
            response.status_code,
            response.headers.get('Server', 'N/A'),
            port,
            socket.gethostbyname(host) if host else 'N/A',
            host
        )
    except (requests.RequestException, socket.gaierror):
        return None

def format_time(elapsed_time):
    minutes, seconds = divmod(elapsed_time, 60)
    return f"{int(minutes)}m {int(seconds)}s" if minutes else f"{seconds:.2f}s"

def perform_scan(hosts, ports, output_file, threads, method):
    clear_screen()
    print(Fore.LIGHTGREEN_EX + f"\ud83d\udd0d Scanning using HTTP method: {method}...\n")

    headers = (
        f"{Fore.GREEN}Code  {Fore.CYAN}Server               "
        f"{Fore.YELLOW}Port   {Fore.MAGENTA}IP Address     {Fore.LIGHTBLUE_EX}Host{Style.RESET_ALL}"
    )
    separator = "-" * 65

    Path(output_file).write_text(f"{headers}\n{separator}\n")

    print(headers, separator, sep='\n')

    start_time = time.time()
    total_tasks = len(hosts) * len(ports)
    scanned, responded = 0, 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_http_response, host, port, method): (host, port) for host in hosts for port in ports}
        for future in as_completed(futures):
            scanned += 1
            result = future.result()
            if result:
                responded += 1
                row = format_row(*result)
                print(row)
                with FILE_WRITE_LOCK:
                    with open(output_file, 'a') as file:
                        file.write(format_row(*result, use_colors=False) + "\n")

            elapsed = time.time() - start_time
            print(f"Scanned {scanned}/{total_tasks} - Responded: {responded} - Elapsed: {format_time(elapsed)}", end='\r')

    print(f"\n\n{Fore.GREEN} Scan completed! {responded}/{scanned} hosts responded.")
    print(f"Results saved to {output_file}.{Style.RESET_ALL}")
