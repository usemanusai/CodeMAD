# Data Migration Strategy Task

## Purpose

To develop a comprehensive strategy for migrating data from legacy systems to new platforms while ensuring data integrity, minimal downtime, and business continuity.

## Inputs

- Current System Architecture and Data Models
- Target System Architecture and Requirements
- Business Requirements and Constraints
- Data Volume and Complexity Assessment
- Migration Timeline and Resource Constraints

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with creating the data migration strategy? We can work:
A. **Incrementally (Default & Recommended):** We'll plan each migration phase step-by-step.
B. **"YOLO" Mode:** I can create a comprehensive migration strategy for you to review."

### 2. Migration Assessment and Planning

- **Current State Analysis:** Analyze existing data sources, formats, and quality
- **Target State Definition:** Define target data architecture and requirements
- **Gap Analysis:** Identify differences between source and target systems
- **Risk Assessment:** Identify migration risks and mitigation strategies
- **Resource Planning:** Plan migration team, tools, and infrastructure resources
- **Timeline Development:** Create detailed migration timeline and milestones

### 3. Data Migration Strategy Design

- **Migration Approach:** Choose appropriate migration strategy (big bang, phased, parallel run)
- **Migration Patterns:** Design migration patterns for different data types
- **Cutover Strategy:** Plan system cutover and rollback procedures
- **Downtime Minimization:** Design strategies to minimize business disruption
- **Rollback Planning:** Develop comprehensive rollback and recovery procedures
- **Business Continuity:** Ensure business operations continuity during migration

### 4. Data Mapping and Transformation

- **Data Mapping:** Create detailed mapping between source and target data structures
- **Transformation Rules:** Define data transformation and cleansing rules
- **Business Logic Migration:** Plan migration of business rules and calculations
- **Data Validation:** Design validation rules for migrated data
- **Reference Data Migration:** Plan migration of reference and master data
- **Historical Data Handling:** Define strategy for historical data migration

### 5. Migration Tool and Infrastructure Setup

- **Tool Selection:** Select appropriate data migration tools and platforms
- **Infrastructure Provisioning:** Set up migration infrastructure and environments
- **Performance Optimization:** Optimize migration processes for performance
- **Monitoring Setup:** Implement migration monitoring and progress tracking
- **Security Configuration:** Ensure secure data transfer and access controls
- **Backup and Recovery:** Set up backup and recovery for migration processes

### 6. Migration Execution and Validation

- **Pre-migration Validation:** Validate source data quality and readiness
- **Migration Execution:** Execute migration according to planned procedures
- **Data Validation:** Perform comprehensive validation of migrated data
- **Reconciliation:** Reconcile data between source and target systems
- **Performance Testing:** Test system performance with migrated data
- **User Acceptance Testing:** Conduct UAT with migrated data and systems

### 7. Post-Migration Activities

- **Go-Live Support:** Provide support during initial go-live period
- **Issue Resolution:** Resolve any post-migration data or system issues
- **Performance Monitoring:** Monitor system performance and data quality
- **Documentation Update:** Update system documentation and procedures
- **Lessons Learned:** Document lessons learned and best practices
- **Decommissioning:** Plan decommissioning of legacy systems and data

## Output Deliverables

- **Data Migration Strategy Document** (`docs/data-migration-strategy.md`)
- **Migration Runbooks** (detailed execution procedures)
- **Data Mapping Specifications** (source to target mappings)
- **Validation and Testing Plans** (comprehensive testing procedures)

## Key Resources

- **Template:** `templates#data-pipeline-tmpl`
- **Validation:** `checklists#data-pipeline-checklist`
- **User Preferences:** `data#technical-preferences`
