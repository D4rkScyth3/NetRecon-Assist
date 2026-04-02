import socket
import json
import sys
from tabulate import tabulate

# Port → Service + Version mapping
PORT_SERVICES = {
    21: ("ftp", "vsftpd 2.3.4", "File Transfer Protocol", "vsftpd", "sudo systemctl stop vsftpd"),
    22: ("ssh", "OpenSSH 7.2", "Secure Shell Access", "sshd", "sudo systemctl stop ssh"),
    23: ("telnet", "telnet", "Unencrypted Remote Shell", "telnetd", "sudo systemctl stop telnetd"),
    25: ("smtp", "SMTP", "Email Sending Service", "postfix", "sudo systemctl stop postfix"),
    80: ("http", "Apache 2.4.18", "Web Server HTTP", "apache2", "sudo systemctl stop apache2"),
    135: ("msrpc", "RPC Endpoint Mapper", "RPC Port Mapper Service", "rpcbind", "sudo systemctl stop rpcbind"),
    139: ("netbios-ssn", "NetBIOS", "NetBIOS Session Service", "smbd", "sudo systemctl stop smbd"),
    443: ("https", "TLS/SSL", "Web Server HTTPS", "apache2", "sudo systemctl stop apache2"),
    445: ("microsoft-ds", "SMB/CIFS", "File Sharing & Printing", "smbd", "sudo systemctl stop smbd"),
    3306: ("mysql", "5.5", "Database Management", "mysqld", "sudo systemctl stop mysql"),
    3389: ("rdp", "RDP", "Remote Desktop", "xrdp", "sudo systemctl stop xrdp"),
    6379: ("redis", "any", "In-Memory Data Cache", "redis-server", "sudo systemctl stop redis-server"),
    27017: ("mongodb", "any", "NoSQL Database", "mongod", "sudo systemctl stop mongod"),
    8080: ("http-alt", "Apache", "Alternate Web Port", "apache2", "sudo systemctl stop apache2"),
    3307: ("mysql-alt", "MySQL", "Alternate Database", "mysqld", "sudo systemctl stop mysql"),
    5432: ("postgresql", "PostgreSQL", "Object Database", "postgresql", "sudo systemctl stop postgresql"),
    5984: ("couchdb", "CouchDB", "Document Database", "couchdb", "sudo systemctl stop couchdb"),
    8000: ("http", "Python", "Development Web", "python", "sudo kill -9 $(lsof -t -i :8000)"),
    49152: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd"),
    49153: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd"),
    49154: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd"),
    49155: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd"),
    49156: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd"),
    49157: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd"),
    49158: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd"),
    49159: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd"),
    49160: ("ephemeral-rpc", "Dynamic RPC", "RPC Dynamic Port", "rpc.statd", "sudo systemctl stop rpc.statd")
}

# Ports jo generally unnecessary / risky maane jaate hain
UNNECESSARY_PORTS = [21, 23, 25, 135, 139, 445, 3306, 3389, 6379, 27017, 5432, 5984, 49152, 49153, 49154, 49155, 49156, 49157, 49158, 49159, 49160]

# Service descriptions for beginner guidance
SERVICE_GUIDANCE = {
    "ftp": "FTP allows file transfer. It sends passwords in plain text. NOT SAFE for public access.",
    "ssh": "SSH is for remote server access. Keep it updated and use strong passwords.",
    "telnet": "TELNET is VERY DANGEROUS - uses no encryption. Always disable it.",
    "smtp": "SMTP sends emails. Can be exploited for spam. Limit to trusted IPs only.",
    "http": "HTTP is standard web traffic. Keep web server patched and secured.",
    "https": "HTTPS is secure web traffic. Generally safe if updated.",
    "msrpc": "RPC Endpoint Mapper - used for remote procedure calls. High risk if exposed.",
    "netbios-ssn": "NetBIOS - legacy Windows file sharing. Should be disabled on internet-facing systems.",
    "microsoft-ds": "SMB/CIFS - Windows file and printer sharing. NEVER expose directly to internet.",
    "mysql": "MySQL is a database. Never expose to internet - very risky.",
    "rdp": "RDP allows remote desktop access. Disable if not needed - highly targeted.",
    "redis": "Redis stores data in memory. No authentication by default - VERY RISKY.",
    "mongodb": "MongoDB is a database. Disable public access immediately.",
    "http-alt": "Alternative HTTP port. Check if needed.",
    "postgresql": "PostgreSQL database. Keep private and never expose.",
    "couchdb": "Document database. Requires authentication - disable if unused.",
    "ephemeral-rpc": "Dynamic RPC ports - used for Windows RPC services. Should be firewalled."
}

