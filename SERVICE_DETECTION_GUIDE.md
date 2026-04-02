# SERVICE DETECTION & DISABLE GUIDE

> **Enhanced IP Scanner with Accurate Service Detection & Practical Disable Instructions**

---

## 🎯 NEW FEATURES

### ✅ Accurate Service Detection

- Detects what service is actually running on each port
- Retrieves service banner information
- Identifies ports with unexpected services

### ✅ Detailed Disable Instructions

- Linux/Unix step-by-step commands
- Windows GUI instructions
- Service verification commands
- Why the service should be disabled

### ✅ Comprehensive Risk Assessment

- Critical vs. Low risk ports
- Security vulnerabilities
- Real-world attack scenarios

---

## 🔧 HOW IT WORKS

### Step 1: Port Scanning

```bash
python main.py
Enter IP: 127.0.0.1
Choose: 2 (Common ports)
```

### Step 2: Service Detection

Scanner connects to each port and retrieves:

- Service banner (e.g., "SSH-2.0-OpenSSH_7.2")
- Running status
- Detected version info

### Step 3: Risk Assessment

Shows:

- Port number
- Service name
- Description
- **Detected service** (actual vs. expected)
- Risk level

### Step 4: Disable Instructions

For risky ports, provides:

- Why it's dangerous
- Why you should disable it
- Linux commands
- Windows steps
- How to verify

---

## 📊 ENHANCED PORT STRUCTURE

Each port now has **5 fields**:

```python
PORT_SERVICES = {
    22: (
        "ssh",                          # Service name
        "OpenSSH 7.2",                  # Default version
        "Secure Shell Access",          # Description
        "sshd",                         # Service name for systemctl
        "sudo systemctl stop ssh"       # Quick disable command
    )
}
```

---

## 🛑 DISABLE INSTRUCTIONS BY PORT

### Port 21 (FTP)

```
Why Risky: Sends passwords in PLAIN TEXT over network
Why Disable: Modern systems use SFTP (SSH) instead

Linux:
  $ sudo systemctl stop vsftpd
  $ sudo systemctl disable vsftpd

Windows:
  Services > vsftpd > Disabled > Apply

Verify:
  $ sudo systemctl status vsftpd
```

### Port 23 (TELNET) - MOST DANGEROUS!

```
Why Risky: ZERO encryption - all data visible on network
Why Disable: COMPLETELY DEPRECATED - SSH is replacement

Linux:
  $ sudo systemctl stop telnetd
  $ sudo systemctl disable telnetd

Windows:
  Services > Telnet > Disabled > Apply

Verify:
  $ sudo systemctl status telnetd
```

### Port 25 (SMTP)

```
Why Risky: Open relay can be used for spam attacks
Why Disable: Restrict SMTP to internal use only

Linux:
  $ sudo systemctl stop postfix
  $ sudo systemctl disable postfix

Windows:
  Control Panel > Programs > Remove Programs > SMTP

Verify:
  $ sudo systemctl status postfix
```

### Port 3306 (MySQL)

```
Why Risky: Databases should NEVER be exposed to internet
Why Disable: Direct database access enables complete data theft

Linux:
  $ sudo systemctl stop mysql
  $ sudo systemctl disable mysql
  Edit /etc/mysql/my.cnf: bind-address=127.0.0.1

Windows:
  Services > MySQL > Disabled > Apply

Verify:
  $ sudo systemctl status mysql
```

### Port 3389 (RDP)

```
Why Risky: BlueKeep vulnerability allows unauthenticated takeover
Why Disable: Use VPN instead. If needed, restrict to internal network only

Linux:
  $ sudo systemctl stop xrdp
  $ sudo systemctl disable xrdp

Windows:
  Settings > System > Remote Desktop > Off

Verify:
  $ sudo systemctl status xrdp
```

### Port 6379 (Redis)

```
Why Risky: Default configuration has NO password protection
Why Disable: Ransomware uses this to wipe cached data

Linux:
  $ sudo systemctl stop redis-server
  Edit /etc/redis/redis.conf: requirepass [strong_password]

Windows:
  Services > Redis > Disabled > Apply

Verify:
  $ redis-cli ping
```

### Port 27017 (MongoDB)

```
Why Risky: Millions of records have been publicly exposed
Why Disable: Firewall MongoDB and enable authentication immediately

Linux:
  $ sudo systemctl stop mongod
  Edit /etc/mongod.conf: security.authorization enable

Windows:
  Services > MongoDB > Disabled > Apply

Verify:
  $ sudo systemctl status mongod
```

### Port 5432 (PostgreSQL)

```
Why Risky: Database exposure leads to complete data compromise
Why Disable: Database should only be accessible from app servers

Linux:
  $ sudo systemctl stop postgresql
  Edit /etc/postgresql/*/main/postgresql.conf: listen_addresses='localhost'

Windows:
  Services > PostgreSQL > Disabled > Apply

Verify:
  $ sudo systemctl status postgresql
```

### Port 5984 (CouchDB)

```
Why Risky: Admin party mode gives everyone admin privileges by default
Why Disable: Enable authentication and disable admin party mode

Linux:
  $ sudo systemctl stop couchdb
  Edit /opt/couchdb/etc/couchdb/local.ini: admin party disabled

Windows:
  Services > CouchDB > Disabled > Apply

Verify:
  $ sudo systemctl status couchdb
```

---

## 📊 OUTPUT EXAMPLE

### Ports Table with Service Detection

