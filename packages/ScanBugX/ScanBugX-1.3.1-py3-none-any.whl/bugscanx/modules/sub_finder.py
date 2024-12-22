import re
import random
import requests
import threading
from bs4 import BeautifulSoup
from colorama import Fore, init
from datetime import datetime, timedelta
from bugscanx.modules.utils.utils import get_input
from concurrent.futures import ThreadPoolExecutor, as_completed
from bugscanx.modules.utils.http_utils import HEADERS, USER_AGENTS
file_write_lock = threading.Lock()
init(autoreset=True)

session = requests.Session()
DEFAULT_TIMEOUT2 = 10


def get_random_headers():
    headers = HEADERS.copy()
    headers["user-agent"] = random.choice(USER_AGENTS)
    return headers

def fetch_subdomains(source_func, domain):
    try:
        subdomains = source_func(domain)
        return set(sub for sub in subdomains if isinstance(sub, str))
    except Exception as e:
        return set()

def crtsh_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://crt.sh/?q=%25.{domain}&output=json", headers=get_random_headers(), timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200 and response.headers.get('Content-Type') == 'application/json':
        for entry in response.json():
            subdomains.update(entry['name_value'].splitlines())
    return subdomains

def hackertarget_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", headers=get_random_headers(), timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200 and 'text' in response.headers.get('Content-Type', ''):
        subdomains.update([line.split(",")[0] for line in response.text.splitlines()])
    return subdomains

def rapiddns_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://rapiddns.io/subdomain/{domain}?full=1", headers=get_random_headers(), timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('td'):
            text = link.get_text(strip=True)
            if text.endswith(f".{domain}"):
                subdomains.add(text)
    return subdomains

def anubisdb_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://jldc.me/anubis/subdomains/{domain}", headers=get_random_headers(), timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200:
        subdomains.update(response.json())
    return subdomains

def alienvault_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", headers=get_random_headers(), timeout=DEFAULT_TIMEOUT2)
    if response.status_code == 200:
        for entry in response.json().get("passive_dns", []):
            subdomains.add(entry.get("hostname"))
    return subdomains

def urlscan_subdomains(domain):
    subdomains = set()
    url = f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
    
    try:
        response = session.get(url, headers=get_random_headers(), timeout=DEFAULT_TIMEOUT2)
        if response.status_code == 200:
            data = response.json()
            for result in data.get('results', []):
                page_url = result.get('page', {}).get('domain')
                if page_url and page_url.endswith(f".{domain}"):
                    subdomains.add(page_url)
    except requests.RequestException:
        pass
    return subdomains

recently_seen_subdomains = set()

def c99_subdomains(domain, days=10):
    base_url = "https://subdomainfinder.c99.nl/scans"
    subdomains = set()

    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    urls = [f"{base_url}/{date}/{domain}" for date in dates]

    def fetch_url(url):
        try:
            response = session.get(url, timeout=DEFAULT_TIMEOUT2)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    text = link.get_text(strip=True)
                    if text.endswith(f".{domain}") and text not in recently_seen_subdomains:
                        subdomains.add(text)
                        recently_seen_subdomains.add(text)
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            future.result()

    return subdomains

def is_valid_domain(domain):
    regex = re.compile(
        r'^(?:[a-zA-Z0-9]'  # First character of the domain
        r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)'  # Sub domain + hostname
        r'+[a-zA-Z]{2,6}$'  # Top level domain
    )
    return re.match(regex, domain) is not None

def process_domain(domain, output_file, sources):
    if not is_valid_domain(domain):
        print(Fore.RED + f"\n⚠️ Invalid domain: {domain}")
        return

    print(Fore.CYAN + f"🔍 Enumerating {domain}\n")
    
    subdomains = set()
    total_sources = len(sources)
    progress_counter = 0

    def fetch_and_update(source, domain):
        nonlocal progress_counter
        result = fetch_subdomains(source, domain)
        subdomains.update(result)

    with ThreadPoolExecutor(max_workers=min(total_sources, 10)) as source_executor:
        futures = {source_executor.submit(fetch_and_update, source, domain): source for source in sources}
        for future in as_completed(futures):
            future.result()

    print(Fore.GREEN + f"\n ✔ Completed {domain} - {len(subdomains)} subdomains found")
    
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"\n# Subdomains for {domain}\n")
        for subdomain in sorted(subdomains):
            if is_valid_domain(subdomain):
                file.write(f"{subdomain}\n")

def find_subdomains():
    input_choice = get_input(Fore.CYAN + " \n ⮞  Enter '1' for single domain or '2' for multiple from txt file: ").strip()
    
    if input_choice == '1':
        domain = get_input(Fore.CYAN + "\n ⮞  Enter the domain to find subdomains for: ").strip()
        if not domain:
            print(Fore.RED + "\n⚠️ Domain cannot be empty.")
            return
        domains_to_process = [domain]
        sources = [
            crtsh_subdomains, hackertarget_subdomains, rapiddns_subdomains,
            anubisdb_subdomains, alienvault_subdomains,
            urlscan_subdomains, c99_subdomains
        ]
        default_filename = f"{domain}_subdomains.txt"
        
    elif input_choice == '2':
        file_path = get_input(Fore.CYAN + "\n ⮞  Enter the path to the file containing domains: ").strip()
        try:
            with open(file_path, 'r') as file:
                domains_to_process = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + "\n⚠️ File not found. Please check the path.")
            return

        sources = [
            crtsh_subdomains, hackertarget_subdomains, rapiddns_subdomains,
            anubisdb_subdomains, alienvault_subdomains,
            urlscan_subdomains
        ]

        default_filename = f"{file_path.split('/')[-1].split('.')[0]}_subdomains.txt"
    
    else:
        print(Fore.RED + "\n⚠️ Invalid choice.")
        return

    output_file = get_input(Fore.CYAN + "\n ⮞ Enter the output file name (without extension): ").strip()
    output_file = output_file + "_subdomains.txt" if output_file else default_filename

    total_domains = len(domains_to_process)
    processed_domains = [0]
    progress_lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=3) as domain_executor:
        futures = {domain_executor.submit(process_domain, domain, output_file, sources, progress_lock, processed_domains, total_domains): domain for domain in domains_to_process}

        for future in as_completed(futures):
            future.result()

    print(Fore.GREEN + f"\n✔ All results saved to {output_file}")