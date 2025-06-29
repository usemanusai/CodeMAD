# Design Data Architecture Task

## Purpose

To design a comprehensive data architecture that supports current and future data needs, ensuring scalability, performance, reliability, and compliance with data governance requirements.

## Inputs

- Product Requirements Document (PRD)
- System Architecture Document
- Data Requirements and Use Cases
- Compliance and Regulatory Requirements
- Performance and Scalability Requirements

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with designing the data architecture? We can work:
A. **Incrementally (Default & Recommended):** We'll design each data component step-by-step, discussing approach and getting your feedback.
B. **"YOLO" Mode:** I can design a comprehensive data architecture for you to review."

### 2. Data Requirements Analysis

- **Data Sources:** Identify all internal and external data sources
- **Data Types:** Catalog structured, semi-structured, and unstructured data types
- **Data Volume:** Estimate current and projected data volumes and growth rates
- **Data Velocity:** Analyze data ingestion rates and real-time processing requirements
- **Data Variety:** Document different data formats, schemas, and sources
- **Data Quality Requirements:** Define data accuracy, completeness, and consistency needs

### 3. Data Architecture Design

- **Data Storage Strategy:** Design storage solutions for different data types and access patterns
- **Data Lake vs Data Warehouse:** Determine appropriate data storage architectures
- **Data Partitioning:** Design data partitioning strategies for performance and scalability
- **Data Retention:** Define data lifecycle management and retention policies
- **Data Archival:** Plan for data archival and long-term storage strategies
- **Backup and Recovery:** Design data backup and disaster recovery procedures

### 4. Data Processing Architecture

- **Batch Processing:** Design batch data processing workflows and schedules
- **Stream Processing:** Architect real-time data processing and streaming analytics
- **ETL/ELT Pipelines:** Design extract, transform, load processes and data pipelines
- **Data Transformation:** Plan data cleansing, enrichment, and transformation logic
- **Data Orchestration:** Design workflow orchestration and dependency management
- **Error Handling:** Implement data processing error handling and recovery mechanisms

### 5. Data Integration and APIs

- **Data Integration Patterns:** Design patterns for data integration across systems
- **API Strategy:** Plan data APIs for internal and external consumption
- **Data Synchronization:** Design real-time and batch data synchronization mechanisms
- **Change Data Capture:** Implement CDC for tracking data changes
- **Data Federation:** Plan for federated data access across multiple sources
- **Master Data Management:** Design master data management and data governance

### 6. Data Security and Governance

- **Data Classification:** Implement data classification and sensitivity labeling
- **Access Controls:** Design role-based access controls for data assets
- **Data Encryption:** Plan encryption at rest and in transit for sensitive data
- **Data Lineage:** Implement data lineage tracking and metadata management
- **Compliance Controls:** Ensure compliance with GDPR, CCPA, and other regulations
- **Data Quality Monitoring:** Design data quality monitoring and alerting systems

### 7. Performance and Scalability

- **Query Optimization:** Design indexing and query optimization strategies
- **Caching Strategy:** Implement data caching for frequently accessed data
- **Horizontal Scaling:** Plan for horizontal scaling of data processing and storage
- **Performance Monitoring:** Design performance monitoring and optimization processes
- **Capacity Planning:** Plan for data storage and processing capacity growth
- **Cost Optimization:** Optimize data architecture for cost efficiency

## Output Deliverables

- **Data Architecture Document** (`docs/data-architecture.md`)
- **Data Flow Diagrams** (visual representation of data movement)
- **Data Model Specifications** (logical and physical data models)
- **Data Pipeline Designs** (ETL/ELT process specifications)

## Key Resources

- **Template:** `templates#data-model-tmpl`
- **Validation:** `checklists#data-pipeline-checklist`
- **User Preferences:** `data#technical-preferences`
