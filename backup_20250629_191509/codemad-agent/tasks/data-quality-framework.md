# Data Quality Framework Task

## Purpose

To establish a comprehensive data quality framework that ensures data accuracy, completeness, consistency, and reliability across all data assets and processes.

## Inputs

- Data Architecture Document
- Business Data Requirements
- Data Sources and Systems Inventory
- Regulatory and Compliance Requirements
- Data Quality Standards and Policies

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with creating the data quality framework? We can work:
A. **Incrementally (Default & Recommended):** We'll build each quality component step-by-step.
B. **"YOLO" Mode:** I can design a comprehensive framework for you to review."

### 2. Data Quality Requirements Definition

- **Quality Dimensions:** Define data quality dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness)
- **Business Rules:** Document business rules and data validation requirements
- **Quality Metrics:** Define measurable data quality metrics and KPIs
- **Quality Thresholds:** Establish acceptable quality thresholds and SLAs
- **Stakeholder Requirements:** Gather data quality requirements from business stakeholders
- **Regulatory Requirements:** Ensure compliance with data quality regulations

### 3. Data Profiling and Assessment

- **Data Discovery:** Profile existing data sources to understand current quality state
- **Quality Assessment:** Assess current data quality against defined metrics
- **Issue Identification:** Identify common data quality issues and root causes
- **Impact Analysis:** Analyze business impact of data quality issues
- **Baseline Establishment:** Establish baseline data quality metrics for improvement tracking
- **Gap Analysis:** Identify gaps between current and desired data quality state

### 4. Data Quality Rules and Validation

- **Validation Rules:** Design comprehensive data validation rules and checks
- **Business Rule Implementation:** Implement business logic validation
- **Cross-Reference Validation:** Design validation against reference data and master data
- **Anomaly Detection:** Implement statistical and ML-based anomaly detection
- **Real-time Validation:** Design real-time data quality validation for streaming data
- **Batch Validation:** Implement comprehensive batch data quality checks

### 5. Data Quality Monitoring and Alerting

- **Quality Dashboards:** Design real-time data quality monitoring dashboards
- **Alerting System:** Implement automated alerting for data quality issues
- **Trend Analysis:** Monitor data quality trends and degradation patterns
- **Root Cause Analysis:** Implement tools for data quality issue root cause analysis
- **Quality Reporting:** Design regular data quality reporting for stakeholders
- **SLA Monitoring:** Monitor data quality SLAs and compliance metrics

### 6. Data Quality Remediation

- **Issue Classification:** Classify data quality issues by type and severity
- **Remediation Workflows:** Design workflows for data quality issue resolution
- **Data Cleansing:** Implement automated and manual data cleansing processes
- **Source System Fixes:** Coordinate with source system owners for upstream fixes
- **Quarantine Processes:** Implement data quarantine for poor quality data
- **Quality Improvement:** Design continuous data quality improvement processes

### 7. Data Quality Governance

- **Quality Policies:** Establish data quality policies and standards
- **Roles and Responsibilities:** Define data quality roles and accountability
- **Quality Processes:** Document data quality processes and procedures
- **Training and Awareness:** Develop data quality training and awareness programs
- **Quality Metrics:** Establish data quality metrics and reporting frameworks
- **Continuous Improvement:** Implement continuous data quality improvement processes

## Output Deliverables

- **Data Quality Framework Document** (`docs/data-quality-framework.md`)
- **Quality Monitoring Dashboard** (real-time quality metrics and alerts)
- **Data Quality Rules Repository** (comprehensive validation rules)
- **Quality Improvement Roadmap** (prioritized improvement initiatives)

## Key Resources

- **Template:** `templates#data-model-tmpl`
- **Validation:** `checklists#data-quality-checklist`
- **User Preferences:** `data#technical-preferences`
