import os
import re
import socket
import threading
from collections import defaultdict
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from bugscanx.modules.utils.utils import get_input

file_write_lock = threading.Lock()
init(autoreset=True)

def read_file_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except Exception as e:
        print(Fore.RED + f" Error reading file {file_path}: {e}")
        return []

def write_file_lines(file_path, lines):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
    except Exception as e:
        print(Fore.RED + f" Error writing to file {file_path}: {e}")

def split_txt_file(file_path, parts):
    lines = read_file_lines(file_path)
    if not lines:
        return

    lines_per_file = len(lines) // parts
    file_base = os.path.splitext(file_path)[0]
    for i in range(parts):
        part_lines = lines[i * lines_per_file: (i + 1) * lines_per_file] if i < parts - 1 else lines[i * lines_per_file:]
        part_file = f"{file_base}_part_{i + 1}.txt"
        write_file_lines(part_file, part_lines)
        print(Fore.GREEN + f" Created file: {part_file}")

def merge_txt_files():
    directory = get_input(Fore.YELLOW + " Input the directory path where your text files are located (or press Enter to use the current directory): ").strip()
    if not directory:
        directory = os.getcwd()

    if not os.path.isdir(directory):
        print(Fore.YELLOW + " The provided directory does not exist. Please check the path and try again.")
        return
    
    merge_all = get_input(Fore.YELLOW + " Do you want to merge all .txt files in the directory? (yes/no): ").strip().lower()
    
    files_to_merge = []
    
    if merge_all == 'yes':
        files_to_merge = [f for f in os.listdir(directory) if f.endswith('.txt')]
    else:
        filenames = input(Fore.YELLOW + " Enter the filenames to merge, separated by commas: ").strip()
        files_to_merge = [filename.strip() for filename in filenames.split(',') if filename.strip()]
        files_to_merge = [f for f in files_to_merge if os.path.isfile(os.path.join(directory, f))]
        
        if not files_to_merge:
            print(Fore.YELLOW + " No valid files were selected. Please check the filenames and try again.")
            return

    output_file = get_input(Fore.YELLOW + " Enter the name for the merged output file (e.g., merged_output.txt): ").strip()
    
    try:
        with open(os.path.join(directory, output_file), 'w', encoding="utf-8") as outfile:
            for filename in files_to_merge:
                with open(os.path.join(directory, filename), 'r', encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")
        print(Fore.GREEN + f" Files have been successfully merged into '{output_file}' in the directory '{directory}'.")
    except Exception as e:
        print(Fore.RED + f" Error merging files: {e}")

def remove_duplicate_domains(file_path):
    lines = read_file_lines(file_path)
    if not lines:
        return

    domains = set(lines)
    write_file_lines(file_path, sorted(domains))
    print(Fore.GREEN + f" Duplicates removed from {file_path}")

def txt_cleaner():
    input_file = get_input(Fore.YELLOW + " Enter the name of the input file containing the data (e.g., source_file.txt): ").strip()
    file_contents = read_file_lines(input_file)
    if not file_contents:
        return

    domain_pattern = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}\b')
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    
    domains = set()
    ips = set()
    
    for line in file_contents:
        domains.update(domain_pattern.findall(line))
        ips.update(ip_pattern.findall(line))
    
    domain_output_file = get_input(Fore.YELLOW + " Enter the name for the output file for domains (e.g., domains.txt): ").strip()
    ip_output_file = get_input(Fore.YELLOW + " Enter the name for the output file for IP addresses (e.g., ips.txt): ").strip()
    
    write_file_lines(domain_output_file, [f"{domain}\n" for domain in sorted(domains)])
    write_file_lines(ip_output_file, [f"{ip}\n" for ip in sorted(ips)])
    
    print(Fore.GREEN + f" Domains have been saved to '{domain_output_file}', and IP addresses have been saved to '{ip_output_file}'.")