# Service disable instructions (detailed)
DISABLE_INSTRUCTIONS = {
    21: {
        "service": "vsftpd (FTP Server)",
        "why_risky": "Sends passwords in plain text over network",
        "why_disable": "Modern systems use SFTP (SSH) instead which is encrypted",
        "linux_disable": ["sudo systemctl stop vsftpd", "sudo systemctl disable vsftpd"],
        "windows_disable": ["Services > vsftpd > Disabled > Apply"],
        "verify": "sudo systemctl status vsftpd"
    },
    23: {
        "service": "telnetd (TELNET)",
        "why_risky": "ZERO encryption - all data visible on network",
        "why_disable": "COMPLETELY DEPRECATED - SSH is replacement",
        "linux_disable": ["sudo systemctl stop telnetd", "sudo systemctl disable telnetd"],
        "windows_disable": ["Services > Telnet > Disabled > Apply"],
        "verify": "sudo systemctl status telnetd"
    },
    25: {
        "service": "Postfix/SMTP",
        "why_risky": "Open relay can be used for spam attacks",
        "why_disable": "Restrict SMTP to internal use only or disable if not needed",
        "linux_disable": ["sudo systemctl stop postfix", "sudo systemctl disable postfix"],
        "windows_disable": ["Control Panel > Programs > Remove Programs > SMTP"],
        "verify": "sudo systemctl status postfix"
    },
    3306: {
        "service": "MySQL Database",
        "why_risky": "Databases should NEVER be exposed to internet",
        "why_disable": "Direct database access enables complete data theft",
        "linux_disable": ["sudo systemctl stop mysql", "sudo systemctl disable mysql", "Check /etc/mysql/my.cnf: bind-address=127.0.0.1"],
        "windows_disable": ["Services > MySQL > Disabled > Apply"],
        "verify": "sudo systemctl status mysql"
    },
    3389: {
        "service": "RDP (Remote Desktop)",
        "why_risky": "BlueKeep vulnerability allows unauthenticated takeover",
        "why_disable": "Use VPN instead. If needed, restrict to internal network only",
        "linux_disable": ["sudo systemctl stop xrdp", "sudo systemctl disable xrdp"],
        "windows_disable": ["Settings > System > Remote Desktop > Off"],
        "verify": "sudo systemctl status xrdp"
    },
    6379: {
        "service": "Redis Cache",
        "why_risky": "Default configuration has NO password protection",
        "why_disable": "Ransomware uses this to wipe cached data",
        "linux_disable": ["sudo systemctl stop redis-server", "Edit /etc/redis/redis.conf: requirepass [strong_password]"],
        "windows_disable": ["Services > Redis > Disabled > Apply"],
        "verify": "redis-cli ping"
    },
    27017: {
        "service": "MongoDB Database",
        "why_risky": "Millions of records have been publicly exposed",
        "why_disable": "Firewall MongoDB and enable authentication immediately",
        "linux_disable": ["sudo systemctl stop mongod", "Edit /etc/mongod.conf: security.authorization enable"],
        "windows_disable": ["Services > MongoDB > Disabled > Apply"],
        "verify": "sudo systemctl status mongod"
    },
    5432: {
        "service": "PostgreSQL Database",
        "why_risky": "Database exposure leads to complete data compromise",
        "why_disable": "Database should only be accessible from application servers",
        "linux_disable": ["sudo systemctl stop postgresql", "Edit /etc/postgresql/*/main/postgresql.conf: listen_addresses='localhost'"],
        "windows_disable": ["Services > PostgreSQL > Disabled > Apply"],
        "verify": "sudo systemctl status postgresql"
    },
    5984: {
        "service": "CouchDB Database",
        "why_risky": "Admin party mode gives everyone admin privileges by default",
        "why_disable": "Enable authentication and disable admin party mode",
        "linux_disable": ["sudo systemctl stop couchdb", "Edit /opt/couchdb/etc/couchdb/local.ini: admin party disabled"],
        "windows_disable": ["Services > CouchDB > Disabled > Apply"],
        "verify": "sudo systemctl status couchdb"
    },
    135: {
        "service": "RPC Endpoint Mapper",
        "why_risky": "Leaks information about Windows RPC services and can be exploited",
        "why_disable": "Disable RPC on internet-facing servers. Use firewall rules to restrict",
        "linux_disable": ["sudo systemctl stop rpcbind", "sudo systemctl disable rpcbind"],
        "windows_disable": ["Services > RpcSs > Disabled (only if no RPC services needed)"],
        "verify": "sudo systemctl status rpcbind"
    },
    139: {
        "service": "NetBIOS Session Service",
        "why_risky": "Legacy Windows file sharing - can leak system information",
        "why_disable": "NBSTAT, NetBIOS name resolution should be disabled on public networks",
        "linux_disable": ["sudo systemctl stop nmbd", "Edit /etc/samba/smb.conf: disable netbios"],
        "windows_disable": ["Network Settings > Advanced > Disable NetBIOS over TCP/IP"],
        "verify": "netstat -an | grep :139"
    },
    445: {
        "service": "SMB/CIFS (File Sharing)",
        "why_risky": "WannaCry, NotPetya, and many ransomware attacks exploit SMB",
        "why_disable": "CRITICAL - Never expose to internet. Use firewall to block externally",
        "linux_disable": ["sudo systemctl stop smbd", "Edit /etc/samba/smb.conf: interfaces = 127.0.0.1"],
        "windows_disable": ["Disable File and Printer Sharing for Microsoft Networks (for untrusted networks)"],
        "verify": "netstat -an | grep :445"
    },
    49152: {
        "service": "Ephemeral RPC Port",
        "why_risky": "Used by Windows RPC services - can leak information and be exploited",
        "why_disable": "Firewall these ports and restrict to internal networks only",
        "linux_disable": ["These are dynamic ports - restrict them at firewall level"],
        "windows_disable": ["Windows Firewall > Inbound Rules > Block Dynamic RPC ports"],
        "verify": "netstat -an | grep LISTEN"
    }
}


