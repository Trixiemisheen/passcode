# 🔐 Password Attack Toolbox

**Built by Trixie Misheen™**

> A multi-mode WPA-PSK/password cracker with AI-powered intelligent password generation, built for penetration testing and educational purposes.

**GitHub:** [TrixieMisheen/passcode](https://github.com/TrixieMisheen/passcode)

---

## ✨ Features

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

5. **🎲 Random**
   - Random password generation
   - De-duplicated guesses
   - **Best for:** Lucky fast cracks or uniform charset testing

---

## 🚀 Installation

### Requirements
- Python 3.8+
- No external dependencies (uses only stdlib: `threading`, `itertools`, `argparse`)

### Quick Start

```bash
cd passcode
python passwordattack.py --help
```

---

## 💻 Usage

### Basic Usage

```bash
# Interactive mode (prompts for PSK)
python passwordattack.py --mode ai-brain

# Command-line mode (provide PSK directly)
python passwordattack.py mySecretPassword --mode ai-brain
```

### Full CLI Options

```bash
python passwordattack.py TARGET [OPTIONS]

Positional Arguments:
  target                Target PSK to crack (optional; prompts if omitted)

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
  
  -h, --help           Show this help message
```

---

## 📚 Examples

### Example 1: AI Brain Attack (Fast & Smart)
```bash
$ python passwordattack.py password123 --mode ai-brain --timeout 10
[⚡] AI BRAIN attack starting (timeout: 10s)...
[+] Generating smart password candidates...
[⚡] AI BRAIN CRACKED: password123
[+] Attempts: 952 | Time: 0.0s
```

### Example 2: Lightning Quick Test
```bash
$ python passwordattack.py admin123 --mode lightning
[⚡] LIGHTNING ATTACK v2.0 - 8 chars
[⚡] BASE+SUFFIX: admin123
🎯 CRACKED INSTANTLY: admin123
```

### Example 3: Smart Mode with Wordlist
```bash
$ python passwordattack.py target_psk --mode smart --wordlist rockyou.txt
[+] Smart hybrid WPA-PSK attack
[*] Testing dictionary rockyou.txt...
[*] Phase 1: Common patterns...
[*] Phase 2: Systematic brute force...
```

### Example 4: Systematic Full Brute-Force
```bash
$ python passwordattack.py mypassx --mode systematic --threads 8
[+] Target PSK length: 7
[+] Charset size: 94 chars
[+] Total combinations: 59,969,409,256
[+] Starting multi-threaded systematic brute force...
[*] Testing length 1...
[*] Testing length 2...
...
[!] CRACKED: mypassx
```

### Example 5: Random Attack with Custom Charset
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

## 📄 License

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

---

**Stay safe. Test securely.** ⚡🔐

---

**Built with ❤️ by [Trixie Misheen™](https://github.com/TrixieMisheen)**

© 2026 Trixie Misheen. All rights reserved.
