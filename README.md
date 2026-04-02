# 🔍 NetRecon-Assist - Beginner Friendly IP Scanner & CVE Analyzer

## 📌 What is This Project?

**NetRecon-Assist** is an educational IP scanning and vulnerability analysis tool designed specifically for **beginners**. It helps you:

✅ Find all open ports on an IP address  
✅ Identify what services are running  
✅ Discover security vulnerabilities (CVEs)  
✅ Learn why ports should be closed  
✅ Get step-by-step guidance on securing your system

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**

```bash
cd NetRecon-Assist
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

Or install tabulate manually:

```bash
pip install tabulate
```

---

## 📖 How to Use

### Basic Usage

Run the scanner:

```bash
python main.py
```

### Step 1: Enter Target IP

```
Enter Target IP: 192.168.1.100
```

(Use localhost `127.0.0.1` for testing on your own machine)

### Step 2: Choose Scan Mode

You'll see 3 options:

**Option 1️⃣ - Scan ALL Ports (1–65535)**

- ⏱️ Takes longer (5-10 minutes)
- 🔍 Finds every open port
- Best for: Complete vulnerability assessment

**Option 2️⃣ - Scan COMMON Ports (RECOMMENDED)**

- ⚡ Fast (few seconds)
- 📊 Covers 99% of real-world scenarios
- Best for: Quick security check

**Option 3️⃣ - Scan SPECIFIC Ports**

- ⚙️ Custom ports (e.g., `80,443,3306`)
- 🎯 Focused scanning
- Best for: Testing specific services

### Example Scan

```
🔍 BEGINNER FRIENDLY IP SCANNER & CVE ANALYZER 🔍

Enter Target IP: 127.0.0.1

📋 CHOOSE SCAN MODE:
1️⃣  Scan ALL Ports (1–65535)      [Slower, Complete scan]
2️⃣  Scan COMMON Ports             [Faster, Most used ports]
3️⃣  Scan SPECIFIC Ports (e.g. 80,443) [Custom ports]

Enter choice (1/2/3): 2
```

---

## 📊 Understanding the Output

### 1. OPEN PORTS TABLE

Shows all discovered open ports with details:

| Port | Service | Version       | Description         |
| ---- | ------- | ------------- | ------------------- |
| 80   | APACHE  | Apache 2.4.18 | Web Server HTTP     |
| 22   | SSH     | OpenSSH 7.2   | Secure Shell Access |
| 3306 | MYSQL   | 5.5           | Database Management |

### 2. BEGINNER GUIDANCE FOR EACH PORT

For each open port, you get:

- **Risk Level**: HIGH ⚠️ or LOW ✅
- **Status**: Whether it should be open
- **Guidance**: Easy-to-understand explanation

Example:

```
🔹 PORT 80 (APACHE)
   Status  : ✅ RISK: LOW - Generally safe
   Guidance: Apache is a web server. Keep it patched to avoid hacking.

🔹 PORT 3306 (MYSQL)
   Status  : ⚠️  RISK: HIGH - Should be closed
   Guidance: MySQL is a database. Never expose to internet - very risky.
```

### 3. VULNERABILITY & CVE ANALYSIS

Shows security issues found with:

- **CVE ID**: Official vulnerability identifier
- **Issue**: What the problem is
- **Impact**: What could happen if exploited
- **How to Exploit**: How attackers could use it
- **How to Prevent**: How to fix it

---

## 🛡️ Common Vulnerabilities Explained

### 🔴 CRITICAL PORTS (Close Immediately!)

**Port 23 - TELNET**

- Problem: Sends passwords in plain text
- Risk: Hackers can see your password
- Solution: Use SSH instead (port 22)

**Port 3306 - MySQL**

- Problem: Database exposed to internet
- Risk: All your data can be stolen
- Solution: Bind to localhost only, use firewall

**Port 6379 - Redis**

- Problem: No password by default
- Risk: Anyone can read/write your data
- Solution: Enable authentication, restrict access

**Port 3389 - RDP**

- Problem: Remote desktop exposed
- Risk: Full system takeover possible
- Solution: Use VPN, disable if not needed

### 🟡 MEDIUM RISK PORTS

**Port 80/443 - HTTP/HTTPS**

- Generally safe if web server is updated
- Keep software patched
- Use firewall rules

**Port 22 - SSH**

- Secure if configured properly
- Use strong passwords
- Disable root login

---

## 🔧 How to Close an Open Port

### Windows

1. Press `Win + R` → type `services.msc`
2. Find the service (Apache, MySQL, etc.)
3. Right-click → Stop or Disable

### Linux/macOS

```bash
# Stop a service
sudo systemctl stop [service-name]

