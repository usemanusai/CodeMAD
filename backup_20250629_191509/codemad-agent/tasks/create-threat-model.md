# Create Threat Model Task

## Purpose

To systematically identify, analyze, and mitigate security threats and vulnerabilities in the system architecture and design, ensuring comprehensive security coverage.

## Inputs

- System Architecture Document
- Data Flow Diagrams
- User Stories and Use Cases
- Compliance Requirements
- Asset Inventory and Classification

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with creating the threat model? We can work:
A. **Incrementally (Default & Recommended):** We'll go through each threat modeling step systematically, discussing findings and mitigations.
B. **"YOLO" Mode:** I can create a comprehensive threat model for you to review."

### 2. Define Threat Modeling Scope

- **System Boundaries:** Clearly define what components, data flows, and interactions are included
- **Assets Identification:** Catalog all assets including data, systems, and processes that need protection
- **Trust Boundaries:** Identify trust boundaries between different system components and external entities
- **Entry Points:** Map all system entry points including APIs, user interfaces, and integrations
- **Assumptions and Dependencies:** Document security assumptions and external dependencies

### 3. Create System Model

- **Architecture Decomposition:** Break down the system into components, data stores, and processes
- **Data Flow Mapping:** Map how data flows through the system and between components
- **Trust Zones:** Define different trust zones and security contexts within the system
- **External Dependencies:** Model interactions with external systems and third-party services
- **User Roles and Permissions:** Map different user types and their access levels

### 4. Identify Threats Using STRIDE

- **Spoofing:** Identify threats related to identity spoofing and impersonation
- **Tampering:** Analyze data and system integrity threats
- **Repudiation:** Identify non-repudiation and audit trail threats
- **Information Disclosure:** Analyze confidentiality and data exposure threats
- **Denial of Service:** Identify availability and service disruption threats
- **Elevation of Privilege:** Analyze authorization and privilege escalation threats

### 5. Assess Risk and Impact

- **Threat Likelihood:** Assess the probability of each identified threat occurring
- **Impact Assessment:** Evaluate the potential business and technical impact of each threat
- **Risk Scoring:** Calculate risk scores using likelihood and impact assessments
- **Risk Prioritization:** Prioritize threats based on risk scores and business criticality
- **Attack Vector Analysis:** Analyze how threats could be exploited and attack paths

### 6. Design Security Controls

- **Preventive Controls:** Design controls to prevent threats from occurring
- **Detective Controls:** Implement monitoring and detection mechanisms
- **Corrective Controls:** Plan response and recovery procedures for security incidents
- **Control Mapping:** Map security controls to specific threats and vulnerabilities
- **Defense in Depth:** Ensure multiple layers of security controls for critical assets

### 7. Create Threat Model Documentation

Using the `threat-model-tmpl` template, create comprehensive documentation including:
- Executive summary of security posture
- Detailed threat analysis and risk assessment
- Security control recommendations
- Implementation roadmap and priorities
- Monitoring and validation requirements

## Output Deliverables

- **Threat Model Document** (`docs/threat-model.md`)
- **Risk Assessment Matrix** (threats prioritized by risk)
- **Security Control Specifications** (detailed control requirements)
- **Security Architecture Updates** (recommended architecture changes)

## Key Resources

- **Template:** `templates#threat-model-tmpl`
- **Validation:** `checklists#security-architecture-checklist`
- **User Preferences:** `data#technical-preferences`
