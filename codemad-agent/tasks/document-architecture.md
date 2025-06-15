# Document Architecture Task

## Purpose

To create comprehensive technical architecture documentation that enables developers, architects, and stakeholders to understand, maintain, and evolve the system effectively.

## Inputs

- System Architecture Design
- Technical Specifications
- Design Decisions and Rationale
- Implementation Details
- Deployment and Operations Information

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with documenting the architecture? We can work:
A. **Incrementally (Default & Recommended):** We'll document each architectural aspect step-by-step.
B. **"YOLO" Mode:** I can create comprehensive architecture documentation for you to review."

### 2. Architecture Documentation Planning

- **Audience Analysis:** Identify documentation audiences (developers, architects, operations, management)
- **Documentation Scope:** Define what architectural aspects to document
- **Documentation Standards:** Establish architectural documentation standards and templates
- **Tool Selection:** Choose appropriate documentation tools and diagramming software
- **Information Architecture:** Plan documentation structure and cross-references
- **Maintenance Strategy:** Plan for ongoing documentation updates and reviews

### 3. System Overview Documentation

- **Architecture Vision:** Document the overall architectural vision and goals
- **System Context:** Describe how the system fits within the broader ecosystem
- **Key Stakeholders:** Identify and describe key stakeholders and their concerns
- **Quality Attributes:** Document non-functional requirements and quality attributes
- **Constraints and Assumptions:** Document architectural constraints and assumptions
- **Success Metrics:** Define metrics for measuring architectural success

### 4. Architectural Views and Perspectives

- **Logical View:** Document the logical structure and key abstractions
- **Process View:** Describe the runtime behavior and process interactions
- **Development View:** Document the development-time structure and organization
- **Physical View:** Describe the deployment and infrastructure architecture
- **Scenarios View:** Document key use cases and quality scenarios
- **Data View:** Describe data architecture and information flow

### 5. Component and Interface Documentation

- **Component Catalog:** Document all major components and their responsibilities
- **Interface Specifications:** Detail all interfaces and their contracts
- **Dependency Mapping:** Map dependencies between components and external systems
- **Communication Patterns:** Document communication patterns and protocols
- **Data Flow Diagrams:** Visualize data flow through the system
- **Sequence Diagrams:** Document key interaction sequences

### 6. Design Decisions and Rationale

- **Architectural Decision Records (ADRs):** Document key architectural decisions
- **Trade-off Analysis:** Document trade-offs considered and rationale for choices
- **Alternative Approaches:** Document alternatives considered and why they were rejected
- **Risk Assessment:** Document architectural risks and mitigation strategies
- **Evolution Strategy:** Document how the architecture can evolve over time
- **Technical Debt:** Document known technical debt and improvement plans

### 7. Implementation and Operations Guide

- **Development Guidelines:** Document development practices and coding standards
- **Build and Deployment:** Document build processes and deployment procedures
- **Configuration Management:** Document configuration and environment management
- **Monitoring and Observability:** Document monitoring, logging, and alerting strategies
- **Troubleshooting Guide:** Common issues and their resolution procedures
- **Performance Considerations:** Document performance characteristics and optimization strategies

## Output Deliverables

- **Architecture Documentation Portal** (comprehensive, navigable documentation)
- **System Architecture Document** (`docs/system-architecture.md`)
- **Component Documentation** (`docs/components/`)
- **Architectural Decision Records** (`docs/decisions/`)

## Key Resources

- **Template:** `templates#technical-specification-tmpl`
- **Validation:** `checklists#documentation-quality-checklist`
- **User Preferences:** `data#technical-preferences`
