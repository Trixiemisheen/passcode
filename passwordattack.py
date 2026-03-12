"""""
Built by Trixie Misheen™ All rights reserved. For authorized pentesting use only.
This is a demonstration of various password attack techniques, including a smart "AI Brain" generator that creates intelligent password candidates based on common patterns and mutations.
The script supports multiple attack modes: lightning (top patterns), smart (dictionary + patterns), systematic brute-force, optimized random, and the AI Brain approach.

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


def ai_brain_attack(target_psk, max_length=20, max_threads=8, timeout=60):
    """AI Brain attack: Generate smart passwords dynamically."""
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

            if pw == target_psk:
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


def brute_force_psk(target_psk, keys, max_workers=4):
    psk_len = len(target_psk)

    print(f"[+] Target PSK length: {psk_len}")
    print(f"[+] Charset size: {len(keys)} chars")
    print(f"[+] Total combinations: {len(keys) ** psk_len:,}")

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

            if guess == target_psk:
                return guess, local_attempts

    print("[+] Starting multi-threaded systematic brute force...")

    found = False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for length in range(1, psk_len + 1):

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
                break

    return found


def optimized_random_attack(target_psk, keys, max_attempts=1000000):

    psk_len = len(target_psk)

    print(f"\n[*] Starting optimized random attack (max {max_attempts:,} attempts)...")

    start_time = time.time()
    attempts = 0
    seen = set()

    while attempts < max_attempts:

        guess = ''.join(random.choice(keys) for _ in range(psk_len))

        attempts += 1

        if guess in seen:
            continue

        seen.add(guess)

        if guess == target_psk:

            elapsed = time.time() - start_time

            print(f"\n[!] RANDOM CRACKED: {guess}")
            print(f"[+] Attempts: {attempts:,} | Time: {elapsed:.1f}s")

            return True

        if attempts % 10000 == 0:

            elapsed = time.time() - start_time
            rate = attempts / elapsed
            unique_rate = len(seen) / elapsed

            print(
                f"[*] Random attempts: {attempts:,} | "
                f"Unique: {len(seen):,} | Rate: {unique_rate:.0f}/s"
            )

    print(f"[!] Random attack failed after {attempts:,} attempts")

    return False


def smart_brute_force(
    target_psk,
    keys="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{}|;:,.<>?/~`",
    wordlist=None,
):
    """Hybrid attack: dictionary (optional) + common patterns + brute force.

    If ``wordlist`` is provided and the file exists, test each entry first.
    """

    print("[+] Smart hybrid WPA-PSK attack")

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
                if not guess:
                    continue
                if guess == target_psk:
                    print(f"[!] CRACKED with wordlist entry: {guess}")
                    return True

    print("[*] Phase 1: Common patterns...")

    for i, pattern in enumerate(common_patterns):

        try:
            guess = pattern()

            print(f"[*] Testing pattern {i+1}: {guess}")

            if guess == target_psk:
                print(f"[!] CRACKED with common pattern: {guess}")
                return True

        except:
            continue

    print("[*] Phase 2: Systematic brute force...")

    return brute_force_psk(target_psk, keys)


def lightning_attack(target_psk, keys):

    """Lightning attack"""

    psk_len = len(target_psk)

    print(f"[⚡] LIGHTNING ATTACK v2.0 - {psk_len} chars")

    top100 = [
        "admin", "password", "12345678", "qwerty",
        "admin123", "letmein", "password1",
        "123456789", "password123", "welcome1",
        "monkey123", "admin2024", "Password1", "admin1"
    ]
#$Trixie Misheen™$#
    for guess in top100:
        if guess == target_psk:
            print(f"[⚡] TOP100 HIT: {guess}")
            return guess

    bases = ["password", "admin", "user", "test", "guest", "root", "welcome"]
    suffixes = ["1", "123", "12", "11", "!", "!!", "1!", "123!", "@", "1@"]
    prefixes = ["2024", "2023", "admin", "user"]

    for base in bases:

        for suffix in suffixes:

            guess = base + suffix

            if guess == target_psk:
                print(f"[⚡] BASE+SUFFIX: {guess}")
                return guess

        for prefix in prefixes:

            guess = prefix + base

            if guess == target_psk:
                print(f"[⚡] PREFIX+BASE: {guess}")
                return guess

    for year in range(2000, 2026):

        for sym in ["", "!", "@", "#", "$"]:

            guess = f"password{year}{sym}"
            if guess == target_psk:
                return guess

            guess = f"admin{year}{sym}"
            if guess == target_psk:
                return guess

    password_variants = ["password1!", "Password1!", "p@ssw0rd1!", "Password1"]

    for variant in password_variants:

        if variant == target_psk:
            print(f"[⚡] LEET HIT: {variant}")
            return variant

    print("[⚡] Lightning failed - needs heavy brute")

    return None


class HackerGUI:
    """Dark-themed hacker GUI for password attacks with real-time visualization."""

    def __init__(self, root):
        self.root = root
        self.root.title("🔓 PASSWORD CRACKER™ - AUTHORIZED PENTEST ONLY💀 ")
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
            text="▓▓▓ PASSWORD CRACKER™ ▓▓▓",
            font=("Courier New", 20, "bold"),
            fg=self.neon_green,
            bg=self.bg_darker,
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            header_frame,
            text="⚡ AI-POWERED ATTACK ENGINE™ | AUTHORIZED USE ONLY TRIXIE MISHEEN ⚡",
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

        # Target PSK
        tk.Label(input_frame, text="[>] TARGET PSK:", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)
        self.target_var = tk.StringVar(value="password123")
        target_entry = tk.Entry(input_frame, textvariable=self.target_var,
                               font=("Courier New", 10), bg="#1a1f3a",
                               fg=self.neon_cyan, insertbackground=self.neon_green)
        target_entry.pack(fill=tk.X, pady=(5, 10))

        # Wordlist
        tk.Label(input_frame, text="[>] WORDLIST (optional):", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)
        self.wordlist_var = tk.StringVar()
        wordlist_entry = tk.Entry(input_frame, textvariable=self.wordlist_var,
                                 font=("Courier New", 10), bg="#1a1f3a",
                                 fg=self.neon_cyan, insertbackground=self.neon_green)
        wordlist_entry.pack(fill=tk.X, pady=(5, 10))

    def _create_mode_section(self):
        """Create attack mode selection."""
        mode_frame = tk.Frame(self.root, bg=self.bg_dark)
        mode_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(mode_frame, text="[>] ATTACK MODE:", font=("Courier New", 10, "bold"),
                fg=self.neon_green, bg=self.bg_dark).pack(anchor=tk.W)

        self.mode_var = tk.StringVar(value="lightning")
        modes = ["lightning", "smart", "ai-brain", "systematic", "random"]

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

        target = self.target_var.get().strip()
        if not target:
            self.log_output("[!] ERROR: Enter a target PSK!", "error")
            return

        self.running = True
        self.update_status("Running attack...")
        self.log_output("\n" + "=" * 60)
        self.log_output("    ⚡ ATTACK INITIATED ⚡", "success")
        self.log_output("=" * 60 + "\n")

        self.attack_thread = threading.Thread(
            target=self._run_attack,
            args=(target, self.mode_var.get(), self.wordlist_var.get()),
            daemon=True
        )
        self.attack_thread.start()

    def _run_attack(self, target, mode, wordlist):
        """Run the actual attack."""
        try:
            keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

            self.log_output(f"[*] Mode: {mode.upper()}", "info")
            self.log_output(f"[*] Target: {target}\n", "info")

            if mode == "lightning":
                result = lightning_attack(target, keys)
                if result:
                    self.log_output(f"\n🎯 CRACKED INSTANTLY: {result}\n", "success")
                else:
                    self.log_output("\n[!] Lightning failed...\n", "error")
            elif mode == "ai-brain":
                result, attempts, elapsed = ai_brain_attack(
                    target, max_length=20, max_threads=8, timeout=60
                )
                if result:
                    self.log_output(f"\n🎯 AI BRAIN VICTORY: {result}\n", "success")
                else:
                    self.log_output("\n[!] AI brain exhausted...\n", "error")
            elif mode == "smart":
                smart_brute_force(target, keys, wordlist=wordlist if wordlist else None)
            elif mode == "systematic":
                brute_force_psk(target, keys, max_workers=4)
            elif mode == "random":
                optimized_random_attack(target, keys, max_attempts=1000000)

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
    # Check for CLI args - if provided, run CLI mode; otherwise run GUI
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            description="Password attack toolbox: lightning, smart, brute-force or random")

        parser.add_argument("target", nargs="?",
                            help="target PSK to crack (for demo/testing); if omitted you'll be prompted")
        parser.add_argument("-m", "--mode",
                            choices=["lightning", "smart", "systematic", "random", "ai-brain"],
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

        args = parser.parse_args()

        # if the target was omitted on the command line, fall back to interactive input
        if not args.target:
            args.target = input("Enter target PSK: ").strip()

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
        target_psk = args.target
        log("\n" + "=" * 60)
        log("    PENTEST AUTHORIZED - LIGHTNING CRACKER (demo)")
        log("=" * 60)

        if args.mode == "lightning":
            result = lightning_attack(target_psk, keys)
            if result:
                log(f"\n🎯 CRACKED INSTANTLY: {result}")
            else:
                log("\n[!] Lightning failed - trying smart mode...")
                smart_brute_force(target_psk, keys)
        elif args.mode == "ai-brain":
            result, attempts, elapsed = ai_brain_attack(target_psk, max_length=args.max_length,
                                                        max_threads=args.threads,
                                                        timeout=args.timeout)
            if result:
                log(f"\n🎯 AI BRAIN VICTORY: {result}")
            else:
                log("\n[!] AI brain exhausted, falling back to smart mode...")
                smart_brute_force(target_psk, keys)
        elif args.mode == "smart":
            smart_brute_force(target_psk, keys, wordlist=args.wordlist)
        elif args.mode == "systematic":
            brute_force_psk(target_psk, keys, max_workers=args.threads)
        elif args.mode == "random":
            optimized_random_attack(target_psk, keys, max_attempts=args.max_random)
    else:
        # Launch GUI
        root = tk.Tk()
        gui = HackerGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()

