from analyzer import (
    scan_ports,
    print_ports_table,
    cve_analysis,
    load_cve_db,
    PORT_SERVICES
)

COMMON_PORTS = [
    21, 22, 23, 25, 80, 443,
    3306, 3389, 6379, 27017, 8080, 5432
]

def print_header():
    print("\n" + "="*80)
    print("NetRecon-Assist = IP PORT SCANNER & SECURITY ANALYZER")
    print("="*80)
    print("\nCapabilities:")
    print("  • Scan IP addresses for open ports")
    print("  • Detect running services with version information")
    print("  • Identify CVE security vulnerabilities")
    print("  • Provide step-by-step security recommendations")
    print("\n" + "-"*80 + "\n")

print_header()

target_ip = input("Enter Target IP Address: ").strip()

print("\n" + "="*80)
print("SELECT SCAN MODE")
print("="*80)
print("\n  1. FULL SCAN (Ports 1-65535)")
print("     Complete scan - slower, finds all open ports")
print("\n  2. QUICK SCAN (Common Ports)")
print("     Fast scan - checks 12 most common ports")
print("\n  3. CUSTOM SCAN (Your Choice)")
print("     Specify exact ports (e.g., 80,443,3306)")
print("\n" + "-"*80 + "\n")

choice = input("Your choice (1/2/3): ").strip()

if choice == "1":
    print("\nInitiating FULL PORT SCAN...")
    print("This will scan all 65,535 ports (may take 5-10 minutes)")
    ports_to_scan = list(range(1, 65536))
elif choice == "2":
    print("\nInitiating QUICK SCAN on 12 common ports...")
    ports_to_scan = COMMON_PORTS
elif choice == "3":
    user_ports = input("\nEnter port numbers (comma-separated, e.g., 80,443,3306): ")
    try:
        ports_to_scan = [int(p.strip()) for p in user_ports.split(",")]
        print(f"\nScanning {len(ports_to_scan)} custom ports: {', '.join(map(str, ports_to_scan))}")
    except:
        print("Invalid format! Using common ports instead.")
        ports_to_scan = COMMON_PORTS
else:
    print("Invalid choice! Using common ports.")
    ports_to_scan = COMMON_PORTS

# Perform port scan
open_ports = scan_ports(target_ip, ports_to_scan)

if not open_ports:
    print("\n" + "="*80)
    print("SCAN COMPLETE - NO OPEN PORTS FOUND")
    print("="*80)
    print("\nEXCELLENT! Your system is well protected.")
    print("All ports are closed to external access.")
    print("="*80 + "\n")
    exit()

# Display results
print("\n" + "="*80)
print(f"SCAN COMPLETE - FOUND {len(open_ports)} OPEN PORT(S)")
print("="*80)

# Show ports in organized sections
active_services, unnecessary_ports_data = print_ports_table(open_ports, target_ip)

# Extract port numbers from unnecessary ports
unnecessary_port_numbers = [p[0] for p in unnecessary_ports_data]

# Provide detailed guidance ONLY for unnecessary ports (no service running)
if unnecessary_port_numbers:
    from analyzer import provide_unnecessary_port_guidance
    provide_unnecessary_port_guidance(unnecessary_port_numbers, target_ip)

# CVE Analysis for active services
if active_services:
    active_port_numbers = [p[0] for p in active_services]
    cve_db = load_cve_db()
    from analyzer import cve_analysis
    cve_analysis(active_port_numbers, cve_db)

print("\n" + "="*80)
print("FINAL SUMMARY & SECURITY RECOMMENDATIONS")
print("="*80 + "\n")

if unnecessary_port_numbers:
    print("WARNING: " + str(len(unnecessary_port_numbers)) + " PORT(S) OPEN WITHOUT SERVICE")
    print("-" * 80)
    print("\nCRITICAL - These ports MUST be closed:\n")
    for p in unnecessary_port_numbers:
        service_name = "Unknown"
        if p in PORT_SERVICES:
            service_name = PORT_SERVICES[p][0].upper()
        print(f"  * Port {p} ({service_name}) - No service detected")
    print("\nACTION REQUIRED:")
    print("  1. Review Section 3 above for detailed instructions")
    print("  2. Execute provided commands for your OS (Linux/Windows)")
    print("  3. Verify ports are closed")
    print("  4. Re-run scanner to confirm closure")
    print()
else:
    print("EXCELLENT! All open ports have active services running.")
    print("No unnecessary ports detected - Good security posture!")
    print()

if active_services:
    print(f"\nACTIVE SERVICES SUMMARY: {len(active_services)} Service(s) Running")
    print("-" * 80)
    for p in active_services:
        risk = p[4] if len(p) > 4 else "?"
        status = f"[{risk} Risk]" if risk != "?" else "[Unknown]"
        service_short = p[1][:20] if len(p[1]) > 20 else p[1]
        print(f"  * Port {p[0]} ({service_short}) {status}")
    print()

print("="*80)
print("SECURITY PRINCIPLE: Fewer open ports = Smaller attack surface")
print("Only keep ports open that you actively need for business.")
print("="*80 + "\n")
