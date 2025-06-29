# Security Architecture Review Task

## Purpose

To evaluate the security architecture design and implementation to ensure it adequately protects against identified threats and meets security requirements.

## Inputs

- System Architecture Documentation
- Security Requirements and Policies
- Threat Model and Risk Assessment
- Compliance Requirements
- Security Control Framework

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with the security architecture review? We can work:
A. **Incrementally (Default & Recommended):** We'll review each architectural component systematically.
B. **"YOLO" Mode:** I can perform a comprehensive review and provide a complete assessment."

### 2. Architecture Security Analysis

- **Security Design Principles:** Verify implementation of security design principles (defense in depth, least privilege, fail secure)
- **Trust Boundaries:** Analyze trust boundaries and security zones within the architecture
- **Attack Surface Analysis:** Identify and minimize the attack surface of the system
- **Security Control Placement:** Review placement and effectiveness of security controls
- **Integration Security:** Analyze security of system integrations and interfaces

### 3. Authentication and Authorization Review

- **Identity Management:** Review identity provider integration and user management
- **Authentication Mechanisms:** Analyze authentication methods and multi-factor authentication
- **Session Management:** Review session handling, timeout, and security controls
- **Authorization Model:** Analyze role-based access control and permission management
- **Privilege Management:** Review privilege escalation protections and administrative access

### 4. Data Protection Analysis

- **Data Classification:** Review data classification and handling requirements
- **Encryption Implementation:** Analyze encryption at rest and in transit
- **Key Management:** Review cryptographic key management and rotation
- **Data Loss Prevention:** Analyze data leakage prevention mechanisms
- **Privacy Controls:** Review privacy protection and data minimization implementation

### 5. Network Security Review

- **Network Segmentation:** Analyze network segmentation and micro-segmentation
- **Firewall Configuration:** Review firewall rules and network access controls
- **Secure Communication:** Analyze secure communication protocols and implementation
- **Network Monitoring:** Review network monitoring and intrusion detection capabilities
- **DMZ and Perimeter Security:** Analyze perimeter security controls and DMZ configuration

### 6. Infrastructure Security Assessment

- **Server Hardening:** Review server security configurations and hardening
- **Container Security:** Analyze container security and orchestration platform security
- **Cloud Security:** Review cloud security configurations and shared responsibility model
- **Backup and Recovery:** Analyze backup security and disaster recovery procedures
- **Patch Management:** Review vulnerability management and patching processes

### 7. Security Architecture Documentation

- **Security Architecture Diagram:** Create or update security architecture diagrams
- **Control Mapping:** Map security controls to threats and requirements
- **Gap Analysis:** Identify gaps between current and desired security posture
- **Improvement Recommendations:** Provide specific architecture improvement recommendations
- **Implementation Roadmap:** Create roadmap for security architecture enhancements

## Output Deliverables

- **Security Architecture Review Report** (`docs/security-architecture-review.md`)
- **Security Control Matrix** (controls mapped to threats and requirements)
- **Gap Analysis and Recommendations** (prioritized improvement plan)
- **Updated Security Architecture Diagrams** (visual representation of security controls)

## Key Resources

- **Template:** `templates#security-assessment-tmpl`
- **Validation:** `checklists#security-architecture-checklist`
- **User Preferences:** `data#technical-preferences`
