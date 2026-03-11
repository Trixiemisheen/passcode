import time
import itertools
import os
import random
from collections import deque
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse


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


def main():
    parser = argparse.ArgumentParser(
        description="Password attack toolbox: lightning, smart, brute-force or random")

    parser.add_argument("target", nargs="?",
                        help="target PSK to crack (for demo/testing); if omitted you'll be prompted")
    parser.add_argument("-m", "--mode",
                        choices=["lightning", "smart", "systematic", "random"],
                        default="lightning",
                        help="attack mode to run")
    parser.add_argument("-k", "--charset",
                        default="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{}|;:,.<>?/~`",
                        help="custom character set for brute force")
    parser.add_argument("-w", "--wordlist",
                        help="wordlist file used by smart/lightning modes")
    parser.add_argument("-t", "--threads", type=int, default=4,
                        help="max worker threads for systematic brute force")
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
    elif args.mode == "smart":
        smart_brute_force(target_psk, keys, wordlist=args.wordlist)
    elif args.mode == "systematic":
        brute_force_psk(target_psk, keys, max_workers=args.threads)
    elif args.mode == "random":
        optimized_random_attack(target_psk, keys, max_attempts=args.max_random)


if __name__ == "__main__":
    main()

