import subprocess
import platform
import threading
from queue import Queue
import os
import time
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Lock for clean printing (prevents overlapping lines)
print_lock = threading.Lock()

def print_banner():
    banner = f"""
{Fore.RED}██████╗ ██╗   ██╗██╗     ██╗ ██████╗ 
{Fore.RED}██╔══██╗╚██╗ ██╔╝██║     ██║██╔════╝ 
{Fore.YELLOW}██████╔╝ ╚████╔╝ ██║     ██║██║  ███╗
{Fore.YELLOW}██╔══██╗  ╚██╔╝  ██║     ██║██║   ██║
{Fore.WHITE}██║  ██║   ██║   ███████╗██║╚██████╔╝
{Fore.WHITE}╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝ ╚═════╝ 
{Fore.CYAN}      >> NETWORK PING SCANNER <<
{Fore.MAGENTA}      Developer: T.me/rylig
    """
    print(banner)

def ping_worker(ip_queue, results_file, stats):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    
    while not ip_queue.empty():
        try:
            current_index, ip = ip_queue.get_nowait()
        except:
            break
            
        command = ['ping', param, '1', timeout_param, '1', ip]
        process = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        is_up = (process.returncode == 0)
        
        with print_lock:
            if is_up:
                print(f"{Fore.WHITE}[{current_index}] {Fore.CYAN}{ip:<15} {Fore.GREEN}Active{Style.RESET_ALL}", flush=True)
                stats['active'] += 1
                with open(results_file, "a") as f:
                    f.write(ip + "\n")
            else:
                print(f"{Fore.WHITE}[{current_index}] {Fore.CYAN}{ip:<15} {Fore.RED}Disabled{Style.RESET_ALL}", flush=True)
                stats['disabled'] += 1
        
        ip_queue.task_done()

def generate_ips(cidr):
    try:
        parts = cidr.split('/')
        base_ip = parts[0]
        ip_prefix = ".".join(base_ip.split('.')[:-1])
        return [f"{ip_prefix}.{i}" for i in range(1, 255)]
    except:
        return []

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_banner()
    
    range_file = input(f"{Fore.YELLOW}📂 Enter range file (e.g., range.txt): {Fore.WHITE}")
    if not os.path.exists(range_file):
        print(f"{Fore.RED}Error: File not found!")
        return

    try:
        thread_input = input(f"{Fore.YELLOW}🚀 Threads (default 30): {Fore.WHITE}")
        thread_count = int(thread_input) if thread_input.strip() else 30
    except:
        thread_count = 30

    all_ips = []
    with open(range_file, "r") as f:
        for r in f.read().splitlines():
            if r.strip():
                all_ips.extend(generate_ips(r.strip()))

    if not all_ips:
        print(f"{Fore.RED}No IPs found.")
        return

    # Stats for final report
    stats = {'active': 0, 'disabled': 0, 'total': len(all_ips)}
    
    print(f"\n{Fore.BLUE}>> Starting Scan at {time.strftime('%H:%M:%S')}")
    print(f"{Fore.BLUE}>> Target: {stats['total']} IPs | Threads: {thread_count}\n" + "="*45)

    start_time = time.time()
    ip_queue = Queue()
    for index, ip in enumerate(all_ips, 1):
        ip_queue.put((index, ip))

    open("active.txt", "w").close()

    for _ in range(thread_count):
        t = threading.Thread(target=ping_worker, args=(ip_queue, "active.txt", stats), daemon=True)
        t.start()

    ip_queue.join()
    end_time = time.time()

    # --- FINAL REPORT ---
    duration = round(end_time - start_time, 2)
    print("="*45)
    print(f"{Fore.MAGENTA}📊 SCAN REPORT SUMMARY")
    print(f"{Fore.WHITE}Total IPs Scanned : {stats['total']}")
    print(f"{Fore.GREEN}Active Hosts      : {stats['active']}")
    print(f"{Fore.RED}Disabled Hosts    : {stats['disabled']}")
    print(f"{Fore.YELLOW}Time Elapsed      : {duration} seconds")
    print(f"{Fore.CYAN}Saved To          : active.txt")
    print(f"{Fore.MAGENTA}Developer ID      : T.me/rylig")
    print("="*45)

if __name__ == "__main__":
    main()
