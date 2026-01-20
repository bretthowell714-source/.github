# Security Testing & Penetration Testing Guide

**⚠️ LEGAL DISCLAIMER**: Unauthorized access to computer systems is illegal. This guide is for **AUTHORIZED TESTING ONLY**. Always obtain written authorization before conducting any security testing.

Comprehensive guide for conducting authorized penetration tests using Metasploit and Kali Linux tools.

## Table of Contents

1. [Authorization & Legal Framework](#authorization--legal-framework)
2. [Engagement Planning](#engagement-planning)
3. [Rules of Engagement](#rules-of-engagement)
4. [Testing Methodology](#testing-methodology)
5. [Documentation](#documentation)
6. [Reporting](#reporting)
7. [Post-Testing Cleanup](#post-testing-cleanup)
8. [Escalation Procedures](#escalation-procedures)

## Authorization & Legal Framework

### Required Documentation

Before any testing begins, ensure you have:

1. **Written Authorization Letter**
   ```
   Should include:
   - Company letterhead
   - Specific systems to test
   - Testing window (dates/times)
   - Scope and limitations
   - Point of contact
   - Legal authorization
   ```

2. **Rules of Engagement (ROE)**
   - Clearly defined scope
   - Off-limits systems
   - Testing constraints
   - Communication protocols
   - Emergency procedures

3. **Non-Disclosure Agreement (NDA)**
   - Confidentiality terms
   - Data handling procedures
   - Report distribution limits

4. **Liability Waiver**
   - Acknowledgment of risks
   - Damage liability
   - Legal protections

### Legal Considerations

**United States**
- Computer Fraud and Abuse Act (CFAA)
- Unauthorized access is a federal crime
- Can result in up to 10 years imprisonment
- Civil liability for damages

**European Union**
- GDPR (General Data Protection Regulation)
- Network and Information Systems Directive
- Data breach notification requirements
- Significant financial penalties

**Other Jurisdictions**
- Similar laws exist in most countries
- Penalties vary by jurisdiction
- International law applies to cross-border testing
- Always consult legal counsel

### Authorization Checklist

```
Before Testing:
□ Written authorization obtained
□ Scope clearly defined in writing
□ ROE document signed
□ Testing window scheduled
□ Stakeholders notified
□ Emergency contacts established
□ Legal review completed
□ Insurance verified
□ Approval from management
□ NDA/liability signed
```

## Engagement Planning

### Pre-Engagement Discovery

1. **Client Interview**
   - Business objectives
   - Systems to test
   - Security concerns
   - Previous assessments
   - Known vulnerabilities

2. **Scope Definition**
   - IP ranges to test
   - Systems included/excluded
   - Testing methods allowed
   - Data sensitivity levels
   - Acceptable risk

3. **Timeline Planning**
   - Testing duration
   - Preferred test window
   - Reporting timeline
   - Remediation period

4. **Resource Allocation**
   - Team size
   - Testing tools
   - Lab environment
   - Communication tools

### Risk Assessment

Evaluate potential impact:
- **High Risk**: Core systems (financials, healthcare, critical infrastructure)
- **Medium Risk**: Business operations
- **Low Risk**: Non-critical systems

Plan accordingly with:
- Reduced scope for high-risk systems
- Extended timeline for safe testing
- 24/7 monitoring and support
- Quick rollback procedures

## Rules of Engagement

### Testing Boundaries

**ALLOWED**
- Authorized systems only
- Defined scope
- Specified testing window
- Approved techniques

**NOT ALLOWED**
- Denial of Service attacks
- Data destruction
- Social engineering
- Testing outside scope
- Unauthorized access attempts
- Testing outside scheduled window

### Communication Protocol

1. **Daily Standups**
   - Report findings
   - Discuss next steps
   - Address concerns

2. **Incident Communication**
   - Immediately notify client if:
     - System unavailable
     - Unexpected behavior
     - Out-of-scope impact
     - Data exposure detected

3. **Contact Escalation**
   - Primary contact
   - Secondary contact
   - Emergency contact

### Sensitive Data Handling

```
Policy:
□ No copying of sensitive data
□ No exfiltration from systems
□ Secure deletion after testing
□ Limited access within team
□ Encrypted communications
□ Secure storage of findings
```

## Testing Methodology

### OSSTMM (Open Source Security Testing Methodology Manual)

```
Phase 1: Reconnaissance
  → Information gathering
  → Network mapping
  → Service enumeration

Phase 2: Scanning
  → Port scanning
  → Service detection
  → Vulnerability identification

Phase 3: Enumeration
  → User accounts
  → Shares and resources
  → System configuration

Phase 4: Exploitation
  → Vulnerability verification
  → System compromise
  → Data access

Phase 5: Post-Exploitation
  → System persistence
  → Privilege escalation
  → Data collection

Phase 6: Cleanup
  → Remove artifacts
  → Restore systems
  → Document findings
```

### PTES (Penetration Testing Execution Standard)

```
1. Pre-engagement Interactions
   □ Client discussion
   □ Scope definition
   □ Authorization

2. Intelligence Gathering
   □ Passive reconnaissance
   □ Active scanning
   □ Information analysis

3. Threat Modeling
   □ Identify attack vectors
   □ Risk assessment
   □ Prioritize testing

4. Vulnerability Analysis
   □ Scan for known vulnerabilities
   □ Manual testing
   □ Analysis

5. Exploitation
   □ Verify vulnerabilities
   □ Establish access
   □ Document findings

6. Post-Exploitation
   □ Escalate privileges
   □ Maintain access
   □ Gather intelligence

7. Reporting
   □ Document findings
   □ Calculate risk
   □ Provide recommendations
```

### NIST Testing Methodology

```
Planning & Scoping
- Define objectives
- Determine scope
- Resource planning

Reconnaissance
- Passive information gathering
- Public data collection
- Social engineering tests

Scanning & Enumeration
- Active discovery
- Service detection
- Vulnerability scanning

Vulnerability Analysis
- Verify findings
- Determine exploitability
- Assess impact

Exploitation
- Execute attacks
- Verify compromises
- Document access

Post-Exploitation
- Privilege escalation
- Lateral movement
- Data collection

Reporting
- Risk analysis
- Recommendations
- Remediation guidance
```

### Common Tool Workflows

#### Network Reconnaissance
```
1. Passive scanning
   whois domain.com
   nslookup domain.com
   nmap -sL domain.com

2. Active discovery
   nmap -sn 192.168.1.0/24

3. Port scanning
   nmap -sV -p- 192.168.1.100

4. OS detection
   nmap -O 192.168.1.100

5. Service enumeration
   nmap --script smb-os-discovery 192.168.1.100
```

#### Web Application Testing
```
1. Reconnaissance
   whatweb target.com
   nikto -h target.com

2. Manual exploration
   Browser + Burp Suite

3. Parameter fuzzing
   wfuzz -w wordlist.txt http://target.com/FUZZ

4. Vulnerability testing
   sqlmap -u "http://target.com?id=1"
   xsser testing

5. Authentication bypass
   Credential testing

6. File upload testing
   Malicious file uploads
```

#### Wireless Testing
```
1. Reconnaissance
   airodump-ng mon0

2. Capture handshake
   aireplay-ng -0 1 -a BSSID mon0

3. Crack password
   aircrack-ng -w wordlist.txt capture.cap

4. Authentication
   Connect to network

5. Post-exploitation
   ARP spoofing
   MITM attacks
```

## Documentation

### During Testing

Document:
- Test date/time
- Tools used
- Systems tested
- Commands executed
- Results obtained
- Findings discovered
- Screenshots
- Logs

### Finding Documentation Template

```
Finding ID: VULN-001
Title: SQL Injection in Login Form
Severity: High (CVSS: 8.9)
Description:
  The login form is vulnerable to SQL injection
  allowing unauthorized database access

Affected System:
  - Web server: target.com
  - Port: 80 (HTTP)
  - Application: Custom web app

Proof of Concept:
  URL: http://target.com/login?user=admin' OR '1'='1
  Result: Bypassed authentication

Impact:
  - Unauthorized access to database
  - Exposure of sensitive data
  - Potential data modification

Remediation:
  - Use parameterized queries
  - Input validation
  - Output encoding

Remediation Deadline: [Date]
```

## Reporting

### Report Structure

```
1. Executive Summary
   - Overview of engagement
   - High-level findings
   - Risk assessment

2. Findings Summary
   - Total vulnerabilities found
   - Breakdown by severity
   - Key metrics

3. Detailed Findings
   - Each vulnerability documented
   - Evidence provided
   - Impact assessed

4. Risk Assessment
   - CVSS scores
   - Business impact
   - Priority recommendations

5. Remediation Roadmap
   - Immediate actions
   - Short-term improvements
   - Long-term strategy

6. Appendices
   - Tools used
   - Scan results
   - Screenshots
   - Recommendations
```

### Severity Ratings

```
CRITICAL (CVSS 9.0-10.0)
- Immediate action required
- Exploitable with default config
- Complete system compromise

HIGH (CVSS 7.0-8.9)
- Urgent attention needed
- Significant impact likely
- Exploitation probable

MEDIUM (CVSS 4.0-6.9)
- Should be addressed
- Moderate impact
- May require exploitation

LOW (CVSS 0.1-3.9)
- Monitor and plan remediation
- Limited immediate impact
- Opportunistic exploitation
```

## Post-Testing Cleanup

### System Cleanup Checklist

```
□ Remove shells/backdoors
□ Delete uploaded files
□ Restore modified files
□ Clear logs
  □ Access logs
  □ Event logs
  □ Application logs
□ Terminate established sessions
□ Remove persistence mechanisms
□ Verify system functionality
□ Test critical services
```

### Data Cleanup

```
□ Delete assessment tools
□ Secure destruction of findings
□ Encrypt sensitive data
□ Remove test accounts
□ Revoke test access
□ Final verification
```

### Verification Steps

```
1. System functionality
   - Verify all services running
   - Check system performance
   - Confirm data integrity

2. Security review
   - Verify no backdoors remain
   - Check firewall rules
   - Review access logs

3. Documentation
   - Confirm findings documented
   - Verify evidence captured
   - Final report review
```

## Escalation Procedures

### During Testing Issues

**System Goes Down**
1. Immediately stop testing
2. Notify primary contact
3. Provide incident details
4. Assist with restoration
5. Document incident

**Unexpected Behavior**
1. Document exact behavior
2. Notify client immediately
3. Do not continue testing
4. Await instructions
5. Assist with investigation

**Data Exposure**
1. Immediately stop testing
2. Notify emergency contact
3. Document scope of exposure
4. Secure the data
5. Assist with breach response

## Best Practices

### Security Testing Best Practices

```
1. Never test without authorization
2. Always define scope in writing
3. Establish communication protocol
4. Use staging/lab when possible
5. Test during agreed windows
6. Document everything
7. Maintain confidentiality
8. Provide actionable recommendations
9. Clean up completely
10. Follow up on remediation
```

### Tool Best Practices

```
1. Understand tool capabilities
2. Test in lab first
3. Use least destructive method
4. Verify tool output
5. Maintain tool licenses
6. Keep tools updated
7. Use appropriate tool versions
8. Understand false positives
9. Combine multiple tools
10. Validate findings manually
```

### Communication Best Practices

```
1. Clear and professional communication
2. Regular status updates
3. Immediate incident notification
4. Documented decisions
5. Mutual understanding of scope
6. Escalation procedures documented
7. Emergency contacts established
8. Clear reporting timeline
9. Final meeting to discuss findings
10. Remediation follow-up
```

## Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PTES](http://www.pentest-standard.org/)
- [NIST SP 800-115](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf)
- [CEH Study Guide](https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/)
- [OSSTMM](http://www.isecom.org/research/osstmm.html)

---

**Last Updated**: January 2026

**⚠️ CRITICAL DISCLAIMER**: This guide is provided for authorized security testing only. The author, contributors, and publishers assume no liability for illegal use or misuse. Violating laws regarding unauthorized computer access can result in criminal prosecution and civil liability. Always obtain written authorization before conducting security tests.

**AUTHORIZED USE ONLY** ✅
