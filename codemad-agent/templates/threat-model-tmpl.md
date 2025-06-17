# {{Project Name}} Threat Model

[[LLM: This template creates a comprehensive threat model using the STRIDE methodology. Populate each section based on system architecture and security analysis.]]

## Executive Summary

[[LLM: Provide a high-level overview of the security posture, key threats identified, and recommended security controls.]]

## System Overview

### System Description
[[LLM: Brief description of the system being analyzed]]

### System Boundaries
[[LLM: Clear definition of what is included and excluded from the threat model]]

### Assets and Data Classification
- **Critical Assets:** {{List of critical assets requiring protection}}
- **Sensitive Data:** {{Types of sensitive data handled by the system}}
- **Data Classification:** {{Data classification levels and handling requirements}}

## System Architecture

### Architecture Diagram
[[LLM: Insert system architecture diagram with trust boundaries marked]]

### Components and Services
[[LLM: List and describe each major component]]
- **Component 1:** {{Description and security relevance}}
- **Component 2:** {{Description and security relevance}}

### Trust Boundaries
[[LLM: Description of trust boundaries between different system components and external entities]]

### Data Flow Analysis
[[LLM: Description of how data flows through the system and across trust boundaries]]

## Threat Analysis

### Threat Modeling Methodology
[[LLM: Description of threat modeling approach used - e.g., STRIDE, PASTA, OCTAVE]]

### Identified Threats

#### Spoofing Threats
| Threat ID | Description | Asset Affected | Likelihood | Impact | Risk Score |
|-----------|-------------|----------------|------------|---------|------------|
| S001 | {{Threat description}} | {{Asset}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{Score}} |

#### Tampering Threats
| Threat ID | Description | Asset Affected | Likelihood | Impact | Risk Score |
|-----------|-------------|----------------|------------|---------|------------|
| T001 | {{Threat description}} | {{Asset}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{Score}} |

#### Repudiation Threats
| Threat ID | Description | Asset Affected | Likelihood | Impact | Risk Score |
|-----------|-------------|----------------|------------|---------|------------|
| R001 | {{Threat description}} | {{Asset}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{Score}} |

#### Information Disclosure Threats
| Threat ID | Description | Asset Affected | Likelihood | Impact | Risk Score |
|-----------|-------------|----------------|------------|---------|------------|
| I001 | {{Threat description}} | {{Asset}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{Score}} |

#### Denial of Service Threats
| Threat ID | Description | Asset Affected | Likelihood | Impact | Risk Score |
|-----------|-------------|----------------|------------|---------|------------|
| D001 | {{Threat description}} | {{Asset}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{Score}} |

#### Elevation of Privilege Threats
| Threat ID | Description | Asset Affected | Likelihood | Impact | Risk Score |
|-----------|-------------|----------------|------------|---------|------------|
| E001 | {{Threat description}} | {{Asset}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{Score}} |

## Risk Assessment

### Risk Scoring Methodology
[[LLM: Description of how risk scores are calculated]]

### High-Risk Threats
[[LLM: List of threats with high risk scores requiring immediate attention]]

### Medium-Risk Threats
[[LLM: List of threats with medium risk scores requiring planned mitigation]]

## Security Controls and Mitigations

### Preventive Controls
| Control ID | Description | Threats Mitigated | Implementation Status |
|------------|-------------|-------------------|----------------------|
| PC001 | {{Control description}} | {{Threat IDs}} | {{Planned/In Progress/Implemented}} |

### Detective Controls
| Control ID | Description | Threats Detected | Implementation Status |
|------------|-------------|------------------|----------------------|
| DC001 | {{Control description}} | {{Threat IDs}} | {{Planned/In Progress/Implemented}} |

### Corrective Controls
| Control ID | Description | Threats Addressed | Implementation Status |
|------------|-------------|-------------------|----------------------|
| CC001 | {{Control description}} | {{Threat IDs}} | {{Planned/In Progress/Implemented}} |

## Implementation Roadmap

### Phase 1: Critical Security Controls
[[LLM: List critical controls with timeline]]
- {{Control 1 - Timeline}}
- {{Control 2 - Timeline}}

### Phase 2: Important Security Controls
[[LLM: List important controls with timeline]]
- {{Control 1 - Timeline}}
- {{Control 2 - Timeline}}

## Monitoring and Validation

### Security Monitoring Requirements
[[LLM: Requirements for monitoring security controls and detecting threats]]

### Validation Procedures
[[LLM: Procedures for validating the effectiveness of security controls]]

## Assumptions and Dependencies

### Security Assumptions
[[LLM: Key security assumptions made during threat modeling]]

### External Dependencies
[[LLM: External security dependencies and their implications]]