# Disable it permanently
sudo systemctl disable [service-name]

# Examples
sudo systemctl stop apache2
sudo systemctl stop mysql
```

### Cloud (AWS, Google Cloud, Azure)

1. Go to Security Groups / Firewall Rules
2. Remove the inbound rule for the port
3. Save changes

---

## 📚 Beginner Learning Guide

### Understanding Ports

- **Port**: A numbered entry point for network services
- **Range**: 0 - 65535 (65,536 total)
- **Well-known**: 0-1023 (system ports)
- **Registered**: 1024-49151 (applications)
- **Dynamic**: 49152-65535 (temporary)

### What is CVE?

- **CVE** = Common Vulnerabilities and Exposures
- A unique ID for known security flaws
- Format: CVE-YYYY-NNNNN
- Example: CVE-2021-41773

### Risk Assessment Matrix

```
Port Status                      Risk Level
===============================================
Port 23 (Telnet)                CRITICAL 🔴
Port 3306 (MySQL)               CRITICAL 🔴
Port 6379 (Redis)               CRITICAL 🔴
Port 3389 (RDP)                 CRITICAL 🔴

Port 25 (SMTP)                  HIGH 🟡
Port 21 (FTP)                   HIGH 🟡

Port 80/443 (HTTP/HTTPS)        MEDIUM 🟠
Port 22 (SSH)                   MEDIUM 🟠
```

---

## 🎯 Quick Security Checklist

After running the scanner, follow this checklist:

- [ ] Identify all open ports
- [ ] Check which are necessary
- [ ] Close unnecessary ports
- [ ] Update all services
- [ ] Review CVE issues
- [ ] Apply security patches
- [ ] Set up firewall rules
- [ ] Use strong passwords
- [ ] Enable encryption (HTTPS, SSH)
- [ ] Test again

---

## 📝 Project Structure

```
NetRecon-Assist/
├── main.py              # Main entry point
├── analyzer.py          # Port scanning & CVE analysis logic
├── cve_db.json          # CVE vulnerability database
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### main.py

- Takes user input
- Manages scan options
- Displays formatted results
- Provides summary and recommendations

### analyzer.py

- **scan_ports()**: TCP port scanning
- **print_ports_table()**: Formatted port output
- **provide_port_guidance()**: Beginner-friendly explanations
- **cve_analysis()**: Vulnerability assessment

### cve_db.json

- Database of known CVEs
- Exploit information
- Prevention recommendations

---

## ⚠️ Important Notes

1. **Get Permission First**
   - Only scan IPs you own or have permission to test
   - Never scan other people's systems without permission
   - Unauthorized scanning is illegal

2. **Local Testing**
   - Use `127.0.0.1` or `localhost` to test on your own machine
   - Safe for learning and practice

3. **Accuracy**
   - This is an educational tool
   - For production use, use professional tools like Nmap
   - Results depend on network conditions

4. **Timeout Settings**
   - Default: 0.4 seconds per port
   - Slow network? Increase in `analyzer.py` if needed

---

## 🐛 Troubleshooting

### "No module named 'tabulate'"

```bash
pip install tabulate
```

### Scanner is too slow

- Use option 2 (Common ports) instead of 1
- Increase timeout in analyzer.py: `s.settimeout(1.0)`

### Results show "UNKNOWN" for ports

- The service isn't in our database
- Add it to `PORT_SERVICES` in analyzer.py

### No open ports found

- All ports are closed ✅ (Good!)
- Try scanning a well-known port like 80 or 443
- Check if network connectivity is working

---

## 📖 Learning Resources

- **Networking Basics**: [Khan Academy](https://www.khanacademy.org/)
- **TCP/IP Explained**: [Cisco Networking](https://www.cisco.com/)
- **Security Best Practices**: [OWASP](https://owasp.org/)
- **CVE Database**: [NVD.NIST.GOV](https://nvd.nist.gov/)

---

## 🤝 Contributing

Want to improve this project?

1. Add more CVEs to `cve_db.json`
2. Add more port services to `PORT_SERVICES`
3. Improve beginner guidance text
4. Report bugs or suggest features

---

## 📄 License

This is an educational project. Use responsibly and ethically.

---

## 🎓 Educational Purpose

This tool is created for learning about:

- Network security basics
- Port scanning techniques
- Vulnerability assessment
- Security best practices
- Defensive security measures

**Remember**: Security is not about offense, it's about defense! 🛡️

---

## 📞 Questions?

- Read the guidance in the tool output
- Check this README
- Study the code comments
- Research the CVE IDs mentioned

---

**Last Updated**: February 2, 2026  
**Version**: 1.0  
**Status**: Educational Tool ✅