def convert_subdomains_to_domains(file_path):
    lines = read_file_lines(file_path)
    if not lines:
        return

    root_domains = set(subdomain.split('.')[-2] + '.' + subdomain.split('.')[-1] for subdomain in lines)
    output_file = f"{os.path.splitext(file_path)[0]}_root_domains.txt"
    write_file_lines(output_file, [f"{domain}\n" for domain in sorted(root_domains)])
    print(Fore.GREEN + f" Subdomains converted to root domains and saved to {output_file}")

def separate_domains_by_extension(file_path):
    lines = read_file_lines(file_path)
    if not lines:
        return

    extensions_dict = defaultdict(list)
    for domain in lines:
        extension = domain.split('.')[-1]
        extensions_dict[extension].append(domain)

    base_name = os.path.splitext(file_path)[0]
    for extension, domain_list in extensions_dict.items():
        ext_file = f"{base_name}_{extension}.txt"
        write_file_lines(ext_file, [f"{domain}\n" for domain in domain_list])
        print(Fore.GREEN + f" Domains with .{extension} saved to {ext_file}")

def resolve_domain_to_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return f"{domain} -> {ip}"
    except socket.gaierror:
        return f"{domain} -> Resolution failed"

def domains_to_ip(file_path):
    lines = read_file_lines(file_path)
    if not lines:
        return

    output_file = f"{os.path.splitext(file_path)[0]}_with_ips.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_domain = {executor.submit(resolve_domain_to_ip, domain): domain for domain in lines}
                for future in as_completed(future_to_domain):
                    file.write(future.result() + "\n")
        print(Fore.GREEN + f" Domain-to-IP mappings saved to {output_file}")
    except Exception as e:
        print(Fore.RED + f" Error resolving domains to IPs: {e}")

def txt_toolkit_main_menu():
    while True:
        print(Fore.CYAN + "🛠️  TXT Toolkit - Select an Option:\n")
        print(Fore.YELLOW + " [1] ✂️  Split TXT File")
        print(Fore.YELLOW + " [2] 🗑️   Remove Duplicate Domains")
        print(Fore.YELLOW + " [3] 🧹  Txt cleaner (extract domains, subdomains & IP )")
        print(Fore.YELLOW + " [4] 📄  Separate Domains by Extensions (like .com, .in )")
        print(Fore.YELLOW + " [5] 🌍  Convert Domains to IP Addresses")
        print(Fore.YELLOW + " [6] 🗂️   Merge Txt files")
        print(Fore.YELLOW + " [7] 🌐  Covert Subdomains to Root domains ")
        print(Fore.RED + " [0] 🚪  Exit" + Style.RESET_ALL)

        choice = get_input(Fore.CYAN + "  ⮞  Enter your choice (0-7): " + Style.RESET_ALL).strip()
        
        if choice == "1":
            file_path = get_input(Fore.CYAN + " Enter the file path: ").strip()
            parts = int(get_input(Fore.CYAN + " Enter number of parts to split the file into: ").strip())
            split_txt_file(file_path, parts)

        elif choice == "2":
            file_path = get_input(Fore.CYAN + " Enter the file path: ").strip()
            remove_duplicate_domains(file_path)

        elif choice == "3":
            txt_cleaner()

        elif choice == "4":
            file_path = get_input(Fore.CYAN + " Enter the file path: ").strip()
            separate_domains_by_extension(file_path)

        elif choice == "5":
            file_path = get_input(Fore.CYAN + " Enter the file path: ").strip()
            domains_to_ip(file_path)

        elif choice == "6":
            merge_txt_files()

        elif choice == "7":
            file_path = get_input(Fore.CYAN + " Enter the file path: ").strip()
            convert_subdomains_to_domains(file_path)

        elif choice == "0":
            print(Fore.RED + " Exiting TXT Toolkit !" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + " Invalid choice. Please try again." + Style.RESET_ALL)


