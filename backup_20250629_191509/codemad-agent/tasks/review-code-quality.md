# Review Code Quality Task

## Purpose

To conduct comprehensive code quality reviews focusing on maintainability, performance, security, and adherence to coding standards and best practices.

## Inputs

- Source Code (pull requests, commits, or complete modules)
- Coding Standards and Style Guidelines
- Architecture Documentation
- Security Requirements
- Performance Requirements

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with the code quality review? We can work:
A. **Incrementally (Default & Recommended):** We'll review code sections step-by-step, discussing findings and recommendations.
B. **"YOLO" Mode:** I can perform a comprehensive review and provide a complete report."

### 2. Setup Code Review Process

- **Review Scope:** Define what code will be reviewed (new features, bug fixes, refactoring)
- **Review Criteria:** Establish quality criteria and checklists for reviews
- **Tool Integration:** Set up code review tools and static analysis integration
- **Review Timeline:** Define review timelines and approval processes

### 3. Conduct Static Code Analysis

- **Automated Analysis:** Run static analysis tools to identify potential issues
- **Code Metrics:** Analyze complexity, maintainability, and technical debt metrics
- **Security Scanning:** Perform automated security vulnerability scanning
- **Dependency Analysis:** Review third-party dependencies for security and licensing issues
- **Code Coverage:** Analyze test coverage and identify untested code paths

### 4. Manual Code Review

- **Architecture Compliance:** Verify code follows architectural patterns and principles
- **Coding Standards:** Check adherence to established coding standards and conventions
- **Logic Review:** Analyze business logic for correctness and edge case handling
- **Error Handling:** Review error handling and exception management
- **Performance Considerations:** Identify potential performance bottlenecks

### 5. Security Code Review

- **Input Validation:** Review input sanitization and validation mechanisms
- **Authentication/Authorization:** Verify proper access controls and security checks
- **Data Protection:** Review encryption, data handling, and privacy compliance
- **Injection Prevention:** Check for SQL injection, XSS, and other injection vulnerabilities
- **Secure Configuration:** Review security configurations and hardening measures

### 6. Quality Assessment and Recommendations

- **Issue Prioritization:** Categorize findings by severity and impact
- **Improvement Recommendations:** Provide specific, actionable improvement suggestions
- **Best Practice Guidance:** Share relevant best practices and patterns
- **Technical Debt Assessment:** Identify and document technical debt items
- **Knowledge Sharing:** Facilitate learning and knowledge transfer through reviews

### 7. Generate Review Report

- **Summary Dashboard:** Create overview of code quality metrics and trends
- **Detailed Findings:** Document specific issues with locations and recommendations
- **Action Items:** Create prioritized list of improvements and fixes needed
- **Quality Trends:** Track quality improvements or degradation over time
- **Team Feedback:** Provide constructive feedback to development team

## Output Deliverables

- **Code Review Report** (with findings and recommendations)
- **Quality Metrics Dashboard** (automated quality tracking)
- **Action Item List** (prioritized improvements)
- **Best Practices Guide** (team-specific recommendations)

## Key Resources

- **Validation:** `checklists#qa-testing-checklist`
- **User Preferences:** `data#technical-preferences`