# Detect what service is actually running on a port
def detect_service_on_port(ip, port):
    """Try to detect what service is running on the port"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((ip, port))
        
        # Try to get service banner
        try:
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            s.close()
            if banner:
                return banner[:50]  # First 50 chars
        except:
            pass
        
        s.close()
        return "Service running"
    except:
        return "Unknown"


# Get disable guide
def get_disable_guide(port):
    """Get detailed disable instructions"""
    if port not in DISABLE_INSTRUCTIONS:
        return None
    return DISABLE_INSTRUCTIONS[port]


# Also load the detailed ports database
def load_ports_database():
    try:
        with open("ports_database.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


# ---------------- LOAD CVE DATABASE ----------------
def load_cve_db():
    with open("cve_db.json", "r") as f:
        return json.load(f)


# ---------------- PORT SCANNING WITH PROGRESS ----------------
def scan_ports(ip, ports):
    open_ports = []
    total_ports = len(ports)

    print("\n[*] Port scanning started...\n")

    for index, port in enumerate(ports, start=1):
        # progress indicator
        sys.stdout.write(f"\rScanning port {index}/{total_ports}")
        sys.stdout.flush()

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.4)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except:
            pass

    print("\n[*] Port scanning completed.\n")
    return open_ports


# ---------------- PORT TABLE OUTPUT WITH SERVICE DETECTION ----------------
def print_ports_table(open_ports, ip="127.0.0.1"):
    """Display open ports with service detection and risk assessment"""
    active_services = []
    unnecessary_ports = []
    
    for port in open_ports:
        if port in PORT_SERVICES:
            service, version, description, service_name, disable_cmd = PORT_SERVICES[port]
            
            # Detect actual service
            detected = detect_service_on_port(ip, port)
            
            # Check if service is actually running or just port open
            is_running = detected and detected != "Service running" and detected.strip() != ""
            
            if is_running:
                # Risk level for active services
                if port in UNNECESSARY_PORTS:
                    risk = "HIGH"
                else:
                    risk = "LOW"
                
                active_services.append([
                    port,
                    service.upper(),
                    description,
                    detected[:50],
                    risk
                ])
            else:
                # Port open but no service - unnecessary!
                unnecessary_ports.append([
                    port,
                    service.upper(),
                    description,
                    "⚠️ NO SERVICE"
                ])
        else:
            active_services.append([port, "UNKNOWN", "Unknown service", "?", "?"])
    
    # Section 1: Active Services
    if active_services:
        print("\n" + "="*80)
        print("SECTION 1: ACTIVE SERVICES")
        print("="*80 + "\n")
        # Truncate long detected service names
        display_data = []
        for row in active_services:
            port, service, desc, detected, risk = row
            detected_short = (detected[:40] + "...") if len(detected) > 40 else detected
            desc_short = (desc[:25] + "...") if len(desc) > 25 else desc
            display_data.append([port, service, desc_short, detected_short, risk])
        headers = ["Port", "Service", "Description", "Detected", "Risk"]
        print(tabulate(display_data, headers=headers, tablefmt="simple"))
    
    # Section 2: Unnecessary Open Ports
    if unnecessary_ports:
        print("\n" + "="*80)
        print("SECTION 2: UNNECESSARY OPEN PORTS")
        print("="*80)
        print("ALERT: These ports are OPEN but NO service is running!")
        print("ACTION: Close these immediately to improve security.\n")
        headers = ["Port", "Service", "Description", "Status"]
        print(tabulate(unnecessary_ports, headers=headers, tablefmt="simple"))
    
    print()
    return active_services, unnecessary_ports


# ---------------- UNNECESSARY PORT FILTER ----------------
def get_unnecessary_ports(open_ports):
    unnecessary = [p for p in open_ports if p in UNNECESSARY_PORTS]
    return unnecessary


# ---------------- PROVIDE GUIDANCE FOR UNNECESSARY PORTS ONLY ----------------
def provide_unnecessary_port_guidance(unnecessary_ports_list, ip):
    """Give detailed guidance ONLY for ports with no service running"""
    if not unnecessary_ports_list:
        return
    
    print("\n" + "="*80)
    print("SECTION 3: DETAILED SECURITY RECOMMENDATIONS")
    print("="*80)
    print("\nWHY ARE THESE PORTS DANGEROUS?")
    print("  * Port is OPEN but no legitimate service is using it")
    print("  * Attackers can exploit open ports for backdoor access")
    print("  * Increases attack surface unnecessarily")
    print("  * Security Best Practice: Close all unused ports!")
    print("="*80 + "\n")
    
    for idx, port in enumerate(unnecessary_ports_list, 1):
        if port in PORT_SERVICES:
            service, version, description, service_name, disable_cmd = PORT_SERVICES[port]
        else:
            service = "UNKNOWN"
            service_name = "unknown"
            description = "Unknown service"
            disable_cmd = "N/A"
        
        print(f"\nPORT {port}: {service.upper()} - SHOULD BE CLOSED")
        print("-" * 80)
        print(f"Expected Service: {description}")
        print(f"Service Process:  {service_name}")
        print(f"Current Status:   PORT OPEN | NO SERVICE RUNNING")
        
        print(f"\nWHY IS THIS PORT OPEN?")
        print(f"  * Service crashed but port binding remained")
        print(f"  * Firewall misconfiguration")
        print(f"  * Service uninstalled but port not released")
        print(f"  * System configuration error")
        
        print(f"\nSECURITY RISKS:")
        print(f"  * Unused open ports are prime attack vectors")
        print(f"  * Hackers scan for open ports as entry points")
        print(f"  * No legitimate business reason to keep it open")
        print(f"  * Violates security hardening best practices")
        
        # Show disable guide if available
        guide = get_disable_guide(port)
        if guide:
            print(f"\nHOW TO CLOSE THIS PORT:")
            print(f"\nMethod 1: Disable Service (Recommended)")
            print(f"Reason: {guide['why_disable']}")
            print(f"\nLinux Commands:")
            for cmd in guide['linux_disable']:
                print(f"  $ {cmd}")
            print(f"\nWindows Steps:")
            for cmd in guide['windows_disable']:
                print(f"  > {cmd}")
            print(f"\nVerify Closure:")
            print(f"  $ {guide['verify']}")
        else:
            print(f"\nHOW TO CLOSE THIS PORT:")
            print(f"\nLinux:   {disable_cmd}")
            print(f"Windows: Services.msc > {service_name} > Stop & Disable")
        
        print(f"\nMethod 2: Firewall Block")
        print(f"  Linux:   $ sudo ufw deny {port}")
        print(f"  Windows: Control Panel > Firewall > Block Port {port}")
        
        if idx < len(unnecessary_ports_list):
            print("\n" + "-"*80)


# CVE ANALYSIS
def cve_analysis(ports, cve_db):
    """Comprehensive vulnerability analysis with detailed exploit and prevention guidance"""
    print("\n" + "="*80)
    print("SECTION 4: CVE VULNERABILITY ANALYSIS")
    print("="*80 + "\n")

    for port in ports:
        if port not in PORT_SERVICES:
            continue

        service, version, service_full, process_name, disable_cmd = PORT_SERVICES[port]

        # Check CVE DB for this service
        if service not in cve_db:
            print(f"\nPORT {port}: {service.upper()} - No CVE data available\n")
            continue

        service_cves = cve_db[service]
        found_cve = False

        # Search through all versions for this service
        for version_entry in service_cves:
            cve_list = service_cves[version_entry] if isinstance(service_cves[version_entry], list) else [service_cves[version_entry]]
            
            for cve_entry in cve_list:
                found_cve = True
                
                print(f"\nPORT {port}: {service.upper()} - {service_full}")
                print("-" * 80)
                cve_id = cve_entry.get('cve', 'N/A')[:20]
                severity = cve_entry.get('severity', 'N/A')[:15]
                print(f"CVE ID:    {cve_id}")
                print(f"Severity:  {severity} (CVSS: {cve_entry.get('cvss_score', 'N/A')})")
                issue_short = cve_entry.get('issue', 'N/A')[:60]
                print(f"Issue:     {issue_short}")
                
                impact = cve_entry.get('impact', 'N/A')[:70]
                print(f"\nIMPACT:\n  {impact}")
                
                desc = cve_entry.get('description_urdu', 'N/A')[:70]
                print(f"\nEXPLANATION:\n  {desc}")
                
                exploit = cve_entry.get('how_hacker_exploits', 'N/A')[:70]
                print(f"\nEXPLOIT METHOD:\n  {exploit}")
                
                prevent = cve_entry.get('prevent', 'N/A')[:70]
                print(f"\nPREVENTION:\n  {prevent}")
                
                realworld = cve_entry.get('real_world_impact', 'N/A')[:70]
                print(f"\nREAL-WORLD IMPACT:\n  {realworld}\n")
        
        if not found_cve:
            print(f"\nPORT {port}: {service.upper()} - No specific CVE data\n")
    
    print("\n" + "="*80 + "\n")
