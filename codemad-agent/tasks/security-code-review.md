# Security Code Review Task

## Purpose

To conduct comprehensive security-focused code reviews to identify vulnerabilities, security weaknesses, and ensure adherence to secure coding practices.

## Inputs

- Source Code (pull requests, commits, or modules)
- Security Coding Standards
- Threat Model and Security Requirements
- Known Vulnerability Databases
- Security Testing Results

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with the security code review? We can work:
A. **Incrementally (Default & Recommended):** We'll review code sections systematically, discussing security findings.
B. **"YOLO" Mode:** I can perform a comprehensive security review and provide a complete report."

### 2. Prepare Security Review

- **Review Scope:** Define code components and security areas to focus on
- **Security Checklist:** Prepare security-specific review checklist
- **Tool Setup:** Configure static application security testing (SAST) tools
- **Baseline Assessment:** Establish security baseline and comparison metrics
- **Risk Context:** Review relevant threats and security requirements

### 3. Automated Security Analysis

- **SAST Scanning:** Run static application security testing tools
- **Dependency Scanning:** Analyze third-party dependencies for known vulnerabilities
- **Secret Detection:** Scan for hardcoded secrets, keys, and credentials
- **Configuration Review:** Analyze security configurations and settings
- **Compliance Checking:** Verify adherence to security coding standards

### 4. Manual Security Code Review

- **Input Validation:** Review all input validation and sanitization mechanisms
- **Authentication Logic:** Analyze authentication implementation and session management
- **Authorization Controls:** Review access control and permission checking logic
- **Cryptographic Implementation:** Examine encryption, hashing, and key management
- **Error Handling:** Review error handling to prevent information disclosure

### 5. Vulnerability Pattern Analysis

- **Injection Flaws:** Check for SQL injection, XSS, command injection vulnerabilities
- **Broken Authentication:** Review authentication bypass and session management issues
- **Sensitive Data Exposure:** Analyze data protection and encryption implementation
- **XML External Entities:** Check for XXE vulnerabilities in XML processing
- **Broken Access Control:** Review authorization and access control implementation
- **Security Misconfiguration:** Identify insecure default configurations
- **Cross-Site Scripting:** Analyze XSS prevention mechanisms
- **Insecure Deserialization:** Review object deserialization security
- **Known Vulnerable Components:** Check for use of components with known vulnerabilities
- **Insufficient Logging:** Review security event logging and monitoring

### 6. Security Architecture Review

- **Design Pattern Security:** Verify secure implementation of architectural patterns
- **Trust Boundary Validation:** Review security at trust boundaries
- **Privilege Management:** Analyze least privilege implementation
- **Secure Communication:** Review encryption and secure communication protocols
- **Data Flow Security:** Analyze security throughout data processing flows

### 7. Generate Security Review Report

- **Vulnerability Summary:** Categorize findings by severity and type
- **Risk Assessment:** Assess business risk and exploitability of findings
- **Remediation Guidance:** Provide specific fix recommendations and secure coding examples
- **Security Metrics:** Track security debt and improvement trends
- **Compliance Status:** Report on adherence to security standards and requirements

## Output Deliverables

- **Security Review Report** (detailed findings and recommendations)
- **Vulnerability Tracking** (prioritized security issues)
- **Secure Coding Guidelines** (team-specific recommendations)
- **Security Metrics Dashboard** (ongoing security posture tracking)

## Key Resources

- **Template:** `templates#security-assessment-tmpl`
- **Validation:** `checklists#code-security-review-checklist`
- **User Preferences:** `data#technical-preferences`