```
+------+---------+--------------------+-------------------+----------+
| Port | Service | Description        | Detected          | Risk     |
+======+=========+====================+===================+==========+
|   22 | SSH     | Secure Shell       | SSH-2.0-OpenSSH   | LOW      |
+------+---------+--------------------+-------------------+----------+
|   80 | APACHE  | Web Server HTTP    | Apache 2.4.18     | LOW      |
+------+---------+--------------------+-------------------+----------+
|   23 | TELNET  | Remote Shell       | Service running   | CRITICAL |
+------+---------+--------------------+-------------------+----------+
| 3306 | MYSQL   | Database           | MySQL 5.5         | CRITICAL |
+------+---------+--------------------+-------------------+----------+
```

### Detailed Guidance for Each Port

```
[PORT 23] TELNET
Description: Unencrypted Remote Shell
Service Name: telnetd
Default Command: sudo systemctl stop telnetd
Status: RISKY - Should be CLOSED
Guidance: TELNET is VERY DANGEROUS - uses no encryption. Always disable it.

   === HOW TO DISABLE THIS SERVICE ===
   Why Risky: ZERO encryption - all data visible on network
   Why Disable: COMPLETELY DEPRECATED - SSH is replacement

   Linux Steps:
     $ sudo systemctl stop telnetd
     $ sudo systemctl disable telnetd

   Windows Steps:
     > Services > Telnet > Disabled > Apply

   Verify: sudo systemctl status telnetd
```

---

## 🚀 USAGE

### Run Enhanced Scanner

```bash
python main.py
```

### Features

1. **Accurate Detection** - Knows what service actually runs
2. **Risk Assessment** - Shows CRITICAL vs LOW
3. **Practical Steps** - Linux + Windows instructions
4. **Verification** - How to confirm service is stopped

---

## 🔐 SECURITY CHECKLIST

After scanning, use this checklist:

- [ ] Port 21 (FTP) disabled? Switch to SFTP
- [ ] Port 23 (TELNET) disabled? Use SSH instead
- [ ] Port 25 (SMTP) restricted? Only internal use
- [ ] Port 3306 (MySQL) firewalled? Internal only
- [ ] Port 3389 (RDP) behind VPN? Not public
- [ ] Port 6379 (Redis) password protected?
- [ ] Port 27017 (MongoDB) authentication enabled?
- [ ] Port 5432 (PostgreSQL) accessible from app server only?
- [ ] Port 5984 (CouchDB) admin party disabled?

---

## 💡 TIPS

### For Linux Users

```bash
# See all running services
sudo systemctl list-units --type=service --state=running

# Stop a service
sudo systemctl stop [service-name]

# Disable service from starting at boot
sudo systemctl disable [service-name]

# Check service status
sudo systemctl status [service-name]
```

### For Windows Users

```
Services Management:
  1. Press Win+R
  2. Type: services.msc
  3. Find your service
  4. Right-click > Properties > Startup type > Disabled
  5. Click Apply > OK

Or use PowerShell:
  Stop-Service -Name [ServiceName]
  Set-Service -Name [ServiceName] -StartupType Disabled
```

---

## 📋 PORT REFERENCE QUICK LOOKUP

| Port  | Service    | Risk     | Action                      |
| ----- | ---------- | -------- | --------------------------- |
| 21    | FTP        | CRITICAL | Disable - Use SFTP          |
| 22    | SSH        | LOW      | Keep - Secure remote access |
| 23    | TELNET     | CRITICAL | Disable - Completely!       |
| 25    | SMTP       | HIGH     | Restrict to internal        |
| 80    | HTTP       | LOW      | Redirect to HTTPS           |
| 443   | HTTPS      | LOW      | Keep - Secure web           |
| 3306  | MySQL      | CRITICAL | Firewall to localhost       |
| 3389  | RDP        | CRITICAL | VPN only                    |
| 6379  | Redis      | CRITICAL | Password + Firewall         |
| 27017 | MongoDB    | CRITICAL | Enable auth + Firewall      |
| 5432  | PostgreSQL | CRITICAL | Internal network only       |
| 5984  | CouchDB    | CRITICAL | Disable admin party         |

---

## 🎓 LEARNING EXAMPLES

### Example 1: Scan & Fix FTP

```bash
$ python main.py
Enter IP: 192.168.1.1
Mode: 2 (Common)

Output:
[PORT 21] FTP
Service Name: vsftpd
Default Command: sudo systemctl stop vsftpd
Status: RISKY - Should be CLOSED

   === HOW TO DISABLE THIS SERVICE ===
   Why Risky: Sends passwords in PLAIN TEXT

   $ sudo systemctl stop vsftpd
   $ sudo systemctl disable vsftpd
```

### Example 2: Scan & Secure MySQL

```bash
$ python main.py
Enter IP: 10.0.0.5
Mode: 2

Output:
[PORT 3306] MYSQL
Service Name: mysqld
Status: RISKY - Should be CLOSED

   === HOW TO DISABLE THIS SERVICE ===
   Why Disable: Direct database access = data theft

   $ sudo systemctl stop mysql
   $ sudo systemctl disable mysql
   Edit /etc/mysql/my.cnf: bind-address=127.0.0.1
```

---

## ✅ VERIFICATION

After disabling a service:

```bash
# Verify service is stopped
sudo systemctl status [service-name]

# Verify port is closed
sudo netstat -tulpn | grep :[port-number]

# Scan again to confirm
python main.py
```

---

## 🌟 SUMMARY

**This enhanced version provides:**

✓ Accurate service detection (not just port guessing)
✓ Comprehensive disable instructions (Linux + Windows)
✓ Risk assessment (CRITICAL vs LOW)
✓ Real-world security guidance
✓ Step-by-step troubleshooting
✓ Verification procedures

**Now you have everything needed to:**

- Identify open services
- Understand why they're risky
- Know exactly how to disable them
- Verify they're stopped

**Security is just a few commands away!** 🔒
